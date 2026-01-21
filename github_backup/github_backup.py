#!/usr/bin/env python

from __future__ import print_function

import argparse
import base64
import calendar
import codecs
import errno
import json
import logging
import os
import platform
import random
import re
import select
import socket
import ssl
import subprocess
import sys
import time
from collections.abc import Generator
from datetime import datetime
from http.client import IncompleteRead
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

try:
    from . import __version__

    VERSION = __version__
except ImportError:
    VERSION = "unknown"

FNULL = open(os.devnull, "w")
FILE_URI_PREFIX = "file://"
logger = logging.getLogger(__name__)


class RepositoryUnavailableError(Exception):
    """Raised when a repository is unavailable due to legal reasons (e.g., DMCA takedown)."""

    def __init__(self, message, dmca_url=None):
        super().__init__(message)
        self.dmca_url = dmca_url


# Setup SSL context with fallback chain
https_ctx = ssl.create_default_context()
if https_ctx.get_ca_certs():
    # Layer 1: Certificates pre-loaded from system (file-based)
    pass
else:
    paths = ssl.get_default_verify_paths()
    if (paths.cafile and os.path.exists(paths.cafile)) or (
        paths.capath and os.path.exists(paths.capath)
    ):
        # Layer 2: Cert paths exist, will be lazy-loaded on first use (directory-based)
        pass
    else:
        # Layer 3: Try certifi package as optional fallback
        try:
            import certifi

            https_ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            # All layers failed - no certificates available anywhere
            sys.exit(
                "\nERROR: No CA certificates found. Cannot connect to GitHub over SSL.\n\n"
                "Solutions you can explore:\n"
                "  1. pip install certifi\n"
                "  2. Alpine: apk add ca-certificates\n"
                "  3. Debian/Ubuntu: apt-get install ca-certificates\n\n"
            )


def logging_subprocess(
    popenargs, stdout_log_level=logging.DEBUG, stderr_log_level=logging.ERROR, **kwargs
):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.
    """
    child = subprocess.Popen(
        popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )
    if sys.platform == "win32":
        logger.info(
            "Windows operating system detected - no subprocess logging will be returned"
        )

    log_level = {child.stdout: stdout_log_level, child.stderr: stderr_log_level}

    def check_io():
        if sys.platform == "win32":
            return
        ready_to_read = select.select([child.stdout, child.stderr], [], [], 1000)[0]
        for io in ready_to_read:
            line = io.readline()
            if not logger:
                continue
            if not (io == child.stderr and not line):
                logger.log(log_level[io], line[:-1])

    # keep checking stdout/stderr until the child exits
    while child.poll() is None:
        check_io()

    check_io()  # check again to catch anything after the process exits

    rc = child.wait()

    if rc != 0:
        print("{} returned {}:".format(popenargs[0], rc), file=sys.stderr)
        print("\t", " ".join(popenargs), file=sys.stderr)

    return rc


def mkdir_p(*args):
    for path in args:
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def mask_password(url, secret="*****"):
    parsed = urlparse(url)

    if not parsed.password:
        return url
    elif parsed.password == "x-oauth-basic":
        return url.replace(parsed.username, secret)

    return url.replace(parsed.password, secret)


def non_negative_int(value):
    """Argparse type validator for non-negative integers."""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid integer")
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} must be 0 or greater")
    return ivalue


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Backup a github account")
    parser.add_argument("user", metavar="USER", type=str, help="github username")
    parser.add_argument(
        "-t",
        "--token",
        dest="token_classic",
        help="personal access, OAuth, or JSON Web token, or path to token (file://...)",
    )  # noqa
    parser.add_argument(
        "-f",
        "--token-fine",
        dest="token_fine",
        help="fine-grained personal access token (github_pat_....), or path to token (file://...)",
    )  # noqa
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        dest="quiet",
        help="supress log messages less severe than warning, e.g. info",
    )
    parser.add_argument(
        "--as-app",
        action="store_true",
        dest="as_app",
        help="authenticate as github app instead of as a user.",
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        default=".",
        dest="output_directory",
        help="directory at which to backup the repositories",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default="info",
        dest="log_level",
        help="log level to use (default: info, possible levels: debug, info, warning, error, critical)",
    )
    parser.add_argument(
        "-i",
        "--incremental",
        action="store_true",
        dest="incremental",
        help="incremental backup",
    )
    parser.add_argument(
        "--incremental-by-files",
        action="store_true",
        dest="incremental_by_files",
        help="incremental backup based on modification date of files",
    )
    parser.add_argument(
        "--starred",
        action="store_true",
        dest="include_starred",
        help="include JSON output of starred repositories in backup",
    )
    parser.add_argument(
        "--all-starred",
        action="store_true",
        dest="all_starred",
        help="include starred repositories in backup [*]",
    )
    parser.add_argument(
        "--starred-skip-size-over",
        type=int,
        metavar="MB",
        dest="starred_skip_size_over",
        help="skip starred repositories larger than this size in MB",
    )
    parser.add_argument(
        "--watched",
        action="store_true",
        dest="include_watched",
        help="include JSON output of watched repositories in backup",
    )
    parser.add_argument(
        "--followers",
        action="store_true",
        dest="include_followers",
        help="include JSON output of followers in backup",
    )
    parser.add_argument(
        "--following",
        action="store_true",
        dest="include_following",
        help="include JSON output of following users in backup",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="include_everything",
        help="include everything in backup (not including [*])",
    )
    parser.add_argument(
        "--issues",
        action="store_true",
        dest="include_issues",
        help="include issues in backup",
    )
    parser.add_argument(
        "--issue-comments",
        action="store_true",
        dest="include_issue_comments",
        help="include issue comments in backup",
    )
    parser.add_argument(
        "--issue-events",
        action="store_true",
        dest="include_issue_events",
        help="include issue events in backup",
    )
    parser.add_argument(
        "--pulls",
        action="store_true",
        dest="include_pulls",
        help="include pull requests in backup",
    )
    parser.add_argument(
        "--pull-comments",
        action="store_true",
        dest="include_pull_comments",
        help="include pull request review comments in backup",
    )
    parser.add_argument(
        "--pull-commits",
        action="store_true",
        dest="include_pull_commits",
        help="include pull request commits in backup",
    )
    parser.add_argument(
        "--pull-details",
        action="store_true",
        dest="include_pull_details",
        help="include more pull request details in backup [*]",
    )
    parser.add_argument(
        "--labels",
        action="store_true",
        dest="include_labels",
        help="include labels in backup",
    )
    parser.add_argument(
        "--hooks",
        action="store_true",
        dest="include_hooks",
        help="include hooks in backup (works only when authenticated)",
    )  # noqa
    parser.add_argument(
        "--milestones",
        action="store_true",
        dest="include_milestones",
        help="include milestones in backup",
    )
    parser.add_argument(
        "--security-advisories",
        action="store_true",
        dest="include_security_advisories",
        help="include security advisories in backup",
    )
    parser.add_argument(
        "--repositories",
        action="store_true",
        dest="include_repository",
        help="include repository clone in backup",
    )
    parser.add_argument(
        "--bare", action="store_true", dest="bare_clone", help="clone bare repositories"
    )
    parser.add_argument(
        "--no-prune",
        action="store_true",
        dest="no_prune",
        help="disable prune option for git fetch",
    )
    parser.add_argument(
        "--lfs",
        action="store_true",
        dest="lfs_clone",
        help="clone LFS repositories (requires Git LFS to be installed, https://git-lfs.github.com) [*]",
    )
    parser.add_argument(
        "--wikis",
        action="store_true",
        dest="include_wiki",
        help="include wiki clone in backup",
    )
    parser.add_argument(
        "--gists",
        action="store_true",
        dest="include_gists",
        help="include gists in backup [*]",
    )
    parser.add_argument(
        "--starred-gists",
        action="store_true",
        dest="include_starred_gists",
        help="include starred gists in backup [*]",
    )
    parser.add_argument(
        "--skip-archived",
        action="store_true",
        dest="skip_archived",
        help="skip project if it is archived",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        dest="skip_existing",
        help="skip project if a backup directory exists",
    )
    parser.add_argument(
        "-L",
        "--languages",
        dest="languages",
        help="only allow these languages",
        nargs="*",
    )
    parser.add_argument(
        "-N",
        "--name-regex",
        dest="name_regex",
        help="python regex to match names against",
    )
    parser.add_argument(
        "-H", "--github-host", dest="github_host", help="GitHub Enterprise hostname"
    )
    parser.add_argument(
        "-O",
        "--organization",
        action="store_true",
        dest="organization",
        help="whether or not this is an organization user",
    )
    parser.add_argument(
        "-R",
        "--repository",
        dest="repository",
        help="name of repository to limit backup to",
    )
    parser.add_argument(
        "-P",
        "--private",
        action="store_true",
        dest="private",
        help="include private repositories [*]",
    )
    parser.add_argument(
        "-F",
        "--fork",
        action="store_true",
        dest="fork",
        help="include forked repositories [*]",
    )
    parser.add_argument(
        "--prefer-ssh",
        action="store_true",
        help="Clone repositories using SSH instead of HTTPS",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + VERSION
    )
    parser.add_argument(
        "--keychain-name",
        dest="osx_keychain_item_name",
        help="OSX ONLY: name field of password item in OSX keychain that holds the personal access or OAuth token",
    )
    parser.add_argument(
        "--keychain-account",
        dest="osx_keychain_item_account",
        help="OSX ONLY: account field of password item in OSX keychain that holds the personal access or OAuth token",
    )
    parser.add_argument(
        "--releases",
        action="store_true",
        dest="include_releases",
        help="include release information, not including assets or binaries",
    )
    parser.add_argument(
        "--latest-releases",
        type=int,
        default=0,
        dest="number_of_latest_releases",
        help="include certain number of the latest releases; only applies if including releases",
    )
    parser.add_argument(
        "--skip-prerelease",
        action="store_true",
        dest="skip_prerelease",
        help="skip prerelease and draft versions; only applies if including releases",
    )
    parser.add_argument(
        "--assets",
        action="store_true",
        dest="include_assets",
        help="include assets alongside release information; only applies if including releases",
    )
    parser.add_argument(
        "--skip-assets-on",
        dest="skip_assets_on",
        nargs="*",
        help="skip asset downloads for these repositories",
    )
    parser.add_argument(
        "--attachments",
        action="store_true",
        dest="include_attachments",
        help="download user-attachments from issues and pull requests",
    )
    parser.add_argument(
        "--throttle-limit",
        dest="throttle_limit",
        type=int,
        default=0,
        help="start throttling of GitHub API requests after this amount of API requests remain",
    )
    parser.add_argument(
        "--throttle-pause",
        dest="throttle_pause",
        type=float,
        default=30.0,
        help="wait this amount of seconds when API request throttling is active (default: 30.0, requires --throttle-limit to be set)",
    )
    parser.add_argument(
        "--exclude", dest="exclude", help="names of repositories to exclude", nargs="*"
    )
    parser.add_argument(
        "--retries",
        dest="max_retries",
        type=non_negative_int,
        default=5,
        help="maximum number of retries for API calls (default: 5)",
    )
    return parser.parse_args(args)


def get_auth(args, encode=True, for_git_cli=False):
    auth = None

    if args.osx_keychain_item_name:
        if not args.osx_keychain_item_account:
            raise Exception(
                "You must specify both name and account fields for osx keychain password items"
            )
        else:
            if platform.system() != "Darwin":
                raise Exception("Keychain arguments are only supported on Mac OSX")
            try:
                with open(os.devnull, "w") as devnull:
                    token = subprocess.check_output(
                        [
                            "security",
                            "find-generic-password",
                            "-s",
                            args.osx_keychain_item_name,
                            "-a",
                            args.osx_keychain_item_account,
                            "-w",
                        ],
                        stderr=devnull,
                    ).strip()
                token = token.decode("utf-8")
                auth = token + ":" + "x-oauth-basic"
            except subprocess.SubprocessError:
                raise Exception(
                    "No password item matching the provided name and account could be found in the osx keychain."
                )
    elif args.osx_keychain_item_account:
        raise Exception(
            "You must specify both name and account fields for osx keychain password items"
        )
    elif args.token_fine:
        if args.token_fine.startswith(FILE_URI_PREFIX):
            args.token_fine = read_file_contents(args.token_fine)

        if args.token_fine.startswith("github_pat_"):
            auth = args.token_fine
        else:
            raise Exception(
                "Fine-grained token supplied does not look like a GitHub PAT"
            )
    elif args.token_classic:
        if args.token_classic.startswith(FILE_URI_PREFIX):
            args.token_classic = read_file_contents(args.token_classic)

        if not args.as_app:
            auth = args.token_classic + ":" + "x-oauth-basic"
        else:
            if not for_git_cli:
                auth = args.token_classic
            else:
                auth = "x-access-token:" + args.token_classic

    if not auth:
        return None

    if not encode or args.token_fine is not None:
        return auth

    return base64.b64encode(auth.encode("ascii"))


def get_github_api_host(args):
    if args.github_host:
        host = args.github_host + "/api/v3"
    else:
        host = "api.github.com"

    return host


def get_github_host(args):
    if args.github_host:
        host = args.github_host
    else:
        host = "github.com"

    return host


def read_file_contents(file_uri):
    return open(file_uri[len(FILE_URI_PREFIX) :], "rt").readline().strip()


def get_github_repo_url(args, repository):
    if repository.get("is_gist"):
        if args.prefer_ssh:
            # The git_pull_url value is always https for gists, so we need to transform it to ssh form
            repo_url = re.sub(
                r"^https?:\/\/(.+)\/(.+)\.git$",
                r"git@\1:\2.git",
                repository["git_pull_url"],
            )
            repo_url = re.sub(
                r"^git@gist\.", "git@", repo_url
            )  # strip gist subdomain for better hostkey compatibility
        else:
            repo_url = repository["git_pull_url"]
        return repo_url

    if args.prefer_ssh:
        return repository["ssh_url"]

    auth = get_auth(args, encode=False, for_git_cli=True)
    if auth:
        repo_url = "https://{0}@{1}/{2}/{3}.git".format(
            auth if args.token_fine is None else "oauth2:" + auth,
            get_github_host(args),
            repository["owner"]["login"],
            repository["name"],
        )
    else:
        repo_url = repository["clone_url"]

    return repo_url


def calculate_retry_delay(attempt, headers):
    """Calculate delay before next retry with exponential backoff."""
    # Respect retry-after header if present
    if retry_after := headers.get("retry-after"):
        return int(retry_after)

    # Respect rate limit reset time
    if int(headers.get("x-ratelimit-remaining", 1)) < 1:
        reset_time = int(headers.get("x-ratelimit-reset", 0))
        return max(10, reset_time - calendar.timegm(time.gmtime()))

    # Exponential backoff with jitter for server errors (1s base, 120s max)
    delay = min(1.0 * (2**attempt), 120.0)
    return delay + random.uniform(0, delay * 0.1)


def retrieve_data(args, template, query_args=None, paginated=True):
    """
    Fetch the data from GitHub API.

    Handle both single requests and pagination with yield of individual dicts.
    Handles throttling, retries, read errors, and DMCA takedowns.
    """
    query_args = query_args or {}
    auth = get_auth(args, encode=not args.as_app)
    per_page = 100

    def _extract_next_page_url(link_header):
        for link in link_header.split(","):
            if 'rel="next"' in link:
                return link[link.find("<") + 1 : link.find(">")]
        return None

    def fetch_all() -> Generator[dict, None, None]:
        next_url = None

        while True:
            # FIRST: Fetch response

            for attempt in range(args.max_retries + 1):
                request = _construct_request(
                    per_page=per_page if paginated else None,
                    query_args=query_args,
                    template=next_url or template,
                    auth=auth,
                    as_app=args.as_app,
                    fine=args.token_fine is not None,
                )
                http_response = make_request_with_retry(request, auth, args.max_retries)

                match http_response.getcode():
                    case 200:
                        # Success - Parse JSON response
                        try:
                            response = json.loads(http_response.read().decode("utf-8"))
                            break  # Exit retry loop and handle the data returned
                        except (
                            IncompleteRead,
                            json.decoder.JSONDecodeError,
                            TimeoutError,
                        ) as e:
                            logger.warning(f"{type(e).__name__} reading response")
                            if attempt < args.max_retries:
                                delay = calculate_retry_delay(attempt, {})
                                logger.warning(
                                    f"Retrying read in {delay:.1f}s (attempt {attempt + 1}/{args.max_retries + 1})"
                                )
                                time.sleep(delay)
                            continue  # Next retry attempt

                    case 451:
                        # DMCA takedown - extract URL if available, then raise
                        dmca_url = None
                        try:
                            response_data = json.loads(
                                http_response.read().decode("utf-8")
                            )
                            dmca_url = response_data.get("block", {}).get("html_url")
                        except Exception:
                            pass
                        raise RepositoryUnavailableError(
                            "Repository unavailable due to legal reasons (HTTP 451)",
                            dmca_url=dmca_url,
                        )

                    case _:
                        raise Exception(
                            f"API request returned HTTP {http_response.getcode()}: {http_response.reason}"
                        )
            else:
                logger.error(
                    f"Failed to read response after {args.max_retries + 1} attempts for {next_url or template}"
                )
                raise Exception(
                    f"Failed to read response after {args.max_retries + 1} attempts for {next_url or template}"
                )

            # SECOND: Process and paginate

            # Pause before next request if rate limit is low
            if (
                remaining := int(http_response.headers.get("x-ratelimit-remaining", 0))
            ) <= (args.throttle_limit or 0):
                if args.throttle_limit:
                    logger.info(
                        f"Throttling: {remaining} requests left, pausing {args.throttle_pause}s"
                    )
                    time.sleep(args.throttle_pause)

            # Yield results
            if isinstance(response, list):
                yield from response
            elif isinstance(response, dict):
                yield response

            # Check for more pages
            if not paginated or not (
                next_url := _extract_next_page_url(
                    http_response.headers.get("Link", "")
                )
            ):
                break  # No more data

    return list(fetch_all())


def make_request_with_retry(request, auth, max_retries=5):
    """Make HTTP request with automatic retry for transient errors."""

    def is_retryable_status(status_code, headers):
        # Server errors are always retryable
        if status_code in (500, 502, 503, 504):
            return True
        # Rate limit (403/429) is retryable if limit exhausted
        if status_code in (403, 429):
            return int(headers.get("x-ratelimit-remaining", 1)) < 1
        return False

    for attempt in range(max_retries + 1):
        try:
            return urlopen(request, context=https_ctx)

        except HTTPError as exc:
            # HTTPError can be used as a response-like object
            if not is_retryable_status(exc.code, exc.headers):
                logger.error(
                    f"API Error: {exc.code} {exc.reason} for {request.full_url}"
                )
                raise  # Non-retryable error

            if attempt >= max_retries:
                logger.error(
                    f"HTTP {exc.code} failed after {max_retries + 1} attempts for {request.full_url}"
                )
                raise

            delay = calculate_retry_delay(attempt, exc.headers)
            logger.warning(
                f"HTTP {exc.code} ({exc.reason}), retrying in {delay:.1f}s "
                f"(attempt {attempt + 1}/{max_retries + 1}) for {request.full_url}"
            )
            if auth is None and exc.code in (403, 429):
                logger.info("Hint: Authenticate to raise your GitHub rate limit")
            time.sleep(delay)

        except (URLError, socket.error) as e:
            if attempt >= max_retries:
                logger.error(
                    f"Connection error failed after {max_retries + 1} attempts: {e} for {request.full_url}"
                )
                raise
            delay = calculate_retry_delay(attempt, {})
            logger.warning(
                f"Connection error: {e}, retrying in {delay:.1f}s "
                f"(attempt {attempt + 1}/{max_retries + 1}) for {request.full_url}"
            )
            time.sleep(delay)

    raise Exception(
        f"Request failed after {max_retries + 1} attempts"
    )  # pragma: no cover


def _construct_request(per_page, query_args, template, auth, as_app=None, fine=False):
    # If template is already a full URL with query params (from Link header), use it directly
    if "?" in template and template.startswith("http"):
        request_url = template
        # Extract query string for logging
        querystring = template.split("?", 1)[1]
    else:
        # Build URL with query parameters
        all_query_args = {}
        if per_page:
            all_query_args["per_page"] = per_page
        if query_args:
            all_query_args.update(query_args)

        request_url = template
        if all_query_args:
            querystring = urlencode(all_query_args)
            request_url = template + "?" + querystring
        else:
            querystring = ""

    request = Request(request_url)
    if auth is not None:
        if not as_app:
            if fine:
                request.add_header("Authorization", "token " + auth)
            else:
                request.add_header("Authorization", "Basic ".encode("ascii") + auth)
        else:
            auth = auth.encode("ascii")
            request.add_header("Authorization", "token ".encode("ascii") + auth)

    log_url = template if "?" not in template else template.split("?")[0]
    if querystring:
        log_url += "?" + querystring
    logger.info("Requesting {}".format(log_url))
    return request


class S3HTTPRedirectHandler(HTTPRedirectHandler):
    """
    A subclassed redirect handler for downloading Github assets from S3.

    urllib will add the Authorization header to the redirected request to S3, which will result in a 400,
    so we should remove said header on redirect.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        request = super(S3HTTPRedirectHandler, self).redirect_request(
            req, fp, code, msg, headers, newurl
        )
        # Only delete Authorization header if it exists (attachments may not have it)
        if "Authorization" in request.headers:
            del request.headers["Authorization"]
        return request


def download_file(url, path, auth, as_app=False, fine=False):
    # Skip downloading release assets if they already exist on disk so we don't redownload on every sync
    if os.path.exists(path):
        return

    request = _construct_request(
        per_page=None,
        query_args={},
        template=url,
        auth=auth,
        as_app=as_app,
        fine=fine,
    )
    request.add_header("Accept", "application/octet-stream")
    opener = build_opener(S3HTTPRedirectHandler)

    try:
        response = opener.open(request)

        chunk_size = 16 * 1024
        with open(path, "wb") as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
    except HTTPError as exc:
        # Gracefully handle 404 responses (and others) when downloading from S3
        logger.warning(
            "Skipping download of asset {0} due to HTTPError: {1}".format(
                url, exc.reason
            )
        )
    except URLError as e:
        # Gracefully handle other URL errors
        logger.warning(
            "Skipping download of asset {0} due to URLError: {1}".format(url, e.reason)
        )
    except socket.error as e:
        # Gracefully handle socket errors
        # TODO: Implement retry logic
        logger.warning(
            "Skipping download of asset {0} due to socker error: {1}".format(
                url, e.strerror
            )
        )


def download_attachment_file(url, path, auth, as_app=False, fine=False):
    """Download attachment file directly (not via GitHub API).

    Similar to download_file() but for direct file URLs, not API endpoints.
    Attachment URLs (user-images, user-attachments) are direct downloads,
    not API endpoints, so we skip _construct_request() which adds API params.

    URL Format Support & Authentication Requirements:

    | URL Format                                   | Auth Required | Notes                    |
    |----------------------------------------------|---------------|--------------------------|
    | github.com/user-attachments/assets/*         | Private only  | Modern format (2024+)    |
    | github.com/user-attachments/files/*          | Private only  | Modern format (2024+)    |
    | user-images.githubusercontent.com/*          | No (public)   | Legacy CDN, all eras     |
    | private-user-images.githubusercontent.com/*  | JWT in URL    | Legacy private (5min)    |
    | github.com/{owner}/{repo}/files/*            | Repo filter   | Old repo files           |

    - Modern user-attachments: Requires GitHub token auth for private repos
    - Legacy public CDN: No auth needed/accepted (returns 400 with auth header)
    - Legacy private CDN: Uses JWT token embedded in URL, no GitHub token needed
    - Repo files: Filtered to current repository only during extraction

    Returns dict with metadata:
        - success: bool
        - http_status: int (200, 404, etc.)
        - content_type: str or None
        - original_filename: str or None (from Content-Disposition)
        - size_bytes: int or None
        - error: str or None
    """
    import re
    from datetime import datetime, timezone

    metadata = {
        "url": url,
        "success": False,
        "http_status": None,
        "content_type": None,
        "original_filename": None,
        "size_bytes": None,
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "error": None,
    }

    # Create simple request (no API query params)
    request = Request(url)
    request.add_header("Accept", "application/octet-stream")

    # Add authentication header only for modern github.com/user-attachments URLs
    # Legacy CDN URLs (user-images.githubusercontent.com) are public and don't need/accept auth
    # Private CDN URLs (private-user-images) use JWT tokens embedded in the URL
    if auth is not None and "github.com/user-attachments/" in url:
        if not as_app:
            if fine:
                # Fine-grained token: plain token with "token " prefix
                request.add_header("Authorization", "token " + auth)
            else:
                # Classic token: base64-encoded with "Basic " prefix
                request.add_header("Authorization", "Basic ".encode("ascii") + auth)
        else:
            # App authentication
            auth = auth.encode("ascii")
            request.add_header("Authorization", "token ".encode("ascii") + auth)

    # Reuse S3HTTPRedirectHandler from download_file()
    opener = build_opener(S3HTTPRedirectHandler)

    temp_path = path + ".temp"

    try:
        response = opener.open(request)
        metadata["http_status"] = response.getcode()

        # Extract Content-Type
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
        if content_type:
            metadata["content_type"] = content_type

        # Extract original filename from Content-Disposition header
        # Format: attachment; filename=example.mov or attachment;filename="example.mov"
        content_disposition = response.headers.get("Content-Disposition", "")
        if content_disposition:
            # Match: filename=something or filename="something" or filename*=UTF-8''something
            match = re.search(r'filename\*?=["\']?([^"\';\r\n]+)', content_disposition)
            if match:
                original_filename = match.group(1).strip()
                # Handle RFC 5987 encoding: filename*=UTF-8''example.mov
                if "UTF-8''" in original_filename:
                    original_filename = original_filename.split("UTF-8''")[1]
                metadata["original_filename"] = original_filename

        # Fallback: Extract filename from final URL after redirects
        # This handles user-attachments/assets URLs which redirect to S3 with filename.ext
        if not metadata["original_filename"]:
            from urllib.parse import urlparse, unquote

            final_url = response.geturl()
            parsed = urlparse(final_url)
            # Get filename from path (last component before query string)
            path_parts = parsed.path.split("/")
            if path_parts:
                # URL might be encoded, decode it
                filename_from_url = unquote(path_parts[-1])
                # Only use if it has an extension
                if "." in filename_from_url:
                    metadata["original_filename"] = filename_from_url

        # Download file to temporary location
        chunk_size = 16 * 1024
        bytes_downloaded = 0
        with open(temp_path, "wb") as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                bytes_downloaded += len(chunk)

        # Atomic rename to final location
        os.replace(temp_path, path)

        metadata["size_bytes"] = bytes_downloaded
        metadata["success"] = True

    except HTTPError as exc:
        metadata["http_status"] = exc.code
        metadata["error"] = str(exc.reason)
        logger.warning(
            "Skipping download of attachment {0} due to HTTPError: {1}".format(
                url, exc.reason
            )
        )
    except URLError as e:
        metadata["error"] = str(e.reason)
        logger.warning(
            "Skipping download of attachment {0} due to URLError: {1}".format(
                url, e.reason
            )
        )
    except socket.error as e:
        metadata["error"] = str(e.strerror) if hasattr(e, "strerror") else str(e)
        logger.warning(
            "Skipping download of attachment {0} due to socket error: {1}".format(
                url, e.strerror if hasattr(e, "strerror") else str(e)
            )
        )
    except Exception as e:
        metadata["error"] = str(e)
        logger.warning(
            "Skipping download of attachment {0} due to error: {1}".format(url, str(e))
        )
        # Clean up temp file if it was partially created
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

    return metadata


def get_jwt_signed_url_via_markdown_api(url, token, repo_context):
    """Convert a user-attachments/assets URL to a JWT-signed URL via Markdown API.

    GitHub's Markdown API renders image URLs and returns HTML containing
    JWT-signed private-user-images.githubusercontent.com URLs that work
    without token authentication.

    This is a workaround for issue #477 where fine-grained PATs cannot
    download user-attachments URLs from private repos directly.

    Limitations:
    - Only works for /assets/ URLs (images)
    - Does NOT work for /files/ URLs (PDFs, text files, etc.)
    - JWT URLs expire after ~5 minutes

    Args:
        url: The github.com/user-attachments/assets/UUID URL
        token: Raw fine-grained PAT (github_pat_...)
        repo_context: Repository context as "owner/repo"

    Returns:
        str: JWT-signed URL from private-user-images.githubusercontent.com
        None: If conversion fails
    """

    try:
        payload = json.dumps(
            {"text": f"![img]({url})", "mode": "gfm", "context": repo_context}
        ).encode("utf-8")

        request = Request("https://api.github.com/markdown", data=payload, method="POST")
        request.add_header("Authorization", f"token {token}")
        request.add_header("Content-Type", "application/json")
        request.add_header("Accept", "application/vnd.github+json")

        html = urlopen(request, timeout=30).read().decode("utf-8")

        # Parse JWT-signed URL from HTML response
        # Format: <img src="https://private-user-images.githubusercontent.com/...?jwt=..." ...>
        if match := re.search(
            r'src="(https://private-user-images\.githubusercontent\.com/[^"]+)"', html
        ):
            jwt_url = match.group(1)
            logger.debug("Converted attachment URL to JWT-signed URL via Markdown API")
            return jwt_url

        logger.debug("Markdown API response did not contain JWT-signed URL")
        return None

    except HTTPError as e:
        logger.debug(
            "Markdown API request failed with HTTP {0}: {1}".format(e.code, e.reason)
        )
        return None
    except Exception as e:
        logger.debug("Markdown API request failed: {0}".format(str(e)))
        return None


def extract_attachment_urls(item_data, issue_number=None, repository_full_name=None):
    """Extract GitHub-hosted attachment URLs from issue/PR body and comments.

    What qualifies as an attachment?
    There is no "attachment" concept in the GitHub API - it's a user behavior pattern
    we've identified through analysis of real-world repositories. We define attachments as:

    - User-uploaded files hosted on GitHub's CDN domains
    - Found outside of code blocks (not examples/documentation)
    - Matches known GitHub attachment URL patterns

    This intentionally captures bare URLs pasted by users, not just markdown/HTML syntax.
    Some false positives (example URLs in documentation) may occur - these fail gracefully
    with HTTP 404 and are logged in the manifest.

    Supported URL formats:
    - Modern: github.com/user-attachments/{assets,files}/*
    - Legacy: user-images.githubusercontent.com/* (including private-user-images)
    - Repo files: github.com/{owner}/{repo}/files/* (filtered to current repo)
    - Repo assets: github.com/{owner}/{repo}/assets/* (filtered to current repo)

    Repository filtering (repo files/assets only):
    - Direct match: URL is for current repository → included
    - Redirect match: URL redirects to current repository → included (handles renames/transfers)
    - Different repo: URL is for different repository → excluded

    Code block filtering:
    - Removes fenced code blocks (```) and inline code (`) before extraction
    - Prevents extracting URLs from code examples and documentation snippets

    Args:
        item_data: Issue or PR data dict
        issue_number: Issue/PR number for logging
        repository_full_name: Full repository name (owner/repo) for filtering repo-scoped URLs
    """
    import re

    urls = []

    # Define all GitHub attachment patterns
    # Stop at markdown punctuation: whitespace, ), `, ", >, <
    # Trailing sentence punctuation (. ! ? , ; : ' ") is stripped in post-processing
    patterns = [
        r'https://github\.com/user-attachments/(?:assets|files)/[^\s\)`"<>]+',  # Modern
        r'https://(?:private-)?user-images\.githubusercontent\.com/[^\s\)`"<>]+',  # Legacy CDN
    ]

    # Add repo-scoped patterns (will be filtered by repository later)
    # These patterns match ANY repo, then we filter to current repo with redirect checking
    repo_files_pattern = r'https://github\.com/[^/]+/[^/]+/files/\d+/[^\s\)`"<>]+'
    repo_assets_pattern = r'https://github\.com/[^/]+/[^/]+/assets/\d+/[^\s\)`"<>]+'
    patterns.append(repo_files_pattern)
    patterns.append(repo_assets_pattern)

    def clean_url(url):
        """Remove trailing sentence and markdown punctuation that's not part of the URL."""
        return url.rstrip(".!?,;:'\")")

    def remove_code_blocks(text):
        """Remove markdown code blocks (fenced and inline) from text.

        This prevents extracting URLs from code examples like:
        - Fenced code blocks: ```code```
        - Inline code: `code`
        """
        # Remove fenced code blocks first (```...```)
        # DOTALL flag makes . match newlines
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

        # Remove inline code (`...`)
        # Non-greedy match between backticks
        text = re.sub(r"`[^`]*`", "", text)

        return text

    def is_repo_scoped_url(url):
        """Check if URL is a repo-scoped attachment (files or assets)."""
        return bool(
            re.match(r"https://github\.com/[^/]+/[^/]+/(?:files|assets)/\d+/", url)
        )

    def check_redirect_to_current_repo(url, current_repo):
        """Check if URL redirects to current repository.

        Returns True if:
        - URL is already for current repo
        - URL redirects (301/302) to current repo (handles renames/transfers)

        Returns False otherwise (URL is for a different repo).
        """
        # Extract owner/repo from URL
        match = re.match(r"https://github\.com/([^/]+)/([^/]+)/", url)
        if not match:
            return False

        url_owner, url_repo = match.groups()
        url_repo_full = f"{url_owner}/{url_repo}"

        # Direct match - no need to check redirect
        if url_repo_full.lower() == current_repo.lower():
            return True

        # Different repo - check if it redirects to current repo
        # This handles repository transfers and renames
        try:
            import urllib.request
            import urllib.error

            # Make HEAD request with redirect following disabled
            # We need to manually handle redirects to see the Location header
            request = urllib.request.Request(url, method="HEAD")
            request.add_header("User-Agent", "python-github-backup")

            # Create opener that does NOT follow redirects
            class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None  # Don't follow redirects

            opener = urllib.request.build_opener(NoRedirectHandler)

            try:
                _ = opener.open(request, timeout=10)
                # Got 200 - URL works as-is but for different repo
                return False
            except urllib.error.HTTPError as e:
                # Check if it's a redirect (301, 302, 307, 308)
                if e.code in (301, 302, 307, 308):
                    location = e.headers.get("Location", "")
                    # Check if redirect points to current repo
                    if location:
                        redirect_match = re.match(
                            r"https://github\.com/([^/]+)/([^/]+)/", location
                        )
                        if redirect_match:
                            redirect_owner, redirect_repo = redirect_match.groups()
                            redirect_repo_full = f"{redirect_owner}/{redirect_repo}"
                            return redirect_repo_full.lower() == current_repo.lower()
                return False
        except Exception:
            # On any error (timeout, network issue, etc.), be conservative
            # and exclude the URL to avoid downloading from wrong repos
            return False

    # Extract from body
    body = item_data.get("body") or ""
    # Remove code blocks before searching for URLs
    body_cleaned = remove_code_blocks(body)
    for pattern in patterns:
        found_urls = re.findall(pattern, body_cleaned)
        urls.extend([clean_url(url) for url in found_urls])

    # Extract from issue comments
    if "comment_data" in item_data:
        for comment in item_data["comment_data"]:
            comment_body = comment.get("body") or ""
            # Remove code blocks before searching for URLs
            comment_cleaned = remove_code_blocks(comment_body)
            for pattern in patterns:
                found_urls = re.findall(pattern, comment_cleaned)
                urls.extend([clean_url(url) for url in found_urls])

    # Extract from PR regular comments
    if "comment_regular_data" in item_data:
        for comment in item_data["comment_regular_data"]:
            comment_body = comment.get("body") or ""
            # Remove code blocks before searching for URLs
            comment_cleaned = remove_code_blocks(comment_body)
            for pattern in patterns:
                found_urls = re.findall(pattern, comment_cleaned)
                urls.extend([clean_url(url) for url in found_urls])

    regex_urls = list(set(urls))  # dedupe

    # Filter repo-scoped URLs to current repository only
    # This handles repository transfers/renames via redirect checking
    if repository_full_name:
        filtered_urls = []
        for url in regex_urls:
            if is_repo_scoped_url(url):
                # Check if URL belongs to current repo (or redirects to it)
                if check_redirect_to_current_repo(url, repository_full_name):
                    filtered_urls.append(url)
                # else: skip URLs from other repositories
            else:
                # Non-repo-scoped URLs (user-attachments, CDN) - always include
                filtered_urls.append(url)
        regex_urls = filtered_urls

    return regex_urls


def get_attachment_filename(url):
    """Get filename from attachment URL, handling all GitHub formats.

    Formats:
    - github.com/user-attachments/assets/{uuid} → uuid (add extension later)
    - github.com/user-attachments/files/{id}/{filename} → filename
    - github.com/{owner}/{repo}/files/{id}/{filename} → filename
    - user-images.githubusercontent.com/{user}/{hash}.{ext} → hash.ext
    - private-user-images.githubusercontent.com/...?jwt=... → extract from path
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path_parts = parsed.path.split("/")

    # Modern: /user-attachments/files/{id}/{filename}
    if "user-attachments/files" in parsed.path:
        return path_parts[-1]

    # Modern: /user-attachments/assets/{uuid}
    elif "user-attachments/assets" in parsed.path:
        return path_parts[-1]  # extension added later via detect_and_add_extension

    # Repo files: /{owner}/{repo}/files/{id}/{filename}
    elif "/files/" in parsed.path and len(path_parts) >= 2:
        return path_parts[-1]

    # Legacy: user-images.githubusercontent.com/{user}/{hash-with-ext}
    elif "githubusercontent.com" in parsed.netloc:
        return path_parts[-1]  # Already has extension usually

    # Fallback: use last path component
    return path_parts[-1] if path_parts[-1] else "unknown_attachment"


def resolve_filename_collision(filepath):
    """Resolve filename collisions using counter suffix pattern.

    If filepath exists, returns a new filepath with counter suffix.
    Pattern: report.pdf → report_1.pdf → report_2.pdf

    Also protects against manifest.json collisions by treating it as reserved.

    Args:
        filepath: Full path to file that might exist

    Returns:
        filepath that doesn't collide (may be same as input if no collision)
    """
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    # Protect manifest.json - it's a reserved filename
    if filename == "manifest.json":
        name, ext = os.path.splitext(filename)
        counter = 1
        while True:
            new_filename = f"{name}_{counter}{ext}"
            new_filepath = os.path.join(directory, new_filename)
            if not os.path.exists(new_filepath):
                return new_filepath
            counter += 1

    if not os.path.exists(filepath):
        return filepath

    name, ext = os.path.splitext(filename)

    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_filepath = os.path.join(directory, new_filename)
        if not os.path.exists(new_filepath):
            return new_filepath
        counter += 1


def download_attachments(
    args, item_cwd, item_data, number, repository, item_type="issue"
):
    """Download user-attachments from issue/PR body and comments with manifest.

    Args:
        args: Command line arguments
        item_cwd: Working directory (issue_cwd or pulls_cwd)
        item_data: Issue or PR data dict
        number: Issue or PR number
        repository: Repository dict
        item_type: "issue" or "pull" for logging/manifest
    """
    import json
    from datetime import datetime, timezone

    item_type_display = "issue" if item_type == "issue" else "pull request"

    urls = extract_attachment_urls(
        item_data, issue_number=number, repository_full_name=repository["full_name"]
    )
    if not urls:
        return

    attachments_dir = os.path.join(item_cwd, "attachments", str(number))
    manifest_path = os.path.join(attachments_dir, "manifest.json")

    # Load existing manifest to prevent duplicate downloads
    existing_urls = set()
    existing_metadata = []
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r") as f:
                existing_manifest = json.load(f)
                all_metadata = existing_manifest.get("attachments", [])
                # Only skip URLs that were successfully downloaded OR failed with permanent errors
                # Retry transient failures (5xx, timeouts, network errors)
                for item in all_metadata:
                    if item.get("success"):
                        existing_urls.add(item["url"])
                    else:
                        # Check if this is a permanent failure (don't retry) or transient (retry)
                        http_status = item.get("http_status")
                        if http_status in [404, 410, 451]:
                            # Permanent failures - don't retry
                            existing_urls.add(item["url"])
                # Transient failures (5xx, auth errors, timeouts) will be retried
                existing_metadata = all_metadata
        except (json.JSONDecodeError, IOError):
            # If manifest is corrupted, re-download everything
            logger.warning(
                "Corrupted manifest for {0} #{1}, will re-download".format(
                    item_type_display, number
                )
            )
            existing_urls = set()
            existing_metadata = []

    # Filter to only new URLs
    new_urls = [url for url in urls if url not in existing_urls]

    if not new_urls and existing_urls:
        logger.debug(
            "Skipping attachments for {0} #{1} (all {2} already downloaded)".format(
                item_type_display, number, len(urls)
            )
        )
        return

    if new_urls:
        logger.info(
            "Downloading {0} new attachment(s) for {1} #{2}".format(
                len(new_urls), item_type_display, number
            )
        )

    mkdir_p(item_cwd, attachments_dir)

    # Collect metadata for manifest (start with existing)
    attachment_metadata_list = existing_metadata[:]

    for url in new_urls:
        filename = get_attachment_filename(url)
        filepath = os.path.join(attachments_dir, filename)

        # Issue #477: Fine-grained PATs cannot download user-attachments/assets
        # from private repos directly (404). Use Markdown API workaround to get
        # a JWT-signed URL. Only works for /assets/ (images), not /files/.
        needs_jwt = (
            args.token_fine is not None
            and repository.get("private", False)
            and "github.com/user-attachments/assets/" in url
        )

        if not needs_jwt:
            # NORMAL download path
            metadata = download_attachment_file(
                url,
                filepath,
                get_auth(args, encode=not args.as_app),
                as_app=args.as_app,
                fine=args.token_fine is not None,
            )
        elif jwt_url := get_jwt_signed_url_via_markdown_api(
            url, args.token_fine, repository["full_name"]
        ):
            # JWT needed and extracted, download via JWT
            metadata = download_attachment_file(
                jwt_url, filepath, auth=None, as_app=False, fine=False
            )
            metadata["url"] = url  # Apply back the original URL
            metadata["jwt_workaround"] = True
        else:
            # Markdown API workaround failed - skip download we know will fail
            metadata = {
                "url": url,
                "success": False,
                "skipped_at": datetime.now(timezone.utc).isoformat(),
                "error": "Fine-grained token cannot download private repo attachments. "
                "Markdown API workaround failed. Use --token-classic instead.",
            }
            logger.warning(
                "Skipping attachment {0}: {1}".format(url, metadata["error"])
            )

        # If download succeeded but we got an extension from Content-Disposition,
        # we may need to rename the file to add the extension
        if metadata["success"] and metadata.get("original_filename"):
            original_ext = os.path.splitext(metadata["original_filename"])[1]
            current_ext = os.path.splitext(filepath)[1]

            # Add extension if not present
            if original_ext and current_ext != original_ext:
                final_filepath = filepath + original_ext
                # Check for collision again with new extension
                final_filepath = resolve_filename_collision(final_filepath)
                logger.debug(
                    "Adding extension {0} to {1}".format(original_ext, filepath)
                )

                # Rename to add extension (already atomic from download)
                try:
                    os.replace(filepath, final_filepath)
                    metadata["saved_as"] = os.path.basename(final_filepath)
                except Exception as e:
                    logger.warning(
                        "Could not add extension to {0}: {1}".format(filepath, str(e))
                    )
                    metadata["saved_as"] = os.path.basename(filepath)
            else:
                metadata["saved_as"] = os.path.basename(filepath)
        elif metadata["success"]:
            metadata["saved_as"] = os.path.basename(filepath)
        else:
            metadata["saved_as"] = None

        attachment_metadata_list.append(metadata)

    # Write manifest
    if attachment_metadata_list:
        manifest = {
            "issue_number": number,
            "issue_type": item_type,
            "repository": (
                f"{args.user}/{args.repository}"
                if hasattr(args, "repository") and args.repository
                else args.user
            ),
            "manifest_updated_at": datetime.now(timezone.utc).isoformat(),
            "attachments": attachment_metadata_list,
        }

        manifest_path = os.path.join(attachments_dir, "manifest.json")
        with open(manifest_path + ".temp", "w") as f:
            json.dump(manifest, f, indent=2)
        os.replace(manifest_path + ".temp", manifest_path)  # Atomic write
        logger.debug(
            "Wrote manifest for {0} #{1}: {2} attachments".format(
                item_type_display, number, len(attachment_metadata_list)
            )
        )


def get_authenticated_user(args):
    template = "https://{0}/user".format(get_github_api_host(args))
    data = retrieve_data(args, template, paginated=False)
    return data[0]


def check_git_lfs_install():
    exit_code = subprocess.call(["git", "lfs", "version"])
    if exit_code != 0:
        raise Exception(
            "The argument --lfs requires you to have Git LFS installed.\nYou can get it from https://git-lfs.github.com."
        )


def retrieve_repositories(args, authenticated_user):
    logger.info("Retrieving repositories")
    paginated = True
    if args.user == authenticated_user["login"]:
        # we must use the /user/repos API to be able to access private repos
        template = "https://{0}/user/repos".format(get_github_api_host(args))
    else:
        if args.private and not args.organization:
            logger.warning(
                "Authenticated user is different from user being backed up, thus private repositories cannot be accessed"
            )
        template = "https://{0}/users/{1}/repos".format(
            get_github_api_host(args), args.user
        )

    if args.organization:
        template = "https://{0}/orgs/{1}/repos".format(
            get_github_api_host(args), args.user
        )

    if args.repository:
        if "/" in args.repository:
            repo_path = args.repository
        else:
            repo_path = "{0}/{1}".format(args.user, args.repository)
        paginated = False
        template = "https://{0}/repos/{1}".format(get_github_api_host(args), repo_path)

    repos = retrieve_data(args, template, paginated=paginated)

    if args.all_starred:
        starred_template = "https://{0}/users/{1}/starred".format(
            get_github_api_host(args), args.user
        )
        starred_repos = retrieve_data(args, starred_template)
        # flag each repo as starred for downstream processing
        for item in starred_repos:
            item.update({"is_starred": True})
        repos.extend(starred_repos)

    if args.include_gists:
        gists_template = "https://{0}/users/{1}/gists".format(
            get_github_api_host(args), args.user
        )
        gists = retrieve_data(args, gists_template)
        # flag each repo as a gist for downstream processing
        for item in gists:
            item.update({"is_gist": True})
        repos.extend(gists)

    if args.include_starred_gists:
        if (
            not authenticated_user.get("login")
            or args.user.lower() != authenticated_user["login"].lower()
        ):
            logger.warning(
                "Cannot retrieve starred gists for '%s'. GitHub only allows access to the authenticated user's starred gists.",
                args.user,
            )
        else:
            starred_gists_template = "https://{0}/gists/starred".format(
                get_github_api_host(args)
            )
            starred_gists = retrieve_data(args, starred_gists_template)
            # flag each repo as a starred gist for downstream processing
            for item in starred_gists:
                item.update({"is_gist": True, "is_starred": True})
            repos.extend(starred_gists)

    return repos


def filter_repositories(args, unfiltered_repositories):
    if args.repository:
        return unfiltered_repositories
    logger.info("Filtering repositories")

    repositories = []
    for r in unfiltered_repositories:
        # gists can be anonymous, so need to safely check owner
        # Use case-insensitive comparison to match GitHub's case-insensitive username behavior
        owner_login = r.get("owner", {}).get("login", "")
        if owner_login.lower() == args.user.lower() or r.get("is_starred"):
            repositories.append(r)

    name_regex = None
    if args.name_regex:
        name_regex = re.compile(args.name_regex)

    languages = None
    if args.languages:
        languages = [x.lower() for x in args.languages]

    if not args.fork:
        repositories = [r for r in repositories if not r.get("fork")]
    if not args.private:
        repositories = [
            r for r in repositories if not r.get("private") or r.get("public")
        ]
    if languages:
        repositories = [
            r
            for r in repositories
            if r.get("language") and r.get("language").lower() in languages
        ]  # noqa
    if name_regex:
        repositories = [
            r for r in repositories if "name" not in r or name_regex.match(r["name"])
        ]
    if args.skip_archived:
        repositories = [r for r in repositories if not r.get("archived")]
    if args.starred_skip_size_over is not None:
        if args.starred_skip_size_over <= 0:
            logger.warning("--starred-skip-size-over must be greater than 0, ignoring")
        else:
            size_limit_kb = args.starred_skip_size_over * 1024
            filtered = []
            for r in repositories:
                if r.get("is_starred") and r.get("size", 0) > size_limit_kb:
                    size_mb = r.get("size", 0) / 1024
                    logger.info(
                        "Skipping starred repo {0} ({1:.0f} MB) due to --starred-skip-size-over {2}".format(
                            r.get("full_name", r.get("name")),
                            size_mb,
                            args.starred_skip_size_over,
                        )
                    )
                else:
                    filtered.append(r)
            repositories = filtered
    if args.exclude:
        repositories = [
            r for r in repositories if "name" not in r or r["name"] not in args.exclude
        ]

    return repositories


def backup_repositories(args, output_directory, repositories):
    logger.info("Backing up repositories")
    repos_template = "https://{0}/repos".format(get_github_api_host(args))

    if args.incremental:
        last_update_path = os.path.join(output_directory, "last_update")
        if os.path.exists(last_update_path):
            args.since = open(last_update_path).read().strip()
        else:
            args.since = None
    else:
        args.since = None

    last_update = "0000-00-00T00:00:00Z"
    for repository in repositories:
        if "updated_at" in repository and repository["updated_at"] > last_update:
            last_update = repository["updated_at"]
        elif "pushed_at" in repository and repository["pushed_at"] > last_update:
            last_update = repository["pushed_at"]

        if repository.get("is_gist"):
            repo_cwd = os.path.join(output_directory, "gists", repository["id"])
        elif repository.get("is_starred"):
            # put starred repos in -o/starred/${owner}/${repo} to prevent collision of
            # any repositories with the same name
            repo_cwd = os.path.join(
                output_directory,
                "starred",
                repository["owner"]["login"],
                repository["name"],
            )
        else:
            repo_cwd = os.path.join(
                output_directory, "repositories", repository["name"]
            )

        repo_dir = os.path.join(repo_cwd, "repository")
        repo_url = get_github_repo_url(args, repository)

        include_gists = args.include_gists or args.include_starred_gists
        include_starred = args.all_starred and repository.get("is_starred")
        if (
            (args.include_repository or args.include_everything)
            or (include_gists and repository.get("is_gist"))
            or include_starred
        ):
            repo_name = (
                repository.get("name")
                if not repository.get("is_gist")
                else repository.get("id")
            )
            fetch_repository(
                repo_name,
                repo_url,
                repo_dir,
                skip_existing=args.skip_existing,
                bare_clone=args.bare_clone,
                lfs_clone=args.lfs_clone,
                no_prune=args.no_prune,
            )

            if repository.get("is_gist"):
                # dump gist information to a file as well
                output_file = "{0}/gist.json".format(repo_cwd)
                with codecs.open(output_file, "w", encoding="utf-8") as f:
                    json_dump(repository, f)

                continue  # don't try to back anything else for a gist; it doesn't exist

        try:
            download_wiki = args.include_wiki or args.include_everything
            if repository["has_wiki"] and download_wiki:
                fetch_repository(
                    repository["name"],
                    repo_url.replace(".git", ".wiki.git"),
                    os.path.join(repo_cwd, "wiki"),
                    skip_existing=args.skip_existing,
                    bare_clone=args.bare_clone,
                    lfs_clone=args.lfs_clone,
                    no_prune=args.no_prune,
                )
            if args.include_issues or args.include_everything:
                backup_issues(args, repo_cwd, repository, repos_template)

            if args.include_pulls or args.include_everything:
                backup_pulls(args, repo_cwd, repository, repos_template)

            if args.include_milestones or args.include_everything:
                backup_milestones(args, repo_cwd, repository, repos_template)

            if args.include_security_advisories or (args.include_everything and not repository.get("private", False)):
                backup_security_advisories(args, repo_cwd, repository, repos_template)

            if args.include_labels or args.include_everything:
                backup_labels(args, repo_cwd, repository, repos_template)

            if args.include_hooks or args.include_everything:
                backup_hooks(args, repo_cwd, repository, repos_template)

            if args.include_releases or args.include_everything:
                backup_releases(
                    args,
                    repo_cwd,
                    repository,
                    repos_template,
                    include_assets=args.include_assets or args.include_everything,
                )
        except RepositoryUnavailableError as e:
            logger.warning(
                f"Repository {repository['full_name']} is unavailable (HTTP 451)"
            )
            if e.dmca_url:
                logger.warning(f"DMCA notice: {e.dmca_url}")
            logger.info(f"Skipping remaining resources for {repository['full_name']}")
            continue

    if args.incremental:
        if last_update == "0000-00-00T00:00:00Z":
            last_update = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())

        open(last_update_path, "w").write(last_update)


def backup_issues(args, repo_cwd, repository, repos_template):
    has_issues_dir = os.path.isdir("{0}/issues/.git".format(repo_cwd))
    if args.skip_existing and has_issues_dir:
        return

    logger.info("Retrieving {0} issues".format(repository["full_name"]))
    issue_cwd = os.path.join(repo_cwd, "issues")
    mkdir_p(repo_cwd, issue_cwd)

    issues = {}
    issues_skipped = 0
    issues_skipped_message = ""
    _issue_template = "{0}/{1}/issues".format(repos_template, repository["full_name"])

    should_include_pulls = args.include_pulls or args.include_everything
    issue_states = ["open", "closed"]
    for issue_state in issue_states:
        query_args = {"filter": "all", "state": issue_state}
        if args.since:
            query_args["since"] = args.since

        _issues = retrieve_data(args, _issue_template, query_args=query_args)
        for issue in _issues:
            # skip pull requests which are also returned as issues
            # if retrieving pull requests is requested as well
            if "pull_request" in issue and should_include_pulls:
                issues_skipped += 1
                continue

            issues[issue["number"]] = issue

    if issues_skipped:
        issues_skipped_message = " (skipped {0} pull requests)".format(issues_skipped)

    logger.info(
        "Saving {0} issues to disk{1}".format(
            len(list(issues.keys())), issues_skipped_message
        )
    )
    comments_template = _issue_template + "/{0}/comments"
    events_template = _issue_template + "/{0}/events"
    for number, issue in list(issues.items()):
        issue_file = "{0}/{1}.json".format(issue_cwd, number)
        if args.incremental_by_files and os.path.isfile(issue_file):
            modified = os.path.getmtime(issue_file)
            modified = datetime.fromtimestamp(modified).strftime("%Y-%m-%dT%H:%M:%SZ")
            if modified > issue["updated_at"]:
                logger.info(
                    "Skipping issue {0} because it wasn't modified since last backup".format(
                        number
                    )
                )
                continue

        if args.include_issue_comments or args.include_everything:
            template = comments_template.format(number)
            issues[number]["comment_data"] = retrieve_data(args, template)
        if args.include_issue_events or args.include_everything:
            template = events_template.format(number)
            issues[number]["event_data"] = retrieve_data(args, template)
        if args.include_attachments:
            download_attachments(
                args, issue_cwd, issues[number], number, repository, item_type="issue"
            )

        with codecs.open(issue_file + ".temp", "w", encoding="utf-8") as f:
            json_dump(issue, f)
        os.replace(issue_file + ".temp", issue_file)  # Atomic write


def backup_pulls(args, repo_cwd, repository, repos_template):
    has_pulls_dir = os.path.isdir("{0}/pulls/.git".format(repo_cwd))
    if args.skip_existing and has_pulls_dir:
        return

    logger.info("Retrieving {0} pull requests".format(repository["full_name"]))  # noqa
    pulls_cwd = os.path.join(repo_cwd, "pulls")
    mkdir_p(repo_cwd, pulls_cwd)

    pulls = {}
    _pulls_template = "{0}/{1}/pulls".format(repos_template, repository["full_name"])
    _issue_template = "{0}/{1}/issues".format(repos_template, repository["full_name"])
    query_args = {
        "filter": "all",
        "state": "all",
        "sort": "updated",
        "direction": "desc",
    }

    if not args.include_pull_details:
        pull_states = ["open", "closed"]
        for pull_state in pull_states:
            query_args["state"] = pull_state
            _pulls = retrieve_data(args, _pulls_template, query_args=query_args)
            for pull in _pulls:
                if args.since and pull["updated_at"] < args.since:
                    break
                if not args.since or pull["updated_at"] >= args.since:
                    pulls[pull["number"]] = pull
    else:
        _pulls = retrieve_data(args, _pulls_template, query_args=query_args)
        for pull in _pulls:
            if args.since and pull["updated_at"] < args.since:
                break
            if not args.since or pull["updated_at"] >= args.since:
                pulls[pull["number"]] = retrieve_data(
                    args,
                    _pulls_template + "/{}".format(pull["number"]),
                    paginated=False,
                )[0]

    logger.info("Saving {0} pull requests to disk".format(len(list(pulls.keys()))))
    # Comments from pulls API are only _review_ comments
    # regular comments need to be fetched via issue API.
    # For backwards compatibility with versions <= 0.41.0
    # keep name "comment_data" for review comments
    comments_regular_template = _issue_template + "/{0}/comments"
    comments_template = _pulls_template + "/{0}/comments"
    commits_template = _pulls_template + "/{0}/commits"
    for number, pull in list(pulls.items()):
        pull_file = "{0}/{1}.json".format(pulls_cwd, number)
        if args.incremental_by_files and os.path.isfile(pull_file):
            modified = os.path.getmtime(pull_file)
            modified = datetime.fromtimestamp(modified).strftime("%Y-%m-%dT%H:%M:%SZ")
            if modified > pull["updated_at"]:
                logger.info(
                    "Skipping pull request {0} because it wasn't modified since last backup".format(
                        number
                    )
                )
                continue
        if args.include_pull_comments or args.include_everything:
            template = comments_regular_template.format(number)
            pulls[number]["comment_regular_data"] = retrieve_data(args, template)
            template = comments_template.format(number)
            pulls[number]["comment_data"] = retrieve_data(args, template)
        if args.include_pull_commits or args.include_everything:
            template = commits_template.format(number)
            pulls[number]["commit_data"] = retrieve_data(args, template)
        if args.include_attachments:
            download_attachments(
                args, pulls_cwd, pulls[number], number, repository, item_type="pull"
            )

        with codecs.open(pull_file + ".temp", "w", encoding="utf-8") as f:
            json_dump(pull, f)
        os.replace(pull_file + ".temp", pull_file)  # Atomic write


def backup_milestones(args, repo_cwd, repository, repos_template):
    milestone_cwd = os.path.join(repo_cwd, "milestones")
    if args.skip_existing and os.path.isdir(milestone_cwd):
        return

    logger.info("Retrieving {0} milestones".format(repository["full_name"]))
    mkdir_p(repo_cwd, milestone_cwd)

    template = "{0}/{1}/milestones".format(repos_template, repository["full_name"])

    query_args = {"state": "all"}

    _milestones = retrieve_data(args, template, query_args=query_args)

    milestones = {}
    for milestone in _milestones:
        milestones[milestone["number"]] = milestone

    written_count = 0
    for number, milestone in list(milestones.items()):
        milestone_file = "{0}/{1}.json".format(milestone_cwd, number)
        if json_dump_if_changed(milestone, milestone_file):
            written_count += 1

    total = len(milestones)
    if written_count == total:
        logger.info("Saved {0} milestones to disk".format(total))
    elif written_count == 0:
        logger.info("{0} milestones unchanged, skipped write".format(total))
    else:
        logger.info(
            "Saved {0} of {1} milestones to disk ({2} unchanged)".format(
                written_count, total, total - written_count
            )
        )


def backup_security_advisories(args, repo_cwd, repository, repos_template):
    advisory_cwd = os.path.join(repo_cwd, "security-advisories")
    if args.skip_existing and os.path.isdir(advisory_cwd):
        return

    logger.info("Retrieving {0} security advisories".format(repository["full_name"]))

    template = "{0}/{1}/security-advisories".format(
        repos_template, repository["full_name"]
    )

    try:
        _advisories = retrieve_data(args, template)
    except Exception as e:
        if "404" in str(e):
            logger.info("Security advisories are not available for this repository, skipping")
            return
        raise

    mkdir_p(repo_cwd, advisory_cwd)

    advisories = {}
    for advisory in _advisories:
        advisories[advisory["ghsa_id"]] = advisory

    written_count = 0
    for ghsa_id, advisory in list(advisories.items()):
        advisory_file = "{0}/{1}.json".format(advisory_cwd, ghsa_id)
        if json_dump_if_changed(advisory, advisory_file):
            written_count += 1

    total = len(advisories)
    if written_count == total:
        logger.info("Saved {0} security advisories to disk".format(total))
    elif written_count == 0:
        logger.info("{0} security advisories unchanged, skipped write".format(total))
    else:
        logger.info(
            "Saved {0} of {1} security advisories to disk ({2} unchanged)".format(
                written_count, total, total - written_count
            )
        )


def backup_labels(args, repo_cwd, repository, repos_template):
    label_cwd = os.path.join(repo_cwd, "labels")
    output_file = "{0}/labels.json".format(label_cwd)
    template = "{0}/{1}/labels".format(repos_template, repository["full_name"])
    _backup_data(args, "labels", template, output_file, label_cwd)


def backup_hooks(args, repo_cwd, repository, repos_template):
    auth = get_auth(args)
    if not auth:
        logger.info("Skipping hooks since no authentication provided")
        return
    hook_cwd = os.path.join(repo_cwd, "hooks")
    output_file = "{0}/hooks.json".format(hook_cwd)
    template = "{0}/{1}/hooks".format(repos_template, repository["full_name"])
    try:
        _backup_data(args, "hooks", template, output_file, hook_cwd)
    except Exception as e:
        if "404" in str(e):
            logger.info("Unable to read hooks, skipping")
        else:
            raise e


def backup_releases(args, repo_cwd, repository, repos_template, include_assets=False):
    repository_fullname = repository["full_name"]

    # give release files somewhere to live & log intent
    release_cwd = os.path.join(repo_cwd, "releases")
    logger.info("Retrieving {0} releases".format(repository_fullname))
    mkdir_p(repo_cwd, release_cwd)

    query_args = {}

    release_template = "{0}/{1}/releases".format(repos_template, repository_fullname)
    releases = retrieve_data(args, release_template, query_args=query_args)

    if args.skip_prerelease:
        releases = [r for r in releases if not r["prerelease"] and not r["draft"]]

    if args.number_of_latest_releases and args.number_of_latest_releases < len(
        releases
    ):
        releases.sort(
            key=lambda item: datetime.strptime(
                item["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ),
            reverse=True,
        )
        releases = releases[: args.number_of_latest_releases]

    # Check if this repo should skip asset downloads (case-insensitive)
    skip_assets = False
    if include_assets:
        repo_name = repository.get("name", "").lower()
        repo_full_name = repository.get("full_name", "").lower()
        skip_repos = [r.lower() for r in (args.skip_assets_on or [])]
        skip_assets = repo_name in skip_repos or repo_full_name in skip_repos
        if skip_assets:
            logger.info(
                "Skipping assets for {0} ({1} releases) due to --skip-assets-on".format(
                    repository.get("name"), len(releases)
                )
            )

    # for each release, store it
    written_count = 0
    for release in releases:
        release_name = release["tag_name"]
        release_name_safe = release_name.replace("/", "__")
        output_filepath = os.path.join(
            release_cwd, "{0}.json".format(release_name_safe)
        )
        if json_dump_if_changed(release, output_filepath):
            written_count += 1

        if include_assets and not skip_assets:
            assets = retrieve_data(args, release["assets_url"])
            if len(assets) > 0:
                # give release asset files somewhere to live & download them (not including source archives)
                release_assets_cwd = os.path.join(release_cwd, release_name_safe)
                mkdir_p(release_assets_cwd)
                for asset in assets:
                    download_file(
                        asset["url"],
                        os.path.join(release_assets_cwd, asset["name"]),
                        get_auth(args, encode=not args.as_app),
                        as_app=args.as_app,
                        fine=True if args.token_fine is not None else False,
                    )

    # Log the results
    total = len(releases)
    if written_count == total:
        logger.info("Saved {0} releases to disk".format(total))
    elif written_count == 0:
        logger.info("{0} releases unchanged, skipped write".format(total))
    else:
        logger.info(
            "Saved {0} of {1} releases to disk ({2} unchanged)".format(
                written_count, total, total - written_count
            )
        )


def fetch_repository(
    name,
    remote_url,
    local_dir,
    skip_existing=False,
    bare_clone=False,
    lfs_clone=False,
    no_prune=False,
):
    if bare_clone:
        if os.path.exists(local_dir):
            clone_exists = (
                subprocess.check_output(
                    ["git", "rev-parse", "--is-bare-repository"], cwd=local_dir
                )
                == b"true\n"
            )
        else:
            clone_exists = False
    else:
        clone_exists = os.path.exists(os.path.join(local_dir, ".git"))

    if clone_exists and skip_existing:
        return

    masked_remote_url = mask_password(remote_url)

    initialized = subprocess.call(
        "git ls-remote " + remote_url, stdout=FNULL, stderr=FNULL, shell=True
    )
    if initialized == 128:
        if ".wiki.git" in remote_url:
            logger.info(
                "Skipping {0} wiki (wiki is enabled but has no content)".format(name)
            )
        else:
            logger.info(
                "Skipping {0} (repository not accessible - may be empty, private, or credentials invalid)".format(
                    name
                )
            )
        return

    if clone_exists:
        logger.info("Updating {0} in {1}".format(name, local_dir))

        remotes = subprocess.check_output(["git", "remote", "show"], cwd=local_dir)
        remotes = [i.strip() for i in remotes.decode("utf-8").splitlines()]

        if "origin" not in remotes:
            git_command = ["git", "remote", "rm", "origin"]
            logging_subprocess(git_command, cwd=local_dir)
            git_command = ["git", "remote", "add", "origin", remote_url]
            logging_subprocess(git_command, cwd=local_dir)
        else:
            git_command = ["git", "remote", "set-url", "origin", remote_url]
            logging_subprocess(git_command, cwd=local_dir)

        git_command = ["git", "fetch", "--all", "--force", "--tags", "--prune"]
        if no_prune:
            git_command.pop()
        logging_subprocess(git_command, cwd=local_dir)
        if lfs_clone:
            git_command = ["git", "lfs", "fetch", "--all", "--prune"]
            if no_prune:
                git_command.pop()
            logging_subprocess(git_command, cwd=local_dir)
    else:
        logger.info(
            "Cloning {0} repository from {1} to {2}".format(
                name, masked_remote_url, local_dir
            )
        )
        if bare_clone:
            git_command = ["git", "clone", "--mirror", remote_url, local_dir]
            logging_subprocess(git_command)
            if lfs_clone:
                git_command = ["git", "lfs", "fetch", "--all", "--prune"]
                if no_prune:
                    git_command.pop()
                logging_subprocess(git_command, cwd=local_dir)
        else:
            git_command = ["git", "clone", remote_url, local_dir]
            logging_subprocess(git_command)
            if lfs_clone:
                git_command = ["git", "lfs", "fetch", "--all", "--prune"]
                if no_prune:
                    git_command.pop()
                logging_subprocess(git_command, cwd=local_dir)


def backup_account(args, output_directory):
    account_cwd = os.path.join(output_directory, "account")

    if args.include_starred or args.include_everything:
        output_file = "{0}/starred.json".format(account_cwd)
        template = "https://{0}/users/{1}/starred".format(
            get_github_api_host(args), args.user
        )
        _backup_data(args, "starred repositories", template, output_file, account_cwd)

    if args.include_watched or args.include_everything:
        output_file = "{0}/watched.json".format(account_cwd)
        template = "https://{0}/users/{1}/subscriptions".format(
            get_github_api_host(args), args.user
        )
        _backup_data(args, "watched repositories", template, output_file, account_cwd)

    if args.include_followers or args.include_everything:
        output_file = "{0}/followers.json".format(account_cwd)
        template = "https://{0}/users/{1}/followers".format(
            get_github_api_host(args), args.user
        )
        _backup_data(args, "followers", template, output_file, account_cwd)

    if args.include_following or args.include_everything:
        output_file = "{0}/following.json".format(account_cwd)
        template = "https://{0}/users/{1}/following".format(
            get_github_api_host(args), args.user
        )
        _backup_data(args, "following", template, output_file, account_cwd)


def _backup_data(args, name, template, output_file, output_directory):
    skip_existing = args.skip_existing
    if not skip_existing or not os.path.exists(output_file):
        logger.info("Retrieving {0} {1}".format(args.user, name))
        mkdir_p(output_directory)
        data = retrieve_data(args, template)

        if json_dump_if_changed(data, output_file):
            logger.info("Saved {0} {1} to disk".format(len(data), name))
        else:
            logger.info("{0} {1} unchanged, skipped write".format(len(data), name))


def json_dump(data, output_file):
    json.dump(
        data,
        output_file,
        ensure_ascii=False,
        sort_keys=True,
        indent=4,
        separators=(",", ": "),
    )


def json_dump_if_changed(data, output_file_path):
    """
    Write JSON data to file only if content has changed.

    Compares the serialized JSON data with the existing file content
    and only writes if different. This prevents unnecessary file
    modification timestamp updates and disk writes.

    Uses atomic writes (temp file + rename) to prevent corruption
    if the process is interrupted during the write.

    Args:
        data: The data to serialize as JSON
        output_file_path: The path to the output file

    Returns:
        True if file was written (content changed or new file)
        False if write was skipped (content unchanged)
    """
    # Serialize new data with consistent formatting matching json_dump()
    new_content = json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        indent=4,
        separators=(",", ": "),
    )

    # Check if file exists and compare content
    if os.path.exists(output_file_path):
        try:
            with codecs.open(output_file_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
            if existing_content == new_content:
                logger.debug(
                    "Content unchanged, skipping write: {0}".format(output_file_path)
                )
                return False
        except (OSError, UnicodeDecodeError) as e:
            # If we can't read the existing file, write the new one
            logger.debug(
                "Error reading existing file {0}, will overwrite: {1}".format(
                    output_file_path, e
                )
            )

    # Write the file atomically using temp file + rename
    temp_file = output_file_path + ".temp"
    with codecs.open(temp_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    os.replace(temp_file, output_file_path)  # Atomic write
    return True

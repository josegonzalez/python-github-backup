#!/usr/bin/env python
"""Command-line interface for github-backup."""

import logging
import os
import sys
from datetime import datetime, timedelta
import threading
import pause

from github_backup.github_backup import (
    backup_account,
    backup_repositories,
    check_git_lfs_install,
    filter_repositories,
    get_app_installation_token,
    get_auth,
    get_authenticated_user,
    logger,
    mkdir_p,
    parse_args,
    retrieve_repositories,
    FILE_URI_PREFIX
)

# INFO and DEBUG go to stdout, WARNING and above go to stderr
log_format = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda r: r.levelno < logging.WARNING)
stdout_handler.setFormatter(log_format)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.setFormatter(log_format)

logging.basicConfig(level=logging.INFO, handlers=[stdout_handler, stderr_handler])

# In minutes
app_installation_token_refresh_interval = 55

def main():
    """Main entry point for github-backup CLI."""
    args = parse_args()
    
    # Issue #477: Fine-grained PATs cannot download all attachment types from
    # private repos. Image attachments will be retried via Markdown API workaround.
    if args.include_attachments and args.token_fine:
        logger.warning(
            "Using --attachments with fine-grained token. Due to GitHub platform "
            "limitations, file attachments (PDFs, etc.) from private repos may fail. "
            "Image attachments will be retried via workaround. For full attachment "
            "support, use --token-classic instead."
        )

    if args.quiet:
        logger.setLevel(logging.WARNING)

    output_directory = os.path.realpath(args.output_directory)
    if not os.path.isdir(output_directory):
        logger.info("Create output directory {0}".format(output_directory))
        mkdir_p(output_directory)

    if args.lfs_clone:
        check_git_lfs_install()

    if args.log_level:
        log_level = logging.getLevelName(args.log_level.upper())
        if isinstance(log_level, int):
            logger.root.setLevel(log_level)

    def refresh_app_installation_token(args):
        while True:
            refresh_time = datetime.now() + timedelta(minutes=app_installation_token_refresh_interval)
            logger.info("App installation token refresh time: " + str(refresh_time))
            pause.until(refresh_time)
            logger.info("Refreshing app installation token")
            args.token_classic = get_app_installation_token(
                app_id=args.app_id,
                installation_id=args.app_installation_id,
                installation_secret=args.app_installation_secret
            )
    
    if args.as_app_dynamic_token:
        if not (args.app_id and args.app_installation_id and args.app_installation_secret):
            raise Exception(
                "Arguments --app-id, --app-installation-id and --app-installation-secret must be set for --as-app-dynamic-token."
            )
        if args.include_gists:
            logger.warning(
                "Downloading gists with an app installation token doesn't work. "
                "Disabling --gists option."
            )
            args.include_gists = False
        if args.app_installation_secret.startswith(FILE_URI_PREFIX):
            secret_path = args.app_installation_secret.removeprefix(FILE_URI_PREFIX)
            with open(secret_path) as f:
                args.app_installation_secret = f.read()
        args.token_classic = get_app_installation_token(
            app_id=args.app_id,
            installation_id=args.app_installation_id,
            installation_secret=args.app_installation_secret
        )
        args.as_app = True
        refresh_app_installation_token_thread = threading.Thread(
            target=refresh_app_installation_token,
            args=(args,),
            daemon=True
        )
        refresh_app_installation_token_thread.start()
    
    if args.private and not get_auth(args):
        logger.warning(
            "The --private flag has no effect without authentication. "
            "Use -t/--token or -f/--token-fine to authenticate."
        )

    if not args.as_app:
        logger.info("Backing up user {0} to {1}".format(args.user, output_directory))
        authenticated_user = get_authenticated_user(args)
    else:
        authenticated_user = {"login": None}

    repositories = retrieve_repositories(args, authenticated_user)
    repositories = filter_repositories(args, repositories)
    backup_repositories(args, output_directory, repositories)
    backup_account(args, output_directory, authenticated_user)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

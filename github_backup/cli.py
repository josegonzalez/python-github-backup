#!/usr/bin/env python
"""Command-line interface for github-backup."""

import logging
import os
import sys

from github_backup.github_backup import (
    backup_account,
    backup_repositories,
    check_git_lfs_install,
    filter_repositories,
    get_auth,
    get_authenticated_user,
    logger,
    mkdir_p,
    parse_args,
    retrieve_repositories,
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


def main():
    """Main entry point for github-backup CLI."""
    args = parse_args()

    if args.private and not get_auth(args):
        logger.warning(
            "The --private flag has no effect without authentication. "
            "Use -t/--token or -f/--token-fine to authenticate."
        )

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

    if not args.as_app:
        logger.info("Backing up user {0} to {1}".format(args.user, output_directory))
        authenticated_user = get_authenticated_user(args)
    else:
        authenticated_user = {"login": None}

    repositories = retrieve_repositories(args, authenticated_user)
    repositories = filter_repositories(args, repositories)
    backup_repositories(args, output_directory, repositories)
    backup_account(args, output_directory)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

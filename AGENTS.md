# AGENTS.md

Guidance for AI coding agents, and anyone else, contributing to python-github-backup. Read the Development section of `README.rst` and `.github/PULL_REQUEST.md` first. The project is maintained on a best-effort basis, so keep pull requests small and focused.

## Project

- A command line tool that backs up GitHub users and organizations: repositories, wikis and gists as git clones, and metadata (issues, pull requests, discussions, comments, releases and so on) as JSON.
- Most code is in `github_backup/github_backup.py`. GraphQL queries go in `github_backup/graphql_queries.py`.

## Setup, tests and lint

```
pip install -r release-requirements.txt
pytest
flake8 --ignore=E501,E203,W503
```

These match CI (`.github/workflows/test.yml` and `lint.yml`). Fix any test or lint failures before asking for review.

## What reviewers look for

The maintainer's test for a change: it is simple to read and understand, follows the patterns already in the codebase, and doesn't break existing functionality.

- **Use the standard library.** Don't add packages: `requirements.txt` is empty and the project has always worked without them. If an outside tool is needed, shell out to one, as the code already does for `git`, `gh` and `openssl`.
- **Follow existing patterns.** Pass options through `args`, not module-level globals or new modules. Find how a similar case is already handled and do the same.
- **Keep the diff minimal.** Don't reformat or refactor code the change doesn't need; it makes review harder.
- **Keep existing backups unchanged.** Don't change the structure of saved JSON, file names or directory layout for existing data unless that is the point of the change; people keep years of backups and read them with their own tools. Handle a new case alongside the existing behaviour rather than replacing it.
- **Keep incremental runs incremental.** A change that makes `--incremental` re-fetch everything is a regression, even if the output is correct.
- **Skip rather than save wrong data.** When something can't be backed up, warn and skip rather than crash, and never save data that belongs to someone else. Treat a 404 on an optional resource (pull requests disabled, no admin access to hooks) as "not available": log it and skip. Let other errors raise.
- **Fail early on setup problems.** Check missing files, tools or conflicting options in `parse_args` with `parser.error`, before any work starts.
- **Keep it working without a token** where it works today; the GraphQL API requires authentication.
- **Document new or changed command line options** in `README.rst`.

## Tests

- Add tests for new behaviour and bug fixes, sized to the change; a one-line fix doesn't need ninety lines of tests.
- For a bug fix, include a test that fails without the fix and passes with it.
- Build `args` with the `create_args` fixture from `tests/conftest.py`, so tests pick up new options with their defaults.

## Pull requests and commits

- **Search existing issues and pull requests first.** Earlier discussion often explains why something works the way it does, or records an approach that was already tried. If an open pull request already covers the change, build on it rather than opening a competing one.
- **Open an issue first for larger changes.** A pull request without an issue is welcome, but if the change is large or could be solved more than one way, discuss the approach in an issue to avoid rework. Reference any related issue (`Fixes #123`).
- **Keep to one feature or fix per pull request.** Large multi-feature pull requests get asked to be split up.
- **Rebase on `master`** if your branch falls behind.
- **Run it live if you can.** Run a backup that exercises the change and an ordinary backup with common options, then describe both in the pull request, including anything you couldn't test. Not required, but it helps most when reviewers can't reproduce your setup, such as GitHub App authentication or an organization with particular settings.
- **Write for readers who weren't in your session.** Don't put links to agent sessions (for example `claude.ai/code/session_...`) or private trackers in commits or pull requests, or refer to your conversation or prompts; put the context the reader needs in the pull request itself.
- **Credit earlier work.** If your change builds on or replaces someone else's pull request, link it and credit them.
- **Don't edit `CHANGES.rst` or the version number.** The changelog is generated from commit messages at release time, so write a short imperative subject and a body that explains what changed and why.

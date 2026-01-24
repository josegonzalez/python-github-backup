Changelog
=========

0.61.3 (2026-01-24)
-------------------
------------------------
- Fix KeyError: 'Private' when using --all flag (#481) [Rodos]

  The repository dictionary uses lowercase "private" key. Use .get() with
  the correct case to match the pattern used elsewhere in the codebase.

  The bug only affects --all users since --security-advisories short-circuits
  before the key access.
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 80.9.0 to 80.10.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.9.0...v80.10.1)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 80.10.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...


0.61.2 (2026-01-19)
-------------------

Fix
~~~
- Skip security advisories for private repos unless explicitly
  requested. [Lukas Bestle]
- Handle 404 errors on security advisories. [Lukas Bestle]

Other
~~~~~
- Chore(deps): bump black in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 25.12.0 to 26.1.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.12.0...26.1.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 26.1.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Docs: Explain security advisories in README. [Lukas Bestle]
- Feat: Only make security advisory dir if successful. [Lukas Bestle]

  Avoids empty directories for private repos


0.61.1 (2026-01-13)
-------------------
- Refactor test fixtures to use shared create_args helper. [Rodos]

  Uses the real parse_args() function to get CLI defaults, so when
  new arguments are added they're automatically available to all tests.

  Changes:
  - Add tests/conftest.py with create_args fixture
  - Update 8 test files to use shared fixture
  - Remove duplicate _create_mock_args methods
  - Remove redundant @pytest.fixture mock_args definitions

  This eliminates the need to update multiple test files when
  adding new CLI arguments.
- Fix fine-grained PAT attachment downloads for private repos (#477)
  [Rodos]

  Fine-grained personal access tokens cannot download attachments from
  private repositories directly due to a GitHub platform limitation.

  This adds a workaround for image attachments (/assets/ URLs) using
  GitHub's Markdown API to convert URLs to JWT-signed URLs that can be
  downloaded without authentication.

  Changes:
  - Add get_jwt_signed_url_via_markdown_api() function
  - Detect fine-grained token + private repo + /assets/ URL upfront
  - Use JWT workaround for those cases, mark success with jwt_workaround flag
  - Skip download with skipped_at when workaround fails
  - Add startup warning when using --attachments with fine-grained tokens
  - Document limitation in README (file attachments still fail)
  - Add 6 unit tests for JWT workaround logic


0.61.0 (2026-01-12)
-------------------
- Docs: Add missing `--retries` argument to README. [Lukas Bestle]
- Test: Adapt tests to new argument. [Lukas Bestle]
- Feat: Backup of repository security advisories. [Lukas Bestle]


0.60.0 (2025-12-24)
-------------------
- Rm max_retries.py. [michaelmartinez]
- Readme. [michaelmartinez]
- Don't use a global variable, pass the args instead. [michaelmartinez]
- Readme, simplify the logic a bit. [michaelmartinez]
- Max_retries 5. [michaelmartinez]


0.59.0 (2025-12-21)
-------------------
- Add --starred-skip-size-over flag to limit starred repo size (#108)
  [Rodos]

  Allow users to skip starred repositories exceeding a size threshold
  when using --all-starred. Size is specified in MB and checked against
  the GitHub API's repository size field.

  - Only affects starred repos; user's own repos always included
  - Logs each skipped repo with name and size

  Closes #108
- Chore: remove deprecated -u/-p password authentication options.
  [Rodos]


0.58.0 (2025-12-16)
-------------------
- Fix retry logic for HTTP 5xx errors and network failures. [Rodos]

  Refactors error handling to retry all 5xx errors (not just 502), network errors (URLError, socket.error, IncompleteRead), and JSON parse errors with exponential backoff and jitter. Respects retry-after and rate limit headers per GitHub API requirements. Consolidates retry logic into make_request_with_retry() wrapper and adds clear logging for retry attempts and failures. Removes dead code from 2016 (errors list, _request_http_error, _request_url_error) that was intentionally disabled in commit 1e5a9048 to fix #29.

  Fixes #140, #110, #138
- Chore: remove transitive deps from release-requirements.txt. [Rodos]
- Chore(deps): bump urllib3 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.6.1 to 2.6.2
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.6.1...2.6.2)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.57.0 (2025-12-12)
-------------------
- Add GitHub Apps documentation and remove outdated header. [Rodos]

  - Add GitHub Apps authentication section with setup steps
    and CI/CD workflow example using actions/create-github-app-token
  - Remove outdated machine-man-preview header (graduated 2020)

  Closes #189
- Docs: add stdin token example to README. [Rodos]

  Add example showing how to pipe a token from stdin using
  file:///dev/stdin to avoid storing tokens in environment
  variables or command history.

  Closes #187
- Add --skip-assets-on flag to skip release asset downloads (#135)
  [Rodos]

  Allow users to skip downloading release assets for specific repositories
  while still backing up release metadata. Useful for starred repos with
  large assets (e.g. syncthing with 27GB+).

  Usage: --skip-assets-on repo1 repo2 owner/repo3

  Features:
  - Space-separated repos (consistent with --exclude)
  - Case-insensitive matching
  - Supports both repo name and owner/repo format


0.56.0 (2025-12-11)
-------------------

Fix
~~~
- Replace deprecated git lfs clone with git clone + git lfs fetch --all.
  [Rodos]

  git lfs clone is deprecated - modern git clone handles LFS automatically.
  Using git lfs fetch --all ensures all LFS objects across all refs are
  backed up, matching the existing bare clone behavior and providing
  complete LFS backups.

  Closes #379
- Add Windows support with entry_points and os.replace. [Rodos]

  - Replace os.rename() with os.replace() for atomic file operations
    on Windows (os.rename fails if destination exists on Windows)
  - Add entry_points console_scripts for proper .exe generation on Windows
  - Create github_backup/cli.py with main() entry point
  - Add github_backup/__main__.py for python -m github_backup support
  - Keep bin/github-backup as thin wrapper for backwards compatibility

  Closes #112

Other
~~~~~
- Docs: add "Restoring from Backup" section to README. [Rodos]

  Clarifies that this tool is backup-only with no inbuilt restore.
  Documents that git repos can be pushed back, but issues/PRs have
  GitHub API limitations affecting all backup tools.

  Closes #246
- Chore(deps): bump urllib3 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.6.0 to 2.6.1
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.6.0...2.6.1)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [black](https://github.com/psf/black), [pytest](https://github.com/pytest-dev/pytest) and [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `black` from 25.11.0 to 25.12.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.11.0...25.12.0)

  Updates `pytest` from 9.0.1 to 9.0.2
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/9.0.1...9.0.2)

  Updates `platformdirs` from 4.5.0 to 4.5.1
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.5.0...4.5.1)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 25.12.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pytest
    dependency-version: 9.0.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-version: 4.5.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.55.0 (2025-12-07)
-------------------

Fix
~~~
- Improve error messages for inaccessible repos and empty wikis. [Rodos]
- --all-starred now clones repos without --repositories. [Rodos]
- Warn when --private used without authentication. [Rodos]
- Warn and skip when --starred-gists used for different user. [Rodos]

  GitHub's API only allows retrieving starred gists for the authenticated
  user. Previously, using --starred-gists when backing up a different user
  would silently return no relevant data.

  Now warns and skips the retrieval entirely when the target user differs
  from the authenticated user. Uses case-insensitive comparison to match
  GitHub's username handling.

  Fixes #93

Other
~~~~~
- Test: add missing test coverage for case sensitivity fix. [Rodos]
- Docs: fix RST formatting in Known blocking errors section. [Rodos]
- Chore(deps): bump urllib3 from 2.5.0 to 2.6.0. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.5.0 to 2.6.0.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.5.0...2.6.0)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.0
    dependency-type: direct:production
  ...


0.54.0 (2025-12-03)
-------------------

Fix
~~~
- Send INFO/DEBUG to stdout, WARNING/ERROR to stderr. [Rodos]

  Fixes #182

Other
~~~~~
- Docs: update README testing section and add fetch vs pull explanation.
  [Rodos]


0.53.0 (2025-11-30)
-------------------

Fix
~~~
- Case-sensitive username filtering causing silent backup failures.
  [Rodos]

  GitHub's API accepts usernames in any case but returns canonical case.
  The case-sensitive comparison in filter_repositories() filtered out all
  repositories when user-provided case didn't match GitHub's canonical case.

  Changed to case-insensitive comparison.

  Fixes #198

Other
~~~~~
- Avoid rewriting unchanged JSON files for labels, milestones, releases,
  hooks, followers, and following. [Rodos]

  This change reduces unnecessary writes when backing up metadata that changes
  infrequently. The implementation compares existing file content before writing
  and skips the write if the content is identical, preserving file timestamps.

  Key changes:
  - Added json_dump_if_changed() helper that compares content before writing
  - Uses atomic writes (temp file + rename) for all metadata files
  - NOT applied to issues/pulls (they use incremental_by_files logic)
  - Made log messages consistent and past tense ("Saved" instead of "Saving")
  - Added informative logging showing skip counts

  Fixes #133


0.52.0 (2025-11-28)
-------------------
- Skip DMCA'd repos which return a 451 response. [Rodos]

  Log a warning and the link to the DMCA notice. Continue backing up
  other repositories instead of crashing.

  Closes #163
- Chore(deps): bump restructuredtext-lint in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [restructuredtext-lint](https://github.com/twolfson/restructuredtext-lint).


  Updates `restructuredtext-lint` from 1.4.0 to 2.0.2
  - [Changelog](https://github.com/twolfson/restructuredtext-lint/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/twolfson/restructuredtext-lint/compare/1.4.0...2.0.2)

  ---
  updated-dependencies:
  - dependency-name: restructuredtext-lint
    dependency-version: 2.0.2
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump actions/checkout from 5 to 6. [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 5 to 6.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [click](https://github.com/pallets/click), [pytest](https://github.com/pytest-dev/pytest) and [keyring](https://github.com/jaraco/keyring).


  Updates `click` from 8.3.0 to 8.3.1
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.3.0...8.3.1)

  Updates `pytest` from 8.3.3 to 9.0.1
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/8.3.3...9.0.1)

  Updates `keyring` from 25.6.0 to 25.7.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v25.6.0...v25.7.0)

  ---
  updated-dependencies:
  - dependency-name: click
    dependency-version: 8.3.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: pytest
    dependency-version: 9.0.1
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-version: 25.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...


0.51.3 (2025-11-18)
-------------------
- Test: Add pagination tests for cursor and page-based Link headers.
  [Rodos]
- Use cursor based pagination. [Helio Machado]


0.51.2 (2025-11-16)
-------------------

Fix
~~~
- Improve CA certificate detection with fallback chain. [Rodos]

  The previous implementation incorrectly assumed empty get_ca_certs()
  meant broken SSL, causing false failures in GitHub Codespaces and other
  directory-based cert systems where certificates exist but aren't pre-loaded.
  It would then attempt to import certifi as a workaround, but certifi wasn't
  listed in requirements.txt, causing the fallback to fail with ImportError
  even though the system certificates would have worked fine.

  This commit replaces the naive check with a layered fallback approach that
  checks multiple certificate sources. First it checks for pre-loaded system
  certs (file-based systems). Then it verifies system cert paths exist
  (directory-based systems like Ubuntu/Debian/Codespaces). Finally it attempts
  to use certifi as an optional fallback only if needed.

  This approach eliminates hard dependencies (certifi is now optional), works
  in GitHub Codespaces without any setup, and fails gracefully with clear hints
  for resolution when SSL is actually broken rather than failing with
  ModuleNotFoundError.

  Fixes #444


0.51.1 (2025-11-16)
-------------------

Fix
~~~
- Prevent duplicate attachment downloads. [Rodos]

  Fixes bug where attachments were downloaded multiple times with
  incremented filenames (file.mov, file_1.mov, file_2.mov) when
  running backups without --skip-existing flag.

  I should not have used the --skip-existing flag for attachments,
  it did not do what I thought it did.

  The correct approach is to always use the manifest to guide what
  has already been downloaded and what now needs to be done.

Other
~~~~~
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2025.10.5 to 2025.11.12
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.10.05...2025.11.12)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.11.12
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Test: Add pytest infrastructure and attachment tests. [Rodos]

  In making my last fix to attachments, I found it challenging not
  having tests to ensure there was no regression.

  Added pytest with minimal setup and isolated configuration. Created
  a separate test workflow to keep tests isolated from linting.

  Tests cover the key elements of the attachment logic:
  - URL extraction from issue bodies
  - Filename extraction from different URL types
  - Filename collision resolution
  - Manifest duplicate prevention
- Chore(deps): bump black in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 25.9.0 to 25.11.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.9.0...25.11.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 25.11.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump docutils in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [docutils](https://github.com/rtfd/recommonmark).


  Updates `docutils` from 0.22.2 to 0.22.3
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  ---
  updated-dependencies:
  - dependency-name: docutils
    dependency-version: 0.22.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.51.0 (2025-11-06)
-------------------

Fix
~~~
- Remove Python 3.8 and 3.9 from CI matrix. [Rodos]

  3.8 and 3.9 are failing because the pinned dependencies don't support them:
  - autopep8==2.3.2 needs Python 3.9+
  - bleach==6.3.0 needs Python 3.10+

  Both are EOL now anyway (3.8 in Oct 2024, 3.9 in Oct 2025).

  Just fixing CI to test 3.10-3.14 for now. Will do a separate PR to formally
  drop 3.8/3.9 support with python_requires and README updates.

Other
~~~~~
- Refactor: Add atomic writes for attachment files and manifests.
  [Rodos]
- Feat: Add attachment download support for issues and pull requests.
  [Rodos]

  Adds new --attachments flag that downloads user-uploaded files from
  issue and PR bodies and comments. Key features:

  - Determines attachment URLs
  - Tracks downloads in manifest.json with metadata
  - Supports --skip-existing to avoid re-downloading
  - Handles filename collisions with counter suffix
  - Smart retry logic for transient vs permanent failures
  - Uses Content-Disposition for correct file extensions
- Feat: Drop support for Python 3.8 and 3.9 (EOL) [Rodos]

  Both Python 3.8 and 3.9 have reached end-of-life:
  - Python 3.8: EOL October 7, 2024
  - Python 3.9: EOL October 31, 2025

  Changes:
  - Add python_requires=">=3.10" to setup.py
  - Remove Python 3.8 and 3.9 from classifiers
  - Add Python 3.13 and 3.14 to classifiers
  - Update README to document Python 3.10+ requirement
- Feat: Enforce Python 3.8+ requirement and add multi-version CI
  testing. [Rodos]

  - Add python_requires=">=3.8" to setup.py to enforce minimum version at install time
  - Update README to explicitly document Python 3.8+ requirement
  - Add CI matrix to test lint/build on Python 3.8-3.14 (7 versions)
  - Aligns with actual usage patterns (~99% of downloads on Python 3.8+)
  - Prevents future PRs from inadvertently using incompatible syntax

  This change protects users by preventing installation on unsupported Python
  versions and ensures contributors can see version requirements clearly.
- Chore(deps): bump bleach in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [bleach](https://github.com/mozilla/bleach).


  Updates `bleach` from 6.2.0 to 6.3.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.2.0...v6.3.0)

  ---
  updated-dependencies:
  - dependency-name: bleach
    dependency-version: 6.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump charset-normalizer in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [charset-normalizer](https://github.com/jawah/charset_normalizer).


  Updates `charset-normalizer` from 3.4.3 to 3.4.4
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.3...3.4.4)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-version: 3.4.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump idna from 3.10 to 3.11 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [idna](https://github.com/kjd/idna).


  Updates `idna` from 3.10 to 3.11
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.10...v3.11)

  ---
  updated-dependencies:
  - dependency-name: idna
    dependency-version: '3.11'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [platformdirs](https://github.com/tox-dev/platformdirs) and [rich](https://github.com/Textualize/rich).


  Updates `platformdirs` from 4.4.0 to 4.5.0
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.4.0...4.5.0)

  Updates `rich` from 14.1.0 to 14.2.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.1.0...v14.2.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.5.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-version: 14.2.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [certifi](https://github.com/certifi/python-certifi), [click](https://github.com/pallets/click) and [markdown-it-py](https://github.com/executablebooks/markdown-it-py).


  Updates `certifi` from 2025.8.3 to 2025.10.5
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.08.03...2025.10.05)

  Updates `click` from 8.1.8 to 8.3.0
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.1.8...8.3.0)

  Updates `markdown-it-py` from 3.0.0 to 4.0.0
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v3.0.0...v4.0.0)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.10.5
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: click
    dependency-version: 8.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: markdown-it-py
    dependency-version: 4.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump docutils in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [docutils](https://github.com/rtfd/recommonmark).


  Updates `docutils` from 0.22.1 to 0.22.2
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  ---
  updated-dependencies:
  - dependency-name: docutils
    dependency-version: 0.22.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [black](https://github.com/psf/black) and [docutils](https://github.com/rtfd/recommonmark).


  Updates `black` from 25.1.0 to 25.9.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.1.0...25.9.0)

  Updates `docutils` from 0.22 to 0.22.1
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 25.9.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: docutils
    dependency-version: 0.22.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Delete .github/ISSUE_TEMPLATE.md. [Jose Diaz-Gonzalez]
- Create feature.yaml. [Jose Diaz-Gonzalez]
- Delete .github/ISSUE_TEMPLATE/bug_report.md. [Jose Diaz-Gonzalez]
- Rename bug.md to bug.yaml. [Jose Diaz-Gonzalez]
- Chore: create bug template. [Jose Diaz-Gonzalez]
- Chore: Rename PULL_REQUEST.md to .github/PULL_REQUEST.md. [Jose Diaz-
  Gonzalez]
- Chore: Rename ISSUE_TEMPLATE.md to .github/ISSUE_TEMPLATE.md. [Jose
  Diaz-Gonzalez]
- Chore(deps): bump actions/setup-python from 5 to 6. [dependabot[bot]]

  Bumps [actions/setup-python](https://github.com/actions/setup-python) from 5 to 6.
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: actions/setup-python
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Chore(deps): bump twine from 6.1.0 to 6.2.0 in the python-packages
  group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [twine](https://github.com/pypa/twine).


  Updates `twine` from 6.1.0 to 6.2.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/6.1.0...6.2.0)

  ---
  updated-dependencies:
  - dependency-name: twine
    dependency-version: 6.2.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump more-itertools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [more-itertools](https://github.com/more-itertools/more-itertools).


  Updates `more-itertools` from 10.7.0 to 10.8.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.7.0...v10.8.0)

  ---
  updated-dependencies:
  - dependency-name: more-itertools
    dependency-version: 10.8.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump platformdirs in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `platformdirs` from 4.3.8 to 4.4.0
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.3.8...4.4.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump actions/checkout from 4 to 5. [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 5.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v4...v5)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-version: '5'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Chore(deps): bump requests in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [requests](https://github.com/psf/requests).


  Updates `requests` from 2.32.4 to 2.32.5
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.4...v2.32.5)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.32.5
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore: update Dockerfile to use Python 3.12 and improve dependency
  installation. [Mateusz Hajder]
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [certifi](https://github.com/certifi/python-certifi) and [charset-normalizer](https://github.com/jawah/charset_normalizer).


  Updates `certifi` from 2025.7.14 to 2025.8.3
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.07.14...2025.08.03)

  Updates `charset-normalizer` from 3.4.2 to 3.4.3
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.2...3.4.3)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.8.3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-version: 3.4.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.50.3 (2025-08-08)
-------------------
- Revert "Add conditional check for git checkout in development path"
  [Eric Wheeler]

  This reverts commit 1bad563e3f23d3d8b9f98721d857a660692f4847.
- Fix -R flag to allow backups of repositories not owned by user. [Eric
  Wheeler]

  Previously, using -R flag would show zero issues/PRs for repositories
  not owned by the primary user due to incorrect pagination parameters
  being added to single repository API calls.

  - Remove pagination parameters for single repository requests
  - Support owner/repo format in -R flag (e.g., -R owner/repo-name)
  - Skip filtering when specific repository is requested
  - Fix URL construction for requests without query parameters

  This enables backing up any repository, not just those owned by the
  primary user specified in -u flag.
- Add conditional check for git checkout in development path. [Eric
  Wheeler]

  Only insert development path into sys.path when running from a git checkout
  (when ../.git exists). This makes the script more robust by only using the
  development tree when available and falling back to installed package otherwise.
- Chore(deps): bump the python-packages group across 1 directory with 3
  updates. [dependabot[bot]]

  Bumps the python-packages group with 3 updates in the / directory: [certifi](https://github.com/certifi/python-certifi), [docutils](https://github.com/rtfd/recommonmark) and [rich](https://github.com/Textualize/rich).


  Updates `certifi` from 2025.7.9 to 2025.7.14
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.07.09...2025.07.14)

  Updates `docutils` from 0.21.2 to 0.22
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  Updates `rich` from 14.0.0 to 14.1.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.0.0...v14.1.0)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.7.14
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: docutils
    dependency-version: '0.22'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-version: 14.1.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2025.6.15 to 2025.7.9
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.06.15...2025.07.09)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.7.9
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 from 2.4.0 to 2.5.0. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.4.0 to 2.5.0.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.4.0...2.5.0)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.5.0
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group with 5 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 5 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [flake8](https://github.com/pycqa/flake8) | `7.2.0` | `7.3.0` |
  | [pycodestyle](https://github.com/PyCQA/pycodestyle) | `2.13.0` | `2.14.0` |
  | [pyflakes](https://github.com/PyCQA/pyflakes) | `3.3.2` | `3.4.0` |
  | [pygments](https://github.com/pygments/pygments) | `2.19.1` | `2.19.2` |
  | [urllib3](https://github.com/urllib3/urllib3) | `2.4.0` | `2.5.0` |


  Updates `flake8` from 7.2.0 to 7.3.0
  - [Commits](https://github.com/pycqa/flake8/compare/7.2.0...7.3.0)

  Updates `pycodestyle` from 2.13.0 to 2.14.0
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.13.0...2.14.0)

  Updates `pyflakes` from 3.3.2 to 3.4.0
  - [Changelog](https://github.com/PyCQA/pyflakes/blob/main/NEWS.rst)
  - [Commits](https://github.com/PyCQA/pyflakes/compare/3.3.2...3.4.0)

  Updates `pygments` from 2.19.1 to 2.19.2
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.19.1...2.19.2)

  Updates `urllib3` from 2.4.0 to 2.5.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.4.0...2.5.0)

  ---
  updated-dependencies:
  - dependency-name: flake8
    dependency-version: 7.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-version: 2.14.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pyflakes
    dependency-version: 3.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pygments
    dependency-version: 2.19.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-version: 2.5.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...


0.50.2 (2025-06-16)
-------------------
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2025.4.26 to 2025.6.15
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.04.26...2025.06.15)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.6.15
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump requests from 2.32.3 to 2.32.4. [dependabot[bot]]

  Bumps [requests](https://github.com/psf/requests) from 2.32.3 to 2.32.4.
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.3...v2.32.4)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.32.4
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [requests](https://github.com/psf/requests) and [zipp](https://github.com/jaraco/zipp).


  Updates `requests` from 2.32.3 to 2.32.4
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.3...v2.32.4)

  Updates `zipp` from 3.22.0 to 3.23.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.22.0...v3.23.0)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.32.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-version: 3.23.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [setuptools](https://github.com/pypa/setuptools) and [zipp](https://github.com/jaraco/zipp).


  Updates `setuptools` from 80.8.0 to 80.9.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.8.0...v80.9.0)

  Updates `zipp` from 3.21.0 to 3.22.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.21.0...v3.22.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 80.9.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-version: 3.22.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 80.4.0 to 80.8.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.4.0...v80.8.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 80.8.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 80.3.1 to 80.4.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.3.1...v80.4.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 80.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 3
  updates. [dependabot[bot]]

  Bumps the python-packages group with 3 updates in the / directory: [charset-normalizer](https://github.com/jawah/charset_normalizer), [platformdirs](https://github.com/tox-dev/platformdirs) and [setuptools](https://github.com/pypa/setuptools).


  Updates `charset-normalizer` from 3.4.1 to 3.4.2
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.1...3.4.2)

  Updates `platformdirs` from 4.3.7 to 4.3.8
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.3.7...4.3.8)

  Updates `setuptools` from 80.0.0 to 80.3.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.0.0...v80.3.1)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-version: 3.4.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-version: 4.3.8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 80.3.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 6
  updates. [dependabot[bot]]

  Bumps the python-packages group with 6 updates in the / directory:

  | Package | From | To |
  | --- | --- | --- |
  | [certifi](https://github.com/certifi/python-certifi) | `2025.1.31` | `2025.4.26` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `8.6.1` | `8.7.0` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.6.0` | `10.7.0` |
  | [mypy-extensions](https://github.com/python/mypy_extensions) | `1.0.0` | `1.1.0` |
  | [packaging](https://github.com/pypa/packaging) | `24.2` | `25.0` |
  | [setuptools](https://github.com/pypa/setuptools) | `78.1.0` | `80.0.0` |



  Updates `certifi` from 2025.1.31 to 2025.4.26
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.01.31...2025.04.26)

  Updates `importlib-metadata` from 8.6.1 to 8.7.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v8.6.1...v8.7.0)

  Updates `more-itertools` from 10.6.0 to 10.7.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.6.0...v10.7.0)

  Updates `mypy-extensions` from 1.0.0 to 1.1.0
  - [Commits](https://github.com/python/mypy_extensions/compare/1.0.0...1.1.0)

  Updates `packaging` from 24.2 to 25.0
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/24.2...25.0)

  Updates `setuptools` from 78.1.0 to 80.0.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v78.1.0...v80.0.0)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.4.26
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-version: 8.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-version: 10.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: mypy-extensions
    dependency-version: 1.1.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-version: '25.0'
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 80.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore: bump runs-on image from ubuntu-20.04 to ubuntu-24.04. [Jose
  Diaz-Gonzalez]
- Chore(deps): bump urllib3 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.3.0 to 2.4.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.3.0...2.4.0)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 5 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 5 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [flake8](https://github.com/pycqa/flake8) | `7.1.2` | `7.2.0` |
  | [pycodestyle](https://github.com/PyCQA/pycodestyle) | `2.12.1` | `2.13.0` |
  | [pyflakes](https://github.com/PyCQA/pyflakes) | `3.2.0` | `3.3.2` |
  | [rich](https://github.com/Textualize/rich) | `13.9.4` | `14.0.0` |
  | [setuptools](https://github.com/pypa/setuptools) | `77.0.3` | `78.1.0` |


  Updates `flake8` from 7.1.2 to 7.2.0
  - [Commits](https://github.com/pycqa/flake8/compare/7.1.2...7.2.0)

  Updates `pycodestyle` from 2.12.1 to 2.13.0
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.12.1...2.13.0)

  Updates `pyflakes` from 3.2.0 to 3.3.2
  - [Changelog](https://github.com/PyCQA/pyflakes/blob/main/NEWS.rst)
  - [Commits](https://github.com/PyCQA/pyflakes/compare/3.2.0...3.3.2)

  Updates `rich` from 13.9.4 to 14.0.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.9.4...v14.0.0)

  Updates `setuptools` from 77.0.3 to 78.1.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v77.0.3...v78.1.0)

  ---
  updated-dependencies:
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pyflakes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 77.0.1 to 77.0.3
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v77.0.1...v77.0.3)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [platformdirs](https://github.com/tox-dev/platformdirs) and [setuptools](https://github.com/pypa/setuptools).


  Updates `platformdirs` from 4.3.6 to 4.3.7
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.3.6...4.3.7)

  Updates `setuptools` from 76.0.0 to 77.0.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v76.0.0...v77.0.1)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 75.8.2 to 76.0.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v75.8.2...v76.0.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...


0.50.1 (2025-03-06)
-------------------
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 75.8.1 to 75.8.2
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v75.8.1...v75.8.2)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 75.8.0 to 75.8.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v75.8.0...v75.8.1)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.50.0 (2025-02-22)
-------------------
- Chore: fix inline comments. [Jose Diaz-Gonzalez]
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [flake8](https://github.com/pycqa/flake8) and [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk).


  Updates `flake8` from 7.1.1 to 7.1.2
  - [Commits](https://github.com/pycqa/flake8/compare/7.1.1...7.1.2)

  Updates `pkginfo` from 1.12.0 to 1.12.1.2

  ---
  updated-dependencies:
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.49.0 (2025-02-01)
-------------------
- Convert timestamp to string, although maybe the other way around would
  be better ... [Honza Maly]
- Implementing incremental by files, safer version of incremental
  backup. [Honza Maly]
- Chore(deps): bump the python-packages group across 1 directory with 7
  updates. [dependabot[bot]]

  Bumps the python-packages group with 7 updates in the / directory:

  | Package | From | To |
  | --- | --- | --- |
  | [autopep8](https://github.com/hhatto/autopep8) | `2.3.1` | `2.3.2` |
  | [black](https://github.com/psf/black) | `24.10.0` | `25.1.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2024.12.14` | `2025.1.31` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `8.5.0` | `8.6.1` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.5.0` | `10.6.0` |
  | [setuptools](https://github.com/pypa/setuptools) | `75.7.0` | `75.8.0` |
  | [twine](https://github.com/pypa/twine) | `6.0.1` | `6.1.0` |



  Updates `autopep8` from 2.3.1 to 2.3.2
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.3.1...v2.3.2)

  Updates `black` from 24.10.0 to 25.1.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.10.0...25.1.0)

  Updates `certifi` from 2024.12.14 to 2025.1.31
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.12.14...2025.01.31)

  Updates `importlib-metadata` from 8.5.0 to 8.6.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v8.5.0...v8.6.1)

  Updates `more-itertools` from 10.5.0 to 10.6.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.5.0...v10.6.0)

  Updates `setuptools` from 75.7.0 to 75.8.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v75.7.0...v75.8.0)

  Updates `twine` from 6.0.1 to 6.1.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/6.0.1...6.1.0)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: twine
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [pygments](https://github.com/pygments/pygments) and [setuptools](https://github.com/pypa/setuptools).


  Updates `pygments` from 2.18.0 to 2.19.1
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.18.0...2.19.1)

  Updates `setuptools` from 75.6.0 to 75.7.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v75.6.0...v75.7.0)

  ---
  updated-dependencies:
  - dependency-name: pygments
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...


0.48.0 (2025-01-04)
-------------------
- Chore: reformat file to fix lint issues. [Jose Diaz-Gonzalez]
- Chore(deps): bump the python-packages group across 1 directory with 4
  updates. [dependabot[bot]]

  Bumps the python-packages group with 4 updates in the / directory: [charset-normalizer](https://github.com/jawah/charset_normalizer), [click](https://github.com/pallets/click), [keyring](https://github.com/jaraco/keyring) and [urllib3](https://github.com/urllib3/urllib3).


  Updates `charset-normalizer` from 3.4.0 to 3.4.1
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.0...3.4.1)

  Updates `click` from 8.1.7 to 8.1.8
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.1.7...8.1.8)

  Updates `keyring` from 25.5.0 to 25.6.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v25.5.0...v25.6.0)

  Updates `urllib3` from 2.2.3 to 2.3.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.3...2.3.0)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: click
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Fix typo README.rst: --starred-gists that should be --gists. [Michael
  D. Adams]
- Remove fixed release issue from known blocking errors. [Ethan White]

  The issue with --release producing errors documented in #209 (the linked issue) and #234 appears to have been fixed in #257.

  This change removes the associated warning from the README.
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2024.8.30 to 2024.12.14
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.08.30...2024.12.14)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...


0.47.0 (2024-12-09)
-------------------
- Detect empty HTTPS contexts. [John Doe]

  Some users are relying solely on the certifi package to provide their CA certs, as requests does this by default.

  This patch detects this situation and emits a clear warning as well as importing certifi to work around the situation..

  Fixes #162 .
- Chore(deps): bump six from 1.16.0 to 1.17.0 in the python-packages
  group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [six](https://github.com/benjaminp/six).


  Updates `six` from 1.16.0 to 1.17.0
  - [Changelog](https://github.com/benjaminp/six/blob/main/CHANGES)
  - [Commits](https://github.com/benjaminp/six/compare/1.16.0...1.17.0)

  ---
  updated-dependencies:
  - dependency-name: six
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 20
  updates. [dependabot[bot]]

  Bumps the python-packages group with 20 updates in the / directory:

  | Package | From | To |
  | --- | --- | --- |
  | [black](https://github.com/psf/black) | `24.4.2` | `24.10.0` |
  | [bleach](https://github.com/mozilla/bleach) | `6.1.0` | `6.2.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2024.7.4` | `2024.8.30` |
  | [charset-normalizer](https://github.com/Ousret/charset_normalizer) | `3.3.2` | `3.4.0` |
  | [flake8](https://github.com/pycqa/flake8) | `7.1.0` | `7.1.1` |
  | [idna](https://github.com/kjd/idna) | `3.7` | `3.10` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `7.2.1` | `8.5.0` |
  | [keyring](https://github.com/jaraco/keyring) | `25.2.1` | `25.5.0` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.3.0` | `10.5.0` |
  | [packaging](https://github.com/pypa/packaging) | `24.1` | `24.2` |
  | [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk) | `1.11.1` | `1.12.0` |
  | [platformdirs](https://github.com/tox-dev/platformdirs) | `4.2.2` | `4.3.6` |
  | [pycodestyle](https://github.com/PyCQA/pycodestyle) | `2.12.0` | `2.12.1` |
  | [readme-renderer](https://github.com/pypa/readme_renderer) | `43.0` | `44.0` |
  | [rich](https://github.com/Textualize/rich) | `13.7.1` | `13.9.4` |
  | [setuptools](https://github.com/pypa/setuptools) | `70.1.1` | `75.6.0` |
  | [tqdm](https://github.com/tqdm/tqdm) | `4.66.4` | `4.67.1` |
  | [twine](https://github.com/pypa/twine) | `5.1.0` | `6.0.1` |
  | [urllib3](https://github.com/urllib3/urllib3) | `2.2.2` | `2.2.3` |
  | [zipp](https://github.com/jaraco/zipp) | `3.19.2` | `3.21.0` |



  Updates `black` from 24.4.2 to 24.10.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.4.2...24.10.0)

  Updates `bleach` from 6.1.0 to 6.2.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.1.0...v6.2.0)

  Updates `certifi` from 2024.7.4 to 2024.8.30
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.07.04...2024.08.30)

  Updates `charset-normalizer` from 3.3.2 to 3.4.0
  - [Release notes](https://github.com/Ousret/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Ousret/charset_normalizer/compare/3.3.2...3.4.0)

  Updates `flake8` from 7.1.0 to 7.1.1
  - [Commits](https://github.com/pycqa/flake8/compare/7.1.0...7.1.1)

  Updates `idna` from 3.7 to 3.10
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.7...v3.10)

  Updates `importlib-metadata` from 7.2.1 to 8.5.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.2.1...v8.5.0)

  Updates `keyring` from 25.2.1 to 25.5.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v25.2.1...v25.5.0)

  Updates `more-itertools` from 10.3.0 to 10.5.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.3.0...v10.5.0)

  Updates `packaging` from 24.1 to 24.2
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/24.1...24.2)

  Updates `pkginfo` from 1.11.1 to 1.12.0

  Updates `platformdirs` from 4.2.2 to 4.3.6
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.2.2...4.3.6)

  Updates `pycodestyle` from 2.12.0 to 2.12.1
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.12.0...2.12.1)

  Updates `readme-renderer` from 43.0 to 44.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/43.0...44.0)

  Updates `rich` from 13.7.1 to 13.9.4
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.7.1...v13.9.4)

  Updates `setuptools` from 70.1.1 to 75.6.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v70.1.1...v75.6.0)

  Updates `tqdm` from 4.66.4 to 4.67.1
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.66.4...v4.67.1)

  Updates `twine` from 5.1.0 to 6.0.1
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/5.1.0...6.0.1)

  Updates `urllib3` from 2.2.2 to 2.2.3
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.2...2.2.3)

  Updates `zipp` from 3.19.2 to 3.21.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.19.2...v3.21.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: bleach
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: idna
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: twine
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- KeyError fix with gists. [John Doe]
- Fix punctuation in README. [Jakub Wilk]


0.46.0 (2024-09-11)
-------------------

Fix
~~~
- Do not double encode auth when retrieving release assets. [Jarl
  Totland]
- Add now missing setuptools. [Jose Diaz-Gonzalez]

Other
~~~~~
- Git fetch is required even when using lfs. [Louis Parisot]
- Upgrade github workflow ubuntu containers to newest LTS. [Albert Wang]
- Chore(deps): bump certifi from 2024.6.2 to 2024.7.4. [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2024.6.2 to 2024.7.4.
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.06.02...2024.07.04)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Chore(deps): bump docker/build-push-action from 5 to 6.
  [dependabot[bot]]

  Bumps [docker/build-push-action](https://github.com/docker/build-push-action) from 5 to 6.
  - [Release notes](https://github.com/docker/build-push-action/releases)
  - [Commits](https://github.com/docker/build-push-action/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: docker/build-push-action
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Chore(deps): bump the python-packages group across 1 directory with 3
  updates. [dependabot[bot]]

  Bumps the python-packages group with 3 updates in the / directory: [autopep8](https://github.com/hhatto/autopep8), [importlib-metadata](https://github.com/python/importlib_metadata) and [setuptools](https://github.com/pypa/setuptools).


  Updates `autopep8` from 2.3.0 to 2.3.1
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.3.0...v2.3.1)

  Updates `importlib-metadata` from 7.2.0 to 7.2.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.2.0...v7.2.1)

  Updates `setuptools` from 70.1.0 to 70.1.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v70.1.0...v70.1.1)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [importlib-metadata](https://github.com/python/importlib_metadata) and [setuptools](https://github.com/pypa/setuptools).


  Updates `importlib-metadata` from 7.1.0 to 7.2.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.1.0...v7.2.0)

  Updates `setuptools` from 70.0.0 to 70.1.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v70.0.0...v70.1.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [autopep8](https://github.com/hhatto/autopep8), [flake8](https://github.com/pycqa/flake8) and [pycodestyle](https://github.com/PyCQA/pycodestyle).


  Updates `autopep8` from 2.2.0 to 2.3.0
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.2.0...v2.3.0)

  Updates `flake8` from 7.0.0 to 7.1.0
  - [Commits](https://github.com/pycqa/flake8/compare/7.0.0...7.1.0)

  Updates `pycodestyle` from 2.11.1 to 2.12.0
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.11.1...2.12.0)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 from 2.2.1 to 2.2.2. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.2.1 to 2.2.2.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.1...2.2.2)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group across 1 directory with 7
  updates. [dependabot[bot]]

  Bumps the python-packages group with 7 updates in the / directory:

  | Package | From | To |
  | --- | --- | --- |
  | [autopep8](https://github.com/hhatto/autopep8) | `2.1.1` | `2.2.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2024.2.2` | `2024.6.2` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.2.0` | `10.3.0` |
  | [packaging](https://github.com/pypa/packaging) | `24.0` | `24.1` |
  | [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk) | `1.10.0` | `1.11.1` |
  | [requests](https://github.com/psf/requests) | `2.32.2` | `2.32.3` |
  | [zipp](https://github.com/jaraco/zipp) | `3.18.2` | `3.19.2` |



  Updates `autopep8` from 2.1.1 to 2.2.0
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.1.1...v2.2.0)

  Updates `certifi` from 2024.2.2 to 2024.6.2
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.02.02...2024.06.02)

  Updates `more-itertools` from 10.2.0 to 10.3.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.2.0...v10.3.0)

  Updates `packaging` from 24.0 to 24.1
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/24.0...24.1)

  Updates `pkginfo` from 1.10.0 to 1.11.1

  Updates `requests` from 2.32.2 to 2.32.3
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.2...v2.32.3)

  Updates `zipp` from 3.18.2 to 3.19.2
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.18.2...v3.19.2)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: requests
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- --- updated-dependencies: - dependency-name: autopep8   dependency-
  type: direct:production   update-type: version-update:semver-patch
  dependency-group: python-packages - dependency-name: black
  dependency-type: direct:production   update-type: version-
  update:semver-minor   dependency-group: python-packages - dependency-
  name: docutils   dependency-type: direct:production   update-type:
  version-update:semver-minor   dependency-group: python-packages -
  dependency-name: keyring   dependency-type: direct:production
  update-type: version-update:semver-minor   dependency-group: python-
  packages - dependency-name: platformdirs   dependency-type:
  direct:production   update-type: version-update:semver-patch
  dependency-group: python-packages - dependency-name: pygments
  dependency-type: direct:production   update-type: version-
  update:semver-minor   dependency-group: python-packages - dependency-
  name: requests   dependency-type: direct:production   update-type:
  version-update:semver-minor   dependency-group: python-packages -
  dependency-name: tqdm   dependency-type: direct:production   update-
  type: version-update:semver-patch   dependency-group: python-packages
  - dependency-name: twine   dependency-type: direct:production
  update-type: version-update:semver-minor   dependency-group: python-
  packages - dependency-name: zipp   dependency-type: direct:production
  update-type: version-update:semver-patch   dependency-group: python-
  packages ... [dependabot[bot]]
- Chore: update python version in release workflow. [Jose Diaz-Gonzalez]
- Chore: update python version used in linting. [Jose Diaz-Gonzalez]
- Chore: drop unsupported python versions and add supported ones. [Jose
  Diaz-Gonzalez]
- --- updated-dependencies: - dependency-name: requests   dependency-
  type: direct:production ... [dependabot[bot]]
- Chore(deps): bump tqdm from 4.66.2 to 4.66.3. [dependabot[bot]]

  Bumps [tqdm](https://github.com/tqdm/tqdm) from 4.66.2 to 4.66.3.
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.66.2...v4.66.3)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-type: direct:production
  ...


0.45.2 (2024-05-04)
-------------------
- Chore(deps): bump idna from 3.6 to 3.7. [dependabot[bot]]

  Bumps [idna](https://github.com/kjd/idna) from 3.6 to 3.7.
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.6...v3.7)

  ---
  updated-dependencies:
  - dependency-name: idna
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [keyring](https://github.com/jaraco/keyring).


  Updates `keyring` from 25.0.0 to 25.1.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v25.0.0...v25.1.0)

  ---
  updated-dependencies:
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [jaraco-classes](https://github.com/jaraco/jaraco.classes).


  Updates `jaraco-classes` from 3.3.1 to 3.4.0
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.3.1...v3.4.0)

  ---
  updated-dependencies:
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [keyring](https://github.com/jaraco/keyring).


  Updates `keyring` from 24.3.1 to 25.0.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v24.3.1...v25.0.0)

  ---
  updated-dependencies:
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [importlib-metadata](https://github.com/python/importlib_metadata).


  Updates `importlib-metadata` from 7.0.2 to 7.1.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.2...v7.1.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump actions/setup-python from 4 to 5. [dependabot[bot]]

  Bumps [actions/setup-python](https://github.com/actions/setup-python) from 4 to 5.
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v4...v5)

  ---
  updated-dependencies:
  - dependency-name: actions/setup-python
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Scheduled dependabot for GitHub Actions. [paranerd]
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [autopep8](https://github.com/hhatto/autopep8) and [black](https://github.com/psf/black).


  Updates `autopep8` from 2.0.4 to 2.1.0
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.0.4...v2.1.0)

  Updates `black` from 24.2.0 to 24.3.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.2.0...24.3.0)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Added Docker info to README. [paranerd]
- Disable credential persistance on checkout. [paranerd]
- Bumped actions versions to latest. [paranerd]


0.45.1 (2024-03-17)
-------------------
- Remove trailing whitespaces. [dale-primer-e]

  That are triggering flake.
- Fix error with as_app flag. [dale-primer-e]
- Fix error downloading assets. [dale-primer-e]

  When downloading assets using a fine grained token you will get a "can't
  concat str to bytes" error. This is due to the fine grained token being
  concatenated onto bytes in the line:

  `request.add_header("Authorization", "Basic ".encode("ascii") + auth)`

  This is better handled in the function `_construct_request` so I changed
  the lines that construct the request in `download_file` to use the
  function `_construct_request` and updated the function signature to
  reflect that.
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [zipp](https://github.com/jaraco/zipp).


  Updates `zipp` from 3.18.0 to 3.18.1
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.18.0...v3.18.1)

  ---
  updated-dependencies:
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [zipp](https://github.com/jaraco/zipp).


  Updates `zipp` from 3.17.0 to 3.18.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.17.0...v3.18.0)

  ---
  updated-dependencies:
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [importlib-metadata](https://github.com/python/importlib_metadata) and [packaging](https://github.com/pypa/packaging).


  Updates `importlib-metadata` from 7.0.1 to 7.0.2
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.1...v7.0.2)

  Updates `packaging` from 23.2 to 24.0
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/23.2...24.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk) and [rich](https://github.com/Textualize/rich).


  Updates `pkginfo` from 1.9.6 to 1.10.0

  Updates `rich` from 13.7.0 to 13.7.1
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.7.0...v13.7.1)

  ---
  updated-dependencies:
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [keyring](https://github.com/jaraco/keyring).


  Updates `keyring` from 24.3.0 to 24.3.1
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v24.3.0...v24.3.1)

  ---
  updated-dependencies:
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [readme-renderer](https://github.com/pypa/readme_renderer).


  Updates `readme-renderer` from 42.0 to 43.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/42.0...43.0)

  ---
  updated-dependencies:
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.2.0 to 2.2.1
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.0...2.2.1)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 24.1.1 to 24.2.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.1.1...24.2.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [tqdm](https://github.com/tqdm/tqdm) and [twine](https://github.com/pypa/twine).


  Updates `tqdm` from 4.66.1 to 4.66.2
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.66.1...v4.66.2)

  Updates `twine` from 4.0.2 to 5.0.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/4.0.2...5.0.0)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: twine
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [jaraco-classes](https://github.com/jaraco/jaraco.classes).


  Updates `jaraco-classes` from 3.3.0 to 3.3.1
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.3.0...v3.3.1)

  ---
  updated-dependencies:
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2023.11.17 to 2024.2.2
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.11.17...2024.02.02)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [platformdirs](https://github.com/platformdirs/platformdirs) and [urllib3](https://github.com/urllib3/urllib3).


  Updates `platformdirs` from 4.1.0 to 4.2.0
  - [Release notes](https://github.com/platformdirs/platformdirs/releases)
  - [Changelog](https://github.com/platformdirs/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/platformdirs/platformdirs/compare/4.1.0...4.2.0)

  Updates `urllib3` from 2.1.0 to 2.2.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.1.0...2.2.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 24.1.0 to 24.1.1
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.1.0...24.1.1)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.45.0 (2024-01-29)
-------------------

Fix
~~~
- Catch 404s for non-existing hooks. Fixes #176. [Moritz Federspiel]
- Ensure wheel is installed. [Jose Diaz-Gonzalez]

Other
~~~~~
- Fix code style. [BrOleg5]
- Add option to skip prerelease versions. [BrOleg5]

  Replace release sorting by tag with release sorting by creation date.
- Add option to include certain number of the latest releases. [BrOleg5]
- Auto docker build. [8cH9azbsFifZ]
- Vs code. [8cH9azbsFifZ]
- Chore(deps): bump the python-packages group with 6 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 6 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [black](https://github.com/psf/black) | `23.11.0` | `24.1.0` |
  | [flake8](https://github.com/pycqa/flake8) | `6.1.0` | `7.0.0` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `7.0.0` | `7.0.1` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.1.0` | `10.2.0` |
  | [pathspec](https://github.com/cpburnz/python-pathspec) | `0.11.2` | `0.12.1` |
  | [pyflakes](https://github.com/PyCQA/pyflakes) | `3.1.0` | `3.2.0` |


  Updates `black` from 23.11.0 to 24.1.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/23.11.0...24.1.0)

  Updates `flake8` from 6.1.0 to 7.0.0
  - [Commits](https://github.com/pycqa/flake8/compare/6.1.0...7.0.0)

  Updates `importlib-metadata` from 7.0.0 to 7.0.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.0...v7.0.1)

  Updates `more-itertools` from 10.1.0 to 10.2.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.1.0...v10.2.0)

  Updates `pathspec` from 0.11.2 to 0.12.1
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v0.11.2...v0.12.1)

  Updates `pyflakes` from 3.1.0 to 3.2.0
  - [Changelog](https://github.com/PyCQA/pyflakes/blob/main/NEWS.rst)
  - [Commits](https://github.com/PyCQA/pyflakes/compare/3.1.0...3.2.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pathspec
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pyflakes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 15 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 15 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [bleach](https://github.com/mozilla/bleach) | `6.0.0` | `6.1.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2023.7.22` | `2023.11.17` |
  | [charset-normalizer](https://github.com/Ousret/charset_normalizer) | `3.1.0` | `3.3.2` |
  | [idna](https://github.com/kjd/idna) | `3.4` | `3.6` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `6.6.0` | `7.0.0` |
  | [jaraco-classes](https://github.com/jaraco/jaraco.classes) | `3.2.3` | `3.3.0` |
  | [keyring](https://github.com/jaraco/keyring) | `23.13.1` | `24.3.0` |
  | [markdown-it-py](https://github.com/executablebooks/markdown-it-py) | `2.2.0` | `3.0.0` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `9.1.0` | `10.1.0` |
  | [pygments](https://github.com/pygments/pygments) | `2.15.1` | `2.17.2` |
  | [readme-renderer](https://github.com/pypa/readme_renderer) | `37.3` | `42.0` |
  | [rich](https://github.com/Textualize/rich) | `13.3.5` | `13.7.0` |
  | [tqdm](https://github.com/tqdm/tqdm) | `4.65.0` | `4.66.1` |
  | [urllib3](https://github.com/urllib3/urllib3) | `2.0.7` | `2.1.0` |
  | [zipp](https://github.com/jaraco/zipp) | `3.15.0` | `3.17.0` |


  Updates `bleach` from 6.0.0 to 6.1.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.0.0...v6.1.0)

  Updates `certifi` from 2023.7.22 to 2023.11.17
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.07.22...2023.11.17)

  Updates `charset-normalizer` from 3.1.0 to 3.3.2
  - [Release notes](https://github.com/Ousret/charset_normalizer/releases)
  - [Changelog](https://github.com/Ousret/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Ousret/charset_normalizer/compare/3.1.0...3.3.2)

  Updates `idna` from 3.4 to 3.6
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.4...v3.6)

  Updates `importlib-metadata` from 6.6.0 to 7.0.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v6.6.0...v7.0.0)

  Updates `jaraco-classes` from 3.2.3 to 3.3.0
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.2.3...v3.3.0)

  Updates `keyring` from 23.13.1 to 24.3.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v23.13.1...v24.3.0)

  Updates `markdown-it-py` from 2.2.0 to 3.0.0
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v2.2.0...v3.0.0)

  Updates `more-itertools` from 9.1.0 to 10.1.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v9.1.0...v10.1.0)

  Updates `pygments` from 2.15.1 to 2.17.2
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.15.1...2.17.2)

  Updates `readme-renderer` from 37.3 to 42.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/37.3...42.0)

  Updates `rich` from 13.3.5 to 13.7.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.3.5...v13.7.0)

  Updates `tqdm` from 4.65.0 to 4.66.1
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.65.0...v4.66.1)

  Updates `urllib3` from 2.0.7 to 2.1.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.7...2.1.0)

  Updates `zipp` from 3.15.0 to 3.17.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.15.0...v3.17.0)

  ---
  updated-dependencies:
  - dependency-name: bleach
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: idna
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: markdown-it-py
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: pygments
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore: format python code. [Jose Diaz-Gonzalez]
- Chore: format yaml. [Jose Diaz-Gonzalez]
- Chore: update gitignore. [Jose Diaz-Gonzalez]
- Feat: add dependabot config to repository. [Jose Diaz-Gonzalez]


0.44.1 (2023-12-09)
-------------------

Fix
~~~
- Use a deploy key to push tags so releases get auto-created. [Jose
  Diaz-Gonzalez]

Other
~~~~~
- Chore(deps): bump certifi from 2023.5.7 to 2023.7.22.
  [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2023.5.7 to 2023.7.22.
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.05.07...2023.07.22)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Tests: run lint on pull requests. [Jose Diaz-Gonzalez]
- Chore(deps): bump urllib3 from 2.0.2 to 2.0.7. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.2 to 2.0.7.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.2...2.0.7)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
  ...
- Chore: remove circleci as tests now run in github actions. [Jose Diaz-
  Gonzalez]
- Tests: install correct dependencies and rename job. [Jose Diaz-
  Gonzalez]
- Tests: add lint github action workflow. [Jose Diaz-Gonzalez]
- Feat: install autopep8. [Jose Diaz-Gonzalez]
- Chore(deps): bump certifi from 2023.5.7 to 2023.7.22.
  [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2023.5.7 to 2023.7.22.
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.05.07...2023.07.22)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Chore: reformat file and update flake8. [Jose Diaz-Gonzalez]


0.44.0 (2023-12-09)
-------------------

Fix
~~~
- Do not use raw property in readme. [Jose Diaz-Gonzalez]

  This is disabled on pypi.
- Validate release before committing and uploading it. [Jose Diaz-
  Gonzalez]
- Correct lint issues and show errors on lint. [Jose Diaz-Gonzalez]
- Minor cosmetic changes. [ZhymabekRoman]
- Add forgotten variable formatting. [ZhymabekRoman]
- Refactor logging Based on #195. [ZhymabekRoman]
- Minor typo fix. [Zhymabek Roman]

Other
~~~~~
- Bump certifi from 2023.5.7 to 2023.7.22. [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2023.5.7 to 2023.7.22.
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.05.07...2023.07.22)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Checkout everything. [Halvor Holsten Strand]
- Added automatic release workflow, for use with GitHub Actions. [Halvor
  Holsten Strand]
- Feat: create Dockerfile. [Tom Plant]
- Fix rst html. [hozza]
- Add contributor section. [hozza]
- Fix readme wording and format. [hozza]
- Fixed readme working and layout. [hozza]
- Fix readme formatting, spelling and layout. [hozza]
- Added details usage and examples including gotchas, errors and
  development instructions. [hozza]
- Added verbose install instructions. [hozza]
- Bump urllib3 from 2.0.2 to 2.0.7. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.2 to 2.0.7.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.2...2.0.7)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
  ...
- Suggested modification to fix win32 logging failure, due to local
  variable scope. Logger does not appear to have any utility within
  "logging_subprocess". [Halvor Holsten Strand]
- Simplified one if/elif scenario. Extracted file reading of another
  if/elif scenario. [Halvor Holsten Strand]
- Ran black. [Halvor Holsten Strand]
- Keep backwards compatability by going back to "--token" for classic.
  Allow "file://" uri for "--token-fine". [Halvor Holsten Strand]
- Add support for fine-grained tokens. [froggleston]
- Refactor logging and add support for quiet flag. [Harrison Wright]


0.43.1 (2023-05-29)
-------------------
- Chore: add release requirements. [Jose Diaz-Gonzalez]


0.43.0 (2023-05-29)
-------------------

Fix
~~~
- Do not update readme. [Jose Diaz-Gonzalez]
- Adjust for black. [Jose Diaz-Gonzalez]
- Adjust for black. [Jose Diaz-Gonzalez]
- Adjust for black. [Jose Diaz-Gonzalez]

Other
~~~~~
- Feat: commit gitchangelog.rc to repo so anyone can generate a
  changelog. [Jose Diaz-Gonzalez]
- Feat: add release tagging. [Jose Diaz-Gonzalez]
- Chore: formatting. [Jose Diaz-Gonzalez]
- Chore: run black. [Jose Diaz-Gonzalez]
- Add --log-level command line argument. [Enrico Tröger]

  Support changing the log level to the desired value easily.
  For example, this is useful to suppress progress messages but
  keep logging warnings and errors.
- Check both updated_at and pushed_at properties. [Ken Bailey]

  Check both updated_at and pushed_at dates to get the last_update to reduce data retrieved on incremental api calls using since.


0.42.0 (2022-11-28)
-------------------
- Add option to exclude repositories. [npounder]
- Backup regular pull request comments as well. [Oneric]

  Before, only review comments were backed up;
  regular comments need to be fetched via issue API.
- Fix bug forever retry when request url error. [kornpisey]
- Added --no-prune option to disable prune option when doing git fetch.
  [kornpisey]


0.41.0 (2022-03-02)
-------------------
- Git lfs clone doe snot respect --mirror. [Louis Parisot]


0.40.2 (2021-12-29)
-------------------
- Fix lint issues raised by Flake8. [atinary-afoulon]

  According to job:
  [ https://app.circleci.com/pipelines/github/josegonzalez/python-github-backup/30/workflows/74eb93f2-2505-435d-b728-03b3cc04c14a/jobs/23 ]

  Failed on the following checks:
  ./github_backup/github_backup.py:20:1: F811 redefinition of unused 'logging' from line 14
  ./github_backup/github_backup.py:45:1: E302 expected 2 blank lines, found 1
  ./github_backup/github_backup.py:136:20: E251 unexpected spaces around keyword / parameter equals


0.40.1 (2021-09-22)
-------------------
- Revert to fetch. [Harrison Wright]


0.40.0 (2021-07-12)
-------------------
- Add retry on certain network errors. [Jacek Nykis]

  This change includes certain network level errors in the retry logic.
  It partially address #110 but I think more comprehensive fix would be useful.
- Pull changes from remote. [Jonas]

  use `git pull` to pull actual files from the remote instead of using `fetch` for only the metadata


0.39.0 (2021-03-19)
-------------------

Fix
~~~
- Fix missing INFO logs. [Gallo Feliz]

Other
~~~~~
- Try to make compatible code with direct Python call ; reduce the hard
  link of the code with the cli. [Gallo Feliz]
- Fixed release_name with slash bug. [Álvaro Torres Cogollo]


0.38.0 (2021-02-13)
-------------------

Fix
~~~
- Always clone with OAuth token when provided. [Samantha Baldwin]

  Github Enterprise servers with 'Anonymous Git read access' disabled
  cause `git ls-remote` to fail (128) for a repo's `clone_url`. Using the
  OAuth token when provided allows cloning private AND public repos when
  Anonymous Git read access is disabled.

Other
~~~~~
- Change broken link to a fork to a working link to upstream. [Rick van
  Schijndel]


0.37.2 (2021-01-02)
-------------------

Fix
~~~
- Use distutils.core on error. [Jose Diaz-Gonzalez]


0.37.1 (2021-01-02)
-------------------

Fix
~~~
- Use twine for releases. [Jose Diaz-Gonzalez]

  The old method of releasing to pypi broke for whatever reason and switching to a supported toolchain is easier than debugging the old one.

  Additionally:

  - Update gitchangelog
  - Fix license entry
  - Set long description type
  - Gitignore the temporary readme file


0.37.0 (2021-01-02)
-------------------
- Add support for python 3.7 and 3.8 in package classifiers. [Albert
  Wang]
- Remove support for python 2.7 in package classifiers. [Albert Wang]
- Remove python 2 specific import logic. [Albert Wang]
- Remove python 2 specific logic. [Albert Wang]
- Add ability to skip archived repositories. [Gary Moon]


0.36.0 (2020-08-29)
-------------------
- Add flake8 instructions to readme. [Albert Wang]
- Fix regex string. [Albert Wang]
- Fix whitespace issues. [Albert Wang]
- Do not use bare excepts. [Albert Wang]
- Add .circleci/config.yml. [Albert Wang]
- Include --private flag in example. [wouter bolsterlee]

  By default, private repositories are not included. This is surprising.
  It took me a while to figure this out, and making that clear in the
  example can help others to be aware of that.


0.35.0 (2020-08-05)
-------------------
- Make API request throttling optional. [Samantha Baldwin]


0.34.0 (2020-07-24)
-------------------
- Add logic for transforming gist repository urls to ssh. [Matt Fields]


0.33.0 (2020-04-13)
-------------------
- Add basic API request throttling. [Enrico Tröger]

  A simple approach to throttle API requests and so keep within the rate
  limits of the API. Can be enabled with "--throttle-limit" to specify
  when throttling should start.
  "--throttle-pause" defines the time to sleep between further API
  requests.


0.32.0 (2020-04-13)
-------------------
- Add timestamp to log messages. [Enrico Tröger]


0.31.0 (2020-02-25)
-------------------
- #123 update: changed --as-app 'help' description. [ethan]
- #123: Support Authenticating As Github Application. [ethan]


0.29.0 (2020-02-14)
-------------------
- #50 update: keep main() in bin. [ethan]
- #50 - refactor for friendlier import. [ethan]


0.28.0 (2020-02-03)
-------------------
- Remove deprecated (and removed) git lfs flags. [smiley]

  "--tags" and "--force" were removed at some point from "git lfs fetch". This broke our backup script.


0.27.0 (2020-01-22)
-------------------
- Fixed script fails if not installed from pip. [Ben Baron]

  At the top of the script, the line from github_backup import __version__ gets the script's version number to use if the script is called with the -v or --version flags. The problem is that if the script hasn't been installed via pip (for example I cloned the repo directly to my backup server), the script will fail due to an import exception.

  Also presumably it will always use the version number from pip even if running a modified version from git or a fork or something, though this does not fix that as I have no idea how to check if it's running the pip installed version or not. But at least the script will now work fine if cloned from git or just copied to another machine.

  closes https://github.com/josegonzalez/python-github-backup/issues/141
- Fixed macOS keychain access when using Python 3. [Ben Baron]

  Python 3 is returning bytes rather than a string, so the string concatenation to create the auth variable was throwing an exception which the script was interpreting to mean it couldn't find the password. Adding a conversion to string first fixed the issue.
- Public repos no longer include the auth token. [Ben Baron]

  When backing up repositories using an auth token and https, the GitHub personal auth token is leaked in each backed up repository. It is included in the URL of each repository's git remote url.

  This is not needed as they are public and can be accessed without the token and can cause issues in the future if the token is ever changed, so I think it makes more sense not to have the token stored in each repo backup. I think the token should only be "leaked" like this out of necessity, e.g. it's a private repository and the --prefer-ssh option was not chosen so https with auth token was required to perform the clone.
- Fixed comment typo. [Ben Baron]
- Switched log_info to log_warning in download_file. [Ben Baron]
- Crash when an release asset doesn't exist. [Ben Baron]

  Currently, the script crashes whenever a release asset is unable to download (for example a 404 response). This change instead logs the failure and allows the script to continue. No retry logic is enabled, but at least it prevents the crash and allows the backup to complete. Retry logic can be implemented later if wanted.

  closes https://github.com/josegonzalez/python-github-backup/issues/129
- Moved asset downloading loop inside the if block. [Ben Baron]
- Separate release assets and skip re-downloading. [Ben Baron]

  Currently the script puts all release assets into the same folder called `releases`. So any time 2 release files have the same name, only the last one downloaded is actually saved. A particularly bad example of this is MacDownApp/macdown where all of their releases are named `MacDown.app.zip`. So even though they have 36 releases and all 36 are downloaded, only the last one is actually saved.

  With this change, each releases' assets are now stored in a fubfolder inside `releases` named after the release name. There could still be edge cases if two releases have the same name, but this is still much safer tha the previous behavior.

  This change also now checks if the asset file already exists on disk and skips downloading it. This drastically speeds up addiotnal syncs as it no longer downloads every single release every single time. It will now only download new releases which I believe is the expected behavior.

  closes https://github.com/josegonzalez/python-github-backup/issues/126
- Added newline to end of file. [Ben Baron]
- Improved gitignore, macOS files and IDE configs. [Ben Baron]

  Ignores the annoying hidden macOS files .DS_Store and ._* as well as the IDE configuration folders for contributors using the popular Visual Studio Code and Atom IDEs (more can be added later as needed).


0.26.0 (2019-09-23)
-------------------
- Workaround gist clone in `--prefer-ssh` mode. [Vladislav Yarmak]
- Create PULL_REQUEST.md. [Jose Diaz-Gonzalez]
- Create ISSUE_TEMPLATE.md. [Jose Diaz-Gonzalez]


0.25.0 (2019-07-03)
-------------------
- Issue 119: Change retrieve_data to be a generator. [2a]

  See issue #119.


0.24.0 (2019-06-27)
-------------------
- QKT-45: include assets - update readme. [Ethan Timm]

  update readme with flag information for including assets alongside their respective releases
- Make assets it's own flag. [Harrison Wright]
- Fix super call for python2. [Harrison Wright]
- Fix redirect to s3. [Harrison Wright]
- WIP: download assets. [Harrison Wright]
- QKT-42: releases - add readme info. [ethan]
- QKT-42 update: shorter command flag. [ethan]
- QKT-42: support saving release information. [ethan]
- Fix pull details. [Harrison Wright]


0.23.0 (2019-06-04)
-------------------
- Avoid to crash in case of HTTP 502 error. [Gael de Chalendar]

  Survive also on socket.error connections like on HTTPError or URLError.

  This should solve issue #110.


0.22.2 (2019-02-21)
-------------------

Fix
~~~
- Warn instead of error. [Jose Diaz-Gonzalez]

  Refs #106


0.22.1 (2019-02-21)
-------------------
- Log URL error https://github.com/josegonzalez/python-github-
  backup/issues/105. [JOHN STETIC]


0.22.0 (2019-02-01)
-------------------
- Remove unnecessary sys.exit call. [W. Harrison Wright]
- Add org check to avoid incorrect log output. [W. Harrison Wright]
- Fix accidental system exit with better logging strategy. [W. Harrison
  Wright]


0.21.1 (2018-12-25)
-------------------
- Mark options which are not included in --all. [Bernd]

  As discussed in Issue #100


0.21.0 (2018-11-28)
-------------------
- Correctly download repos when user arg != authenticated user. [W.
  Harrison Wright]


0.20.1 (2018-09-29)
-------------------
- Clone the specified user's gists, not the authenticated user. [W.
  Harrison Wright]
- Clone the specified user's starred repos, not the authenticated user.
  [W. Harrison Wright]


0.20.0 (2018-03-24)
-------------------
- Chore: drop Python 2.6. [Jose Diaz-Gonzalez]
- Feat: simplify release script. [Jose Diaz-Gonzalez]


0.19.2 (2018-03-24)
-------------------

Fix
~~~
- Cleanup pep8 violations. [Jose Diaz-Gonzalez]


0.19.0 (2018-03-24)
-------------------
- Add additional output for the current request. [Robin Gloster]

  This is useful to have some progress indication for huge repositories.
- Add option to backup additional PR details. [Robin Gloster]

  Some payload is only included when requesting a single pull request
- Mark string as binary in comparison for skip_existing. [Johannes
  Bornhold]

  Found out that the flag "--skip-existing" did not work out as expected on Python
  3.6. Tracked it down to the comparison which has to be against a string of bytes
  in Python3.


0.18.0 (2018-02-22)
-------------------
- Add option to fetch followers/following JSON data. [Stephen Greene]


0.17.0 (2018-02-20)
-------------------
- Short circuit gists backup process. [W. Harrison Wright]
- Formatting. [W. Harrison Wright]
- Add ability to backup gists. [W. Harrison Wright]


0.16.0 (2018-01-22)
-------------------
- Change option to --all-starred. [W. Harrison Wright]
- JK don't update documentation. [W. Harrison Wright]
- Put starred clone repoistories under a new option. [W. Harrison
  Wright]
- Add comment. [W. Harrison Wright]
- Add ability to clone starred repos. [W. Harrison Wright]


0.14.1 (2017-10-11)
-------------------
- Fix arg not defined error. [Edward Pfremmer]


0.14.0 (2017-10-11)
-------------------
- Added a check to see if git-lfs is installed when doing an LFS clone.
  [pieterclaerhout]
- Added support for LFS clones. [pieterclaerhout]
- Add pypi info to readme. [Albert Wang]
- Explicitly support python 3 in package description. [Albert Wang]
- Add couple examples to help new users. [Yusuf Tran]


0.13.2 (2017-05-06)
-------------------
- Fix remotes while updating repository. [Dima Gerasimov]


0.13.1 (2017-04-11)
-------------------
- Fix error when repository has no updated_at value. [Nicolai Ehemann]


0.13.0 (2017-04-05)
-------------------
- Add OS check for OSX specific keychain args. [Martin O'Reilly]

  Keychain arguments are only supported on Mac OSX.
  Added check for operating system so we give a
  "Keychain arguments are only supported on Mac OSX"
  error message rather than a "No password item matching the
  provided name and account could be found in the osx keychain"
  error message
- Add support for storing PAT in OSX keychain. [Martin O'Reilly]

  Added additional optional arguments and README guidance for storing
  and accessing a Github personal access token (PAT) in the OSX
  keychain


0.12.1 (2017-03-27)
-------------------
- Avoid remote branch name churn. [Chris Adams]

  This avoids the backup output having lots of "[new branch]" messages
  because removing the old remote name removed all of the existing branch
  references.
- Fix detection of bare git directories. [Andrzej Maczuga]


0.12.0 (2016-11-22)
-------------------

Fix
~~~
- Properly import version from github_backup package. [Jose Diaz-
  Gonzalez]
- Support alternate git status output. [Jose Diaz-Gonzalez]

Other
~~~~~
- Pep8: E501 line too long (83 > 79 characters) [Jose Diaz-Gonzalez]
- Pep8: E128 continuation line under-indented for visual indent. [Jose
  Diaz-Gonzalez]
- Support archivization using bare git clones. [Andrzej Maczuga]
- Fix typo, 3x. [Terrell Russell]


0.11.0 (2016-10-26)
-------------------
- Support --token file:///home/user/token.txt (fixes gh-51) [Björn
  Dahlgren]
- Fix some linting. [Albert Wang]
- Fix byte/string conversion for python 3. [Albert Wang]
- Support python 3. [Albert Wang]
- Encode special characters in password. [Remi Rampin]
- Don't pretend program name is "Github Backup" [Remi Rampin]
- Don't install over insecure connection. [Remi Rampin]

  The git:// protocol is unauthenticated and unencrypted, and no longer advertised by GitHub. Using HTTPS shouldn't impact performance.


0.10.3 (2016-08-21)
-------------------
- Fixes #29. [Jonas Michel]

  Reporting an error when the user's rate limit is exceeded causes
  the script to terminate after resuming execution from a rate limit
  sleep. Instead of generating an explicit error we just want to
  inform the user that the script is going to sleep until their rate
  limit count resets.
- Fixes #29. [Jonas Michel]

  The errors list was not being cleared out after resuming a backup
  from a rate limit sleep. When the backup was resumed, the non-empty
  errors list caused the backup to quit after the next `retrieve_data`
  request.


0.10.2 (2016-08-21)
-------------------
- Add a note regarding git version requirement. [Jose Diaz-Gonzalez]

  Closes #37


0.10.0 (2016-08-18)
-------------------
- Implement incremental updates. [Robert Bradshaw]

  Guarded with an --incremental flag.

  Stores the time of the last update and only downloads issue and
  pull request data since this time.  All other data is relatively
  small (likely fetched with a single request) and so is simply
  re-populated from scratch as before.


0.9.0 (2016-03-29)
------------------
- Fix cloning private repos with basic auth or token. [Kazuki Suda]


0.8.0 (2016-02-14)
------------------
- Don't store issues which are actually pull requests. [Enrico Tröger]

  This prevents storing pull requests twice since the Github API returns
  pull requests also as issues. Those issues will be skipped but only if
  retrieving pull requests is requested as well.
  Closes #23.


0.7.0 (2016-02-02)
------------------
- Softly fail if not able to read hooks. [Albert Wang]
- Add note about 2-factor auth. [Albert Wang]
- Make user repository search go through endpoint capable of reading
  private repositories. [Albert Wang]
- Prompt for password if only username given. [Alex Hall]


0.6.0 (2015-11-10)
------------------
- Force proper remote url. [Jose Diaz-Gonzalez]
- Improve error handling in case of HTTP errors. [Enrico Tröger]

  In case of a HTTP status code 404, the returned 'r' was never assigned.
  In case of URL errors which are not timeouts, we probably should bail
  out.
- Add --hooks to also include web hooks into the backup. [Enrico Tröger]
- Create the user specified output directory if it does not exist.
  [Enrico Tröger]

  Fixes #17.
- Add missing auth argument to _get_response() [Enrico Tröger]

  When running unauthenticated and Github starts rate-limiting the client,
  github-backup crashes because the used auth variable in _get_response()
  was not available. This change should fix it.
- Add repository URL to error message for non-existing repositories.
  [Enrico Tröger]

  This makes it easier for the user to identify which repository does not
  exist or is not initialised, i.e. whether it is the main repository or
  the wiki repository and which clone URL was used to check.


0.5.0 (2015-10-10)
------------------
- Add release script. [Jose Diaz-Gonzalez]
- Refactor to both simplify codepath as well as follow PEP8 standards.
  [Jose Diaz-Gonzalez]
- Retry 3 times when the connection times out. [Mathijs Jonker]
- Made unicode output defalut. [Kirill Grushetsky]
- Import alphabetised. [Kirill Grushetsky]
- Preserve Unicode characters in the output file. [Kirill Grushetsky]

  Added option to preserve Unicode characters in the output file
- Josegonzales/python-github-backup#12 Added backup of labels and
  milestones. [aensley]
- Fixed indent. [Mathijs Jonker]
- Skip unitialized repo's. [mjonker-embed]

  These gave me errors which caused mails from crontab.
- Added prefer-ssh. [mjonker-embed]

  Was needed for my back-up setup, code includes this but readme wasn't updated
- Retry API requests which failed due to rate-limiting. [Chris Adams]

  This allows operation to continue, albeit at a slower pace,
  if you have enough data to trigger the API rate limits
- Logging_subprocess: always log when a command fails. [Chris Adams]

  Previously git clones could fail without any indication
  unless you edited the source to change `logger=None` to use
  a configured logger.

  Now a non-zero return code will always output a message to
  stderr and will display the executed command so it can be
  rerun for troubleshooting.
- Switch to using ssh_url. [Chris Adams]

  The previous commit used the wrong URL for a private repo. This was
  masked by the lack of error loging in logging_subprocess (which will be
  in a separate branch)
- Add an option to prefer checkouts over SSH. [Chris Adams]

  This is really useful with private repos to avoid being nagged
  for credentials for every repository
- Add pull request support. [Kevin Laude]

  Back up reporitory pull requests by passing the --include-pulls
  argument. Pull requests are saved to
  repositories/<repository name>/pulls/<pull request number>.json. Include
  the --pull-request-comments argument to add review comments to the pull
  request backup and pass the --pull-request-commits argument to add
  commits to the pull request backup.

  Pull requests are automatically backed up when the --all argument is
  uesd.
- Add GitHub Enterprise support. [Kevin Laude]

  Pass the -H or --github-host argument with a GitHub Enterprise hostname
  to backup from that GitHub enterprise host. If no argument is passed
  then back up from github.com.


0.2.0 (2014-09-22)
------------------
- Add support for retrieving repositories. Closes #1. [Jose Diaz-
  Gonzalez]
- Fix PEP8 violations. [Jose Diaz-Gonzalez]
- Add authorization to header only if specified by user. [Ioannis
  Filippidis]
- Fill out readme more. [Jose Diaz-Gonzalez]
- Fix import. [Jose Diaz-Gonzalez]
- Properly name readme. [Jose Diaz-Gonzalez]
- Create MANIFEST.in. [Jose Diaz-Gonzalez]
- Create .gitignore. [Jose Diaz-Gonzalez]
- Create setup.py. [Jose Diaz-Gonzalez]
- Create requirements.txt. [Jose Diaz-Gonzalez]
- Create __init__.py. [Jose Diaz-Gonzalez]
- Create LICENSE.txt. [Jose Diaz-Gonzalez]
- Create README.md. [Jose Diaz-Gonzalez]
- Create github-backup. [Jose Diaz-Gonzalez]



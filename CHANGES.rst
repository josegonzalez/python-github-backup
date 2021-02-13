Changelog
=========

0.38.0 (2021-02-13)
-------------------
------------

Fix
~~~
- Always clone with OAuth token when provided. [Samantha Baldwin]

  Github Enterprise servers with 'Anonymous Git read access' disabled
  cause `git ls-remote` to fail (128) for a repo's `clone_url`. Using the
  OAuth token when provided allows cloning private AND public repos when
  Anonymous Git read access is disabled.

Other
~~~~~
- Merge pull request #172 from samanthaq/always-use-oauth-when-provided.
  [Jose Diaz-Gonzalez]

  fix: Always clone with OAuth token when provided
- Merge pull request #170 from Mindavi/bugfix/broken-url. [Jose Diaz-
  Gonzalez]

  Fix broken and incorrect link to github repository
- Change broken link to a fork to a working link to upstream. [Rick van
  Schijndel]


0.37.2 (2021-01-02)
-------------------

Fix
~~~
- Use distutils.core on error. [Jose Diaz-Gonzalez]

Other
~~~~~
- Release version 0.37.2. [Jose Diaz-Gonzalez]


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

Other
~~~~~
- Release version 0.37.1. [Jose Diaz-Gonzalez]


0.37.0 (2021-01-02)
-------------------
- Release version 0.37.0. [Jose Diaz-Gonzalez]
- Merge pull request #158 from albertyw/python3. [Jose Diaz-Gonzalez]

  Remove support for python 2
- Add support for python 3.7 and 3.8 in package classifiers. [Albert
  Wang]
- Remove support for python 2.7 in package classifiers. [Albert Wang]
- Remove python 2 specific import logic. [Albert Wang]
- Remove python 2 specific logic. [Albert Wang]
- Merge pull request #165 from garymoon/add-skip-archived. [Jose Diaz-
  Gonzalez]

  Add option to skip archived repositories
- Add ability to skip archived repositories. [Gary Moon]


0.36.0 (2020-08-29)
-------------------
- Release version 0.36.0. [Jose Diaz-Gonzalez]
- Merge pull request #157 from albertyw/lint. [Jose Diaz-Gonzalez]
- Add flake8 instructions to readme. [Albert Wang]
- Fix regex string. [Albert Wang]
- Update boolean check. [Albert Wang]
- Fix whitespace issues. [Albert Wang]
- Do not use bare excepts. [Albert Wang]
- Merge pull request #161 from albertyw/circleci-project-setup. [Jose
  Diaz-Gonzalez]

  Add circleci config
- Add .circleci/config.yml. [Albert Wang]
- Merge pull request #160 from wbolster/patch-1. [Jose Diaz-Gonzalez]

  Include --private flag in example
- Include --private flag in example. [wouter bolsterlee]

  By default, private repositories are not included. This is surprising.
  It took me a while to figure this out, and making that clear in the
  example can help others to be aware of that.


0.35.0 (2020-08-05)
-------------------
- Release version 0.35.0. [Jose Diaz-Gonzalez]
- Merge pull request #156 from samanthaq/restore-optional-throttling.
  [Jose Diaz-Gonzalez]

  Make API request throttling optional
- Make API request throttling optional. [Samantha Baldwin]


0.34.0 (2020-07-24)
-------------------
- Release version 0.34.0. [Jose Diaz-Gonzalez]
- Merge pull request #153 from 0x6d617474/gist_ssh. [Jose Diaz-Gonzalez]

  Add logic for transforming gist repository urls to ssh
- Add logic for transforming gist repository urls to ssh. [Matt Fields]


0.33.1 (2020-05-28)
-------------------
- Release version 0.33.1. [Jose Diaz-Gonzalez]
- Merge pull request #151 from garymoon/readme-update-0.33. [Jose Diaz-
  Gonzalez]
- Update the readme for new switches added in 0.33. [Gary Moon]


0.33.0 (2020-04-13)
-------------------
- Release version 0.33.0. [Jose Diaz-Gonzalez]
- Merge pull request #149 from eht16/simple_api_request_throttling.
  [Jose Diaz-Gonzalez]

  Add basic API request throttling
- Add basic API request throttling. [Enrico Tröger]

  A simple approach to throttle API requests and so keep within the rate
  limits of the API. Can be enabled with "--throttle-limit" to specify
  when throttling should start.
  "--throttle-pause" defines the time to sleep between further API
  requests.


0.32.0 (2020-04-13)
-------------------
- Release version 0.32.0. [Jose Diaz-Gonzalez]
- Merge pull request #148 from eht16/logging_with_timestamp. [Jose Diaz-
  Gonzalez]

  Add timestamp to log messages
- Add timestamp to log messages. [Enrico Tröger]
- Merge pull request #147 from tomhoover/update-readme. [Jose Diaz-
  Gonzalez]

  Update README.rst to match 'github-backup -h'
- Update README.rst to match 'github-backup -h' [Tom Hoover]


0.31.0 (2020-02-25)
-------------------
- Release version 0.31.0. [Jose Diaz-Gonzalez]
- Merge pull request #146 from timm3/upstream-123. [Jose Diaz-Gonzalez]

  Authenticate as Github App
- #123 update: changed --as-app 'help' description. [ethan]
- #123: Support Authenticating As Github Application. [ethan]


0.30.0 (2020-02-14)
-------------------
- Release version 0.30.0. [Jose Diaz-Gonzalez]


0.29.0 (2020-02-14)
-------------------
- Release version 0.29.0. [Jose Diaz-Gonzalez]
- Merge pull request #145 from timm3/50-v0.28.0. [Jose Diaz-Gonzalez]

  #50 - refactor for friendlier import
- #50 update: keep main() in bin. [ethan]
- #50 - refactor for friendlier import. [ethan]


0.28.0 (2020-02-03)
-------------------
- Release version 0.28.0. [Jose Diaz-Gonzalez]
- Merge pull request #143 from smiley/patch-1. [Jose Diaz-Gonzalez]

  Remove deprecated (and removed) "git lfs fetch" flags
- Remove deprecated (and removed) git lfs flags. [smiley]

  "--tags" and "--force" were removed at some point from "git lfs fetch". This broke our backup script.


0.27.0 (2020-01-22)
-------------------
- Release version 0.27.0. [Jose Diaz-Gonzalez]
- Merge pull request #142 from einsteinx2/issue/141-import-error-
  version. [Jose Diaz-Gonzalez]

  Fixed script fails if not installed from pip
- Fixed script fails if not installed from pip. [Ben Baron]

  At the top of the script, the line from github_backup import __version__ gets the script's version number to use if the script is called with the -v or --version flags. The problem is that if the script hasn't been installed via pip (for example I cloned the repo directly to my backup server), the script will fail due to an import exception.

  Also presumably it will always use the version number from pip even if running a modified version from git or a fork or something, though this does not fix that as I have no idea how to check if it's running the pip installed version or not. But at least the script will now work fine if cloned from git or just copied to another machine.

  closes https://github.com/josegonzalez/python-github-backup/issues/141
- Merge pull request #136 from einsteinx2/issue/88-macos-keychain-
  broken-python3. [Jose Diaz-Gonzalez]

  Fixed macOS keychain access when using Python 3
- Fixed macOS keychain access when using Python 3. [Ben Baron]

  Python 3 is returning bytes rather than a string, so the string concatenation to create the auth variable was throwing an exception which the script was interpreting to mean it couldn't find the password. Adding a conversion to string first fixed the issue.
- Merge pull request #137 from einsteinx2/issue/134-only-use-auth-token-
  when-needed. [Jose Diaz-Gonzalez]

  Public repos no longer include the auth token
- Public repos no longer include the auth token. [Ben Baron]

  When backing up repositories using an auth token and https, the GitHub personal auth token is leaked in each backed up repository. It is included in the URL of each repository's git remote url.

  This is not needed as they are public and can be accessed without the token and can cause issues in the future if the token is ever changed, so I think it makes more sense not to have the token stored in each repo backup. I think the token should only be "leaked" like this out of necessity, e.g. it's a private repository and the --prefer-ssh option was not chosen so https with auth token was required to perform the clone.
- Merge pull request #130 from einsteinx2/issue/129-fix-crash-on-
  release-asset-download-error. [Jose Diaz-Gonzalez]

  Crash when an release asset doesn't exist
- Fixed comment typo. [Ben Baron]
- Switched log_info to log_warning in download_file. [Ben Baron]
- Crash when an release asset doesn't exist. [Ben Baron]

  Currently, the script crashes whenever a release asset is unable to download (for example a 404 response). This change instead logs the failure and allows the script to continue. No retry logic is enabled, but at least it prevents the crash and allows the backup to complete. Retry logic can be implemented later if wanted.

  closes https://github.com/josegonzalez/python-github-backup/issues/129
- Merge pull request #132 from einsteinx2/issue/126-prevent-overwriting-
  release-assets. [Jose Diaz-Gonzalez]

  Separate release assets and skip re-downloading
- Moved asset downloading loop inside the if block. [Ben Baron]
- Separate release assets and skip re-downloading. [Ben Baron]

  Currently the script puts all release assets into the same folder called `releases`. So any time 2 release files have the same name, only the last one downloaded is actually saved. A particularly bad example of this is MacDownApp/macdown where all of their releases are named `MacDown.app.zip`. So even though they have 36 releases and all 36 are downloaded, only the last one is actually saved.

  With this change, each releases' assets are now stored in a fubfolder inside `releases` named after the release name. There could still be edge cases if two releases have the same name, but this is still much safer tha the previous behavior.

  This change also now checks if the asset file already exists on disk and skips downloading it. This drastically speeds up addiotnal syncs as it no longer downloads every single release every single time. It will now only download new releases which I believe is the expected behavior.

  closes https://github.com/josegonzalez/python-github-backup/issues/126
- Merge pull request #131 from einsteinx2/improve-gitignore. [Jose Diaz-
  Gonzalez]

  Improved gitignore, macOS files and IDE configs
- Added newline to end of file. [Ben Baron]
- Improved gitignore, macOS files and IDE configs. [Ben Baron]

  Ignores the annoying hidden macOS files .DS_Store and ._* as well as the IDE configuration folders for contributors using the popular Visual Studio Code and Atom IDEs (more can be added later as needed).
- Update ISSUE_TEMPLATE.md. [Jose Diaz-Gonzalez]


0.26.0 (2019-09-23)
-------------------
- Release version 0.26.0. [Jose Diaz-Gonzalez]
- Merge pull request #128 from Snawoot/master. [Jose Diaz-Gonzalez]

  Workaround gist clone in `--prefer-ssh` mode
- Workaround gist clone in `--prefer-ssh` mode. [Vladislav Yarmak]
- Create PULL_REQUEST.md. [Jose Diaz-Gonzalez]
- Create ISSUE_TEMPLATE.md. [Jose Diaz-Gonzalez]
- Update README.rst. [Jose Diaz-Gonzalez]
- Update README.rst. [Jose Diaz-Gonzalez]


0.25.0 (2019-07-03)
-------------------
- Release version 0.25.0. [Jose Diaz-Gonzalez]
- Merge pull request #120 from 8h2a/patch-1. [Jose Diaz-Gonzalez]

  Issue 119: Change retrieve_data to be a generator
- Issue 119: Change retrieve_data to be a generator. [2a]

  See issue #119.


0.24.0 (2019-06-27)
-------------------
- Release version 0.24.0. [Jose Diaz-Gonzalez]
- Merge pull request #117 from QuicketSolutions/master. [Jose Diaz-
  Gonzalez]

  Add option for Releases
- Merge pull request #5 from QuicketSolutions/QKT-45. [Ethan Timm]
- QKT-45: include assets - update readme. [Ethan Timm]

  update readme with flag information for including assets alongside their respective releases
- Merge pull request #4 from whwright/wip-releases. [Ethan Timm]

  Download github assets
- Make assets it's own flag. [Harrison Wright]
- Fix super call for python2. [Harrison Wright]
- Fix redirect to s3. [Harrison Wright]
- WIP: download assets. [Harrison Wright]
- Merge pull request #3 from QuicketSolutions/QKT-42. [Ethan Timm]
- QKT-42: releases - add readme info. [ethan]
- Merge pull request #2 from QuicketSolutions/QKT-42. [Ethan Timm]

  QKT-42 update: shorter command flag
- QKT-42 update: shorter command flag. [ethan]
- Merge pull request #1 from QuicketSolutions/QKT-42. [Ethan Timm]
- QKT-42: support saving release information. [ethan]
- Merge pull request #118 from whwright/115-fix-pull-details. [Jose
  Diaz-Gonzalez]

  Fix pull details
- Fix pull details. [Harrison Wright]


0.23.0 (2019-06-04)
-------------------
- Release version 0.23.0. [Jose Diaz-Gonzalez]
- Merge pull request #113 from kleag/master. [Jose Diaz-Gonzalez]

  Avoid to crash in case of HTTP 502 error
- Avoid to crash in case of HTTP 502 error. [Gael de Chalendar]

  Survive also on socket.error connections like on HTTPError or URLError.

  This should solve issue #110.


0.22.2 (2019-02-21)
-------------------

Fix
~~~
- Warn instead of error. [Jose Diaz-Gonzalez]

  Refs #106

Other
~~~~~
- Release version 0.22.2. [Jose Diaz-Gonzalez]
- Merge pull request #107 from josegonzalez/patch-1. [Jose Diaz-
  Gonzalez]

  fix: warn instead of error


0.22.1 (2019-02-21)
-------------------
- Release version 0.22.1. [Jose Diaz-Gonzalez]
- Merge pull request #106 from jstetic/master. [Jose Diaz-Gonzalez]

  Log URL error
- Log URL error https://github.com/josegonzalez/python-github-
  backup/issues/105. [JOHN STETIC]


0.22.0 (2019-02-01)
-------------------
- Release version 0.22.0. [Jose Diaz-Gonzalez]
- Merge pull request #103 from whwright/98-better-logging. [Jose Diaz-
  Gonzalez]

  Fix accidental system exit with better logging strategy
- Remove unnecessary sys.exit call. [W. Harrison Wright]
- Add org check to avoid incorrect log output. [W. Harrison Wright]
- Fix accidental system exit with better logging strategy. [W. Harrison
  Wright]


0.21.1 (2018-12-25)
-------------------
- Release version 0.21.1. [Jose Diaz-Gonzalez]
- Merge pull request #101 from ecki/patch-2. [Jose Diaz-Gonzalez]

  Mark options which are not included in --all
- Mark options which are not included in --all. [Bernd]

  As discussed in Issue #100


0.21.0 (2018-11-28)
-------------------
- Release version 0.21.0. [Jose Diaz-Gonzalez]
- Merge pull request #97 from whwright/94-fix-user-repos. [Jose Diaz-
  Gonzalez]

  Correctly download repos when user arg != authenticated user
- Correctly download repos when user arg != authenticated user. [W.
  Harrison Wright]


0.20.1 (2018-09-29)
-------------------
- Release version 0.20.1. [Jose Diaz-Gonzalez]
- Merge pull request #92 from whwright/87-fix-starred-bug. [Jose Diaz-
  Gonzalez]

  Clone the specified user's starred repos/gists, not the authenticated user
- Clone the specified user's gists, not the authenticated user. [W.
  Harrison Wright]
- Clone the specified user's starred repos, not the authenticated user.
  [W. Harrison Wright]


0.20.0 (2018-03-24)
-------------------
- Release version 0.20.0. [Jose Diaz-Gonzalez]
- Chore: drop Python 2.6. [Jose Diaz-Gonzalez]
- Feat: simplify release script. [Jose Diaz-Gonzalez]


0.19.2 (2018-03-24)
-------------------

Fix
~~~
- Cleanup pep8 violations. [Jose Diaz-Gonzalez]

Other
~~~~~
- Release version 0.19.2. [Jose Diaz-Gonzalez]


0.19.1 (2018-03-24)
-------------------
- Release version 0.19.1. [Jose Diaz-Gonzalez]


0.19.0 (2018-03-24)
-------------------
- Release version 0.19.0. [Jose Diaz-Gonzalez]
- Merge pull request #77 from mayflower/pull-details. [Jose Diaz-
  Gonzalez]

  Pull Details
- Add additional output for the current request. [Robin Gloster]

  This is useful to have some progress indication for huge repositories.
- Add option to backup additional PR details. [Robin Gloster]

  Some payload is only included when requesting a single pull request
- Merge pull request #84 from johbo/fix-python36-skip-existing. [Jose
  Diaz-Gonzalez]

  Mark string as binary in comparison for skip_existing
- Mark string as binary in comparison for skip_existing. [Johannes
  Bornhold]

  Found out that the flag "--skip-existing" did not work out as expected on Python
  3.6. Tracked it down to the comparison which has to be against a string of bytes
  in Python3.


0.18.0 (2018-02-22)
-------------------
- Release version 0.18.0. [Jose Diaz-Gonzalez]
- Merge pull request #82 from sgreene570/add-followers. [Jose Diaz-
  Gonzalez]

  Add option to fetch followers/following JSON data
- Add option to fetch followers/following JSON data. [Stephen Greene]


0.17.0 (2018-02-20)
-------------------
- Release version 0.17.0. [Jose Diaz-Gonzalez]
- Merge pull request #81 from whwright/gists. [Jose Diaz-Gonzalez]

  Add ability to back up gists
- Short circuit gists backup process. [W. Harrison Wright]
- Formatting. [W. Harrison Wright]
- Add ability to backup gists. [W. Harrison Wright]


0.16.0 (2018-01-22)
-------------------
- Release version 0.16.0. [Jose Diaz-Gonzalez]
- Merge pull request #78 from whwright/clone-starred-repos. [Jose Diaz-
  Gonzalez]

  Clone starred repos
- Update README.rst. [Jose Diaz-Gonzalez]
- Update documentation. [W. Harrison Wright]
- Change option to --all-starred. [W. Harrison Wright]
- JK don't update documentation. [W. Harrison Wright]
- Update documentation. [W. Harrison Wright]
- Put starred clone repoistories under a new option. [W. Harrison
  Wright]
- Add comment. [W. Harrison Wright]
- Add ability to clone starred repos. [W. Harrison Wright]


0.15.0 (2017-12-11)
-------------------
- Release version 0.15.0. [Jose Diaz-Gonzalez]
- Merge pull request #75 from slibby/slibby-patch-windows. [Jose Diaz-
  Gonzalez]

  update check_io() to allow scripts to run on Windows
- Update logging_subprocess function. [Sam Libby]

  1. added newline for return
  2. added one-time warning (once per subprocess)
- Update check_io() to allow scripts to run on Windows. [Sam Libby]


0.14.1 (2017-10-11)
-------------------
- Release version 0.14.1. [Jose Diaz-Gonzalez]
- Merge pull request #70 from epfremmer/patch-1. [Jose Diaz-Gonzalez]

  Fix arg not defined error
- Fix arg not defined error. [Edward Pfremmer]


0.14.0 (2017-10-11)
-------------------
- Release version 0.14.0. [Jose Diaz-Gonzalez]
- Merge pull request #68 from pieterclaerhout/master. [Jose Diaz-
  Gonzalez]

  Added support for LFS clones
- Updated the readme. [pieterclaerhout]
- Added a check to see if git-lfs is installed when doing an LFS clone.
  [pieterclaerhout]
- Added support for LFS clones. [pieterclaerhout]
- Merge pull request #66 from albertyw/python3. [Jose Diaz-Gonzalez]

  Explicitly support python 3
- Add pypi info to readme. [Albert Wang]
- Explicitly support python 3 in package description. [Albert Wang]
- Merge pull request #65 from mumblez/master. [Jose Diaz-Gonzalez]

  add couple examples to help new users
- Add couple examples to help new users. [Yusuf Tran]


0.13.2 (2017-05-06)
-------------------
- Release version 0.13.2. [Jose Diaz-Gonzalez]
- Merge pull request #64 from karlicoss/fix-remotes. [Jose Diaz-
  Gonzalez]

  Fix remotes while updating repository
- Fix remotes while updating repository. [Dima Gerasimov]


0.13.1 (2017-04-11)
-------------------
- Release version 0.13.1. [Jose Diaz-Gonzalez]
- Merge pull request #61 from McNetic/fix_empty_updated_at. [Jose Diaz-
  Gonzalez]

  Fix error when repository has no updated_at value
- Fix error when repository has no updated_at value. [Nicolai Ehemann]


0.13.0 (2017-04-05)
-------------------
- Release version 0.13.0. [Jose Diaz-Gonzalez]
- Merge pull request #59 from martintoreilly/master. [Jose Diaz-
  Gonzalez]

  Add support for storing PAT in OSX keychain
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
- Release version 0.12.1. [Jose Diaz-Gonzalez]
- Merge pull request #57 from acdha/reuse-existing-remotes. [Jose Diaz-
  Gonzalez]

  Avoid remote branch name churn
- Avoid remote branch name churn. [Chris Adams]

  This avoids the backup output having lots of "[new branch]" messages
  because removing the old remote name removed all of the existing branch
  references.
- Merge pull request #55 from amaczuga/master. [Jose Diaz-Gonzalez]

  Fix detection of bare git directories
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
- Release version 0.12.0. [Jose Diaz-Gonzalez]
- Pep8: E501 line too long (83 > 79 characters) [Jose Diaz-Gonzalez]
- Pep8: E128 continuation line under-indented for visual indent. [Jose
  Diaz-Gonzalez]
- Merge pull request #54 from amaczuga/master. [Jose Diaz-Gonzalez]

  Support archivization using bare git clones
- Support archivization using bare git clones. [Andrzej Maczuga]
- Merge pull request #53 from trel/master. [Jose Diaz-Gonzalez]

  fix typo, 3x
- Fix typo, 3x. [Terrell Russell]


0.11.0 (2016-10-26)
-------------------
- Release version 0.11.0. [Jose Diaz-Gonzalez]
- Merge pull request #52 from bjodah/fix-gh-51. [Jose Diaz-Gonzalez]

  Support --token file:///home/user/token.txt (fixes gh-51)
- Support --token file:///home/user/token.txt (fixes gh-51) [Björn
  Dahlgren]
- Merge pull request #48 from albertyw/python3. [Jose Diaz-Gonzalez]

  Support Python 3
- Fix some linting. [Albert Wang]
- Fix byte/string conversion for python 3. [Albert Wang]
- Support python 3. [Albert Wang]
- Merge pull request #46 from remram44/encode-password. [Jose Diaz-
  Gonzalez]

  Encode special characters in password
- Encode special characters in password. [Remi Rampin]
- Merge pull request #45 from remram44/cli-programname. [Jose Diaz-
  Gonzalez]

  Fix program name
- Update README.rst. [Remi Rampin]
- Don't pretend program name is "Github Backup" [Remi Rampin]
- Merge pull request #44 from remram44/readme-git-https. [Jose Diaz-
  Gonzalez]

  Don't install over insecure connection
- Don't install over insecure connection. [Remi Rampin]

  The git:// protocol is unauthenticated and unencrypted, and no longer advertised by GitHub. Using HTTPS shouldn't impact performance.


0.10.3 (2016-08-21)
-------------------
- Release version 0.10.3. [Jose Diaz-Gonzalez]
- Merge pull request #30 from jonasrmichel/master. [Jose Diaz-Gonzalez]

  Fixes #29
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
- Release version 0.10.2. [Jose Diaz-Gonzalez]
- Add a note regarding git version requirement. [Jose Diaz-Gonzalez]

  Closes #37


0.10.1 (2016-08-21)
-------------------
- Release version 0.10.1. [Jose Diaz-Gonzalez]


0.10.0 (2016-08-18)
-------------------
- Release version 0.10.0. [Jose Diaz-Gonzalez]
- Merge pull request #42 from robertwb/master. [Jose Diaz-Gonzalez]

  Implement incremental updates
- Implement incremental updates. [Robert Bradshaw]

  Guarded with an --incremental flag.

  Stores the time of the last update and only downloads issue and
  pull request data since this time.  All other data is relatively
  small (likely fetched with a single request) and so is simply
  re-populated from scratch as before.


0.9.0 (2016-03-29)
------------------
- Release version 0.9.0. [Jose Diaz-Gonzalez]
- Merge pull request #36 from zlabjp/fix-cloning-private-repos. [Jose
  Diaz-Gonzalez]

  Fix cloning private repos with basic auth or token
- Fix cloning private repos with basic auth or token. [Kazuki Suda]


0.8.0 (2016-02-14)
------------------
- Release version 0.8.0. [Jose Diaz-Gonzalez]
- Merge pull request #35 from eht16/issue23_store_pullrequests_once.
  [Jose Diaz-Gonzalez]

  Don't store issues which are actually pull requests
- Don't store issues which are actually pull requests. [Enrico Tröger]

  This prevents storing pull requests twice since the Github API returns
  pull requests also as issues. Those issues will be skipped but only if
  retrieving pull requests is requested as well.
  Closes #23.


0.7.0 (2016-02-02)
------------------
- Release version 0.7.0. [Jose Diaz-Gonzalez]
- Merge pull request #32 from albertyw/soft-fail-hooks. [Jose Diaz-
  Gonzalez]

  Softly fail if not able to read hooks
- Softly fail if not able to read hooks. [Albert Wang]
- Merge pull request #33 from albertyw/update-readme. [Jose Diaz-
  Gonzalez]

  Add note about 2-factor auth in readme
- Add note about 2-factor auth. [Albert Wang]
- Merge pull request #31 from albertyw/fix-private-repos. [Jose Diaz-
  Gonzalez]

  Fix reading user's private repositories
- Make user repository search go through endpoint capable of reading
  private repositories. [Albert Wang]
- Merge pull request #28 from alexmojaki/getpass. [Jose Diaz-Gonzalez]

  Prompt for password if only username given
- Update README with new CLI usage. [Alex Hall]
- Prompt for password if only username given. [Alex Hall]


0.6.0 (2015-11-10)
------------------
- Release version 0.6.0. [Jose Diaz-Gonzalez]
- Force proper remote url. [Jose Diaz-Gonzalez]
- Merge pull request #24 from eht16/add_backup_hooks. [Jose Diaz-
  Gonzalez]

  Add backup hooks
- Improve error handling in case of HTTP errors. [Enrico Tröger]

  In case of a HTTP status code 404, the returned 'r' was never assigned.
  In case of URL errors which are not timeouts, we probably should bail
  out.
- Add --hooks to also include web hooks into the backup. [Enrico Tröger]
- Merge pull request #22 from eht16/issue_17_create_output_directory.
  [Jose Diaz-Gonzalez]

  Create the user specified output directory if it does not exist
- Create the user specified output directory if it does not exist.
  [Enrico Tröger]

  Fixes #17.
- Merge pull request #21 from eht16/fix_get_response_missing_auth. [Jose
  Diaz-Gonzalez]

  Add missing auth argument to _get_response()
- Add missing auth argument to _get_response() [Enrico Tröger]

  When running unauthenticated and Github starts rate-limiting the client,
  github-backup crashes because the used auth variable in _get_response()
  was not available. This change should fix it.
- Merge pull request #20 from
  eht16/improve_error_msg_on_non_existing_repo. [Jose Diaz-Gonzalez]

  Add repository URL to error message for non-existing repositories
- Add repository URL to error message for non-existing repositories.
  [Enrico Tröger]

  This makes it easier for the user to identify which repository does not
  exist or is not initialised, i.e. whether it is the main repository or
  the wiki repository and which clone URL was used to check.


0.5.0 (2015-10-10)
------------------
- Release version 0.5.0. [Jose Diaz-Gonzalez]
- Add release script. [Jose Diaz-Gonzalez]
- Refactor to both simplify codepath as well as follow PEP8 standards.
  [Jose Diaz-Gonzalez]
- Merge pull request #19 from Embed-Engineering/retry-timeout. [Jose
  Diaz-Gonzalez]

  Retry 3 times when the connection times out
- Retry 3 times when the connection times out. [Mathijs Jonker]
- Merge pull request #15 from kromkrom/master. [Jose Diaz-Gonzalez]

  Preserve Unicode characters in the output file
- Update github-backup. [Kirill Grushetsky]
- Update github-backup. [Kirill Grushetsky]
- Made unicode output defalut. [Kirill Grushetsky]
- Import alphabetised. [Kirill Grushetsky]
- Preserve Unicode characters in the output file. [Kirill Grushetsky]

  Added option to preserve Unicode characters in the output file
- Merge pull request #14 from aensley/master. [Jose Diaz-Gonzalez]

  Added backup of labels and milestones.
- Josegonzales/python-github-backup#12 Added backup of labels and
  milestones. [aensley]
- Merge pull request #11 from Embed-Engineering/master. [Jose Diaz-
  Gonzalez]

  Added test for uninitialized repo's (or wiki's)
- Fixed indent. [Mathijs Jonker]
- Update github-backup. [mjonker-embed]
- Skip unitialized repo's. [mjonker-embed]

  These gave me errors which caused mails from crontab.
- Merge pull request #10 from Embed-Engineering/master. [Jose Diaz-
  Gonzalez]

  Added prefer-ssh
- Added prefer-ssh. [mjonker-embed]

  Was needed for my back-up setup, code includes this but readme wasn't updated
- Merge pull request #9 from acdha/ratelimit-retries. [Jose Diaz-
  Gonzalez]

  Retry API requests which failed due to rate-limiting
- Retry API requests which failed due to rate-limiting. [Chris Adams]

  This allows operation to continue, albeit at a slower pace,
  if you have enough data to trigger the API rate limits
- Release 0.4.0. [Jose Diaz-Gonzalez]
- Merge pull request #7 from acdha/repo-backup-overhaul. [Jose Diaz-
  Gonzalez]

  Repo backup overhaul
- Update repository back up handling for wikis. [Chris Adams]

  * Now wikis will follow the same logic as the main repo
    checkout for --prefer-ssh.
  * The regular repository and wiki paths both use the same
    function to handle either cloning or updating a local copy
    of the remote repo
  * All git updates will now use “git fetch --all --tags”
    to ensure that tags and branches other than master will
    also be backed up
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
- Merge pull request #6 from acdha/allow-clone-over-ssh. [Jose Diaz-
  Gonzalez]

  Add an option to prefer checkouts over SSH
- Add an option to prefer checkouts over SSH. [Chris Adams]

  This is really useful with private repos to avoid being nagged
  for credentials for every repository
- Release 0.3.0. [Jose Diaz-Gonzalez]
- Merge pull request #4 from klaude/pull_request_support. [Jose Diaz-
  Gonzalez]

  Add pull request support
- Add pull request support. [Kevin Laude]

  Back up reporitory pull requests by passing the --include-pulls
  argument. Pull requests are saved to
  repositories/<repository name>/pulls/<pull request number>.json. Include
  the --pull-request-comments argument to add review comments to the pull
  request backup and pass the --pull-request-commits argument to add
  commits to the pull request backup.

  Pull requests are automatically backed up when the --all argument is
  uesd.
- Merge pull request #5 from klaude/github-enterprise-support. [Jose
  Diaz-Gonzalez]

  Add GitHub Enterprise Support
- Add GitHub Enterprise support. [Kevin Laude]

  Pass the -H or --github-host argument with a GitHub Enterprise hostname
  to backup from that GitHub enterprise host. If no argument is passed
  then back up from github.com.


0.2.0 (2014-09-22)
------------------
- Release 0.2.0. [Jose Diaz-Gonzalez]
- Add support for retrieving repositories. Closes #1. [Jose Diaz-
  Gonzalez]
- Fix PEP8 violations. [Jose Diaz-Gonzalez]
- Merge pull request #2 from johnyf/master. [Jose Diaz-Gonzalez]

  add authorization to header only if specified by user
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



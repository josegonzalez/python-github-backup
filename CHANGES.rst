Changelog
=========

0.31.0 (2020-02-25)
-------------------
------------------------
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



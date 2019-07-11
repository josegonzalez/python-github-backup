=============
github-backup
=============

|PyPI| |Python Versions|

    This project is considered feature complete for the primary maintainer. If you would like a bugfix or enhancement and cannot sponsor the work, pull requests are welcome. Feel free to contact the maintainer for consulting estimates if desired.

backup a github user or organization

Requirements
============

- GIT 1.9+

Installation
============

Using PIP via PyPI::

    pip install github-backup

Using PIP via Github::

    pip install git+https://github.com/josegonzalez/python-github-backup.git#egg=github-backup

Usage
=====

CLI Usage is as follows::

    github-backup [-h] [-u USERNAME] [-p PASSWORD] [-t TOKEN]
                  [-o OUTPUT_DIRECTORY] [-i] [--starred] [--all-starred]
                  [--watched] [--followers] [--following] [--all]
                  [--issues] [--issue-comments] [--issue-events] [--pulls]
                  [--pull-comments] [--pull-commits] [--labels] [--hooks]
                  [--milestones] [--repositories] [--releases] [--assets]
                  [--bare] [--lfs] [--wikis] [--gists] [--starred-gists]
                  [--skip-existing]
                  [-L [LANGUAGES [LANGUAGES ...]]] [-N NAME_REGEX]
                  [-H GITHUB_HOST] [-O] [-R REPOSITORY] [-P] [-F]
                  [--prefer-ssh] [-v]
                  [--keychain-name OSX_KEYCHAIN_ITEM_NAME]
                  [--keychain-account OSX_KEYCHAIN_ITEM_ACCOUNT]
                  USER

    Backup a github account

    positional arguments:
      USER                  github username

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
                            username for basic auth
      -p PASSWORD, --password PASSWORD
                            password for basic auth. If a username is given but
                            not a password, the password will be prompted for.
      -t TOKEN, --token TOKEN
                            personal access or OAuth token, or path to token
                            (file://...)
      -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                            directory at which to backup the repositories
      -i, --incremental     incremental backup
      --starred             include JSON output of starred repositories in backup
      --all-starred         include starred repositories in backup
      --watched             include watched repositories in backup
      --followers           include JSON output of followers in backup
      --following           include JSON output of following users in backup
      --all                 include everything in backup
      --issues              include issues in backup
      --issue-comments      include issue comments in backup
      --issue-events        include issue events in backup
      --pulls               include pull requests in backup
      --pull-comments       include pull request review comments in backup
      --pull-commits        include pull request commits in backup
      --labels              include labels in backup
      --hooks               include hooks in backup (works only when
                            authenticated)
      --milestones          include milestones in backup
      --repositories        include repository clone in backup
      --releases            include repository releases' information without assets or binaries
      --assets              include assets alongside release information; only applies if including releases
      --bare                clone bare repositories
      --lfs                 clone LFS repositories (requires Git LFS to be
                            installed, https://git-lfs.github.com)
      --wikis               include wiki clone in backup
      --gists               include gists in backup
      --starred-gists       include starred gists in backup
      --skip-existing       skip project if a backup directory exists
      -L [LANGUAGES [LANGUAGES ...]], --languages [LANGUAGES [LANGUAGES ...]]
                            only allow these languages
      -N NAME_REGEX, --name-regex NAME_REGEX
                            python regex to match names against
      -H GITHUB_HOST, --github-host GITHUB_HOST
                            GitHub Enterprise hostname
      -O, --organization    whether or not this is an organization user
      -R REPOSITORY, --repository REPOSITORY
                            name of repository to limit backup to
      -P, --private         include private repositories
      -F, --fork            include forked repositories
      --prefer-ssh          Clone repositories using SSH instead of HTTPS
      -v, --version         show program's version number and exit
      --keychain-name OSX_KEYCHAIN_ITEM_NAME
                            OSX ONLY: name field of password item in OSX keychain
                            that holds the personal access or OAuth token
      --keychain-account OSX_KEYCHAIN_ITEM_ACCOUNT
                            OSX ONLY: account field of password item in OSX
                            keychain that holds the personal access or OAuth token


The package can be used to backup an *entire* organization or repository, including issues and wikis in the most appropriate format (clones for wikis, json files for issues).

Authentication
==============

Note: Password-based authentication will fail if you have two-factor authentication enabled.

Using the Keychain on Mac OSX
=============================
Note: On Mac OSX the token can be stored securely in the user's keychain. To do this:

1. Open Keychain from "Applications -> Utilities -> Keychain Access"
2. Add a new password item using "File -> New Password Item"
3. Enter a name in the "Keychain Item Name" box. You must provide this name to github-backup using the --keychain-name argument.
4. Enter an account name in the "Account Name" box, enter your Github username as set above. You must provide this name to github-backup using the --keychain-account argument.
5. Enter your Github personal access token in the "Password" box

Note:  When you run github-backup, you will be asked whether you want to allow "security" to use your confidential information stored in your keychain. You have two options:

1. **Allow:** In this case you will need to click "Allow" each time you run `github-backup`
2. **Always Allow:** In this case, you will not be asked for permission when you run `github-backup` in future. This is less secure, but is required if you want to schedule `github-backup` to run automatically

About Git LFS
=============

When you use the "--lfs" option, you will need to make sure you have Git LFS installed.

Instructions on how to do this can be found on https://git-lfs.github.com.

Examples
========

Backup all repositories::

    export ACCESS_TOKEN=SOME-GITHUB-TOKEN
    github-backup WhiteHouse --token $ACCESS_TOKEN --organization --output-directory /tmp/white-house --repositories

Backup a single organization repository with everything else (wiki, pull requests, comments, issues etc)::

    export ACCESS_TOKEN=SOME-GITHUB-TOKEN
    ORGANIZATION=docker
    REPO=cli
    # e.g. git@github.com:docker/cli.git
    github-backup $ORGANIZATION -P -t $ACCESS_TOKEN -o . --all -O -R $REPO

.. |PyPI| image:: https://img.shields.io/pypi/v/github-backup.svg
   :target: https://pypi.python.org/pypi/github-backup/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/github-backup.svg
   :target: https://github.com/albertyw/github-backup

=============
github-backup
=============

backup a github user or organization

Installation
============

Using PIP via PyPI::

    pip install github-backup

Using PIP via Github::

    pip install git+git://github.com/josegonzalez/python-github-backup.git#egg=github-backup

Usage
=====

CLI Usage is as follows::

    Github Backup [-h] [-u USERNAME] [-p PASSWORD] [-t TOKEN]
                     [-o OUTPUT_DIRECTORY] [--starred] [--watched] [--all]
                     [--issues] [--issue-comments] [--issue-events] [--pulls]
                     [--pull-comments] [--pull-commits] [--labels] [--hooks]
                     [--milestones] [--repositories] [--wikis]
                     [--skip-existing] [-L [LANGUAGES [LANGUAGES ...]]]
                     [-N NAME_REGEX] [-H GITHUB_HOST] [-O] [-R REPOSITORY]
                     [-P] [-F] [--prefer-ssh] [-v]
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
                            personal access or OAuth token
      -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                            directory at which to backup the repositories
      --starred             include starred repositories in backup
      --watched             include watched repositories in backup
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
      --wikis               include wiki clone in backup
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


The package can be used to backup an *entire* organization or repository, including issues and wikis in the most appropriate format (clones for wikis, json files for issues).

Authentication
==============

Note: Password-based authentication will fail if you have two-factor authentication enabled.

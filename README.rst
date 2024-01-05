=============
github-backup
=============

|PyPI| |Python Versions|

The package can be used to backup an *entire* `Github <https://github.com/>`_ organization, repository or user account, including starred repos, issues and wikis in the most appropriate format (clones for wikis, json files for issues).

Requirements
============

- GIT 1.9+
- Python

Installation
============

Using PIP via PyPI::

    pip install github-backup

Using PIP via Github (more likely the latest version)::

    pip install git+https://github.com/josegonzalez/python-github-backup.git#egg=github-backup
    
*Install note for python newcomers:*

Python scripts are unlikely to be included in your ``$PATH`` by default, this means it cannot be run directly in terminal with ``$ github-backup ...``, you can either add python's install path to your environments ``$PATH`` or call the script directly e.g. using ``$ ~/.local/bin/github-backup``.*

Basic Help
==========

Show the CLI help output::

    github-backup -h

CLI Help output::

    github-backup [-h] [-u USERNAME] [-p PASSWORD] [-t TOKEN_CLASSIC]
                  [-f TOKEN_FINE] [--as-app] [-o OUTPUT_DIRECTORY]
                  [-l LOG_LEVEL] [-i] [--starred] [--all-starred]
                  [--watched] [--followers] [--following] [--all] [--issues]
                  [--issue-comments] [--issue-events] [--pulls]
                  [--pull-comments] [--pull-commits] [--pull-details]
                  [--labels] [--hooks] [--milestones] [--repositories]
                  [--bare] [--lfs] [--wikis] [--gists] [--starred-gists]
                  [--skip-archived] [--skip-existing] [-L [LANGUAGES ...]]
                  [-N NAME_REGEX] [-H GITHUB_HOST] [-O] [-R REPOSITORY]
                  [-P] [-F] [--prefer-ssh] [-v]
                  [--keychain-name OSX_KEYCHAIN_ITEM_NAME]
                  [--keychain-account OSX_KEYCHAIN_ITEM_ACCOUNT]
                  [--releases] [--latest-releases NUMBER_OF_LATEST_RELEASES]
                  [--skip-prerelease] [--assets]
                  [--exclude [REPOSITORY [REPOSITORY ...]]
                  [--throttle-limit THROTTLE_LIMIT] [--throttle-pause THROTTLE_PAUSE]
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
      -f TOKEN_FINE, --token-fine TOKEN_FINE
                            fine-grained personal access token or path to token
                            (file://...)
      -t TOKEN_CLASSIC, --token TOKEN_CLASSIC
                            personal access, OAuth, or JSON Web token, or path to
                            token (file://...)
      --as-app              authenticate as github app instead of as a user.
      -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                            directory at which to backup the repositories
      -l LOG_LEVEL, --log-level LOG_LEVEL
                            log level to use (default: info, possible levels:
                            debug, info, warning, error, critical)
      -i, --incremental     incremental backup
      --starred             include JSON output of starred repositories in backup
      --all-starred         include starred repositories in backup [*]
      --watched             include JSON output of watched repositories in backup
      --followers           include JSON output of followers in backup
      --following           include JSON output of following users in backup
      --all                 include everything in backup (not including [*])
      --issues              include issues in backup
      --issue-comments      include issue comments in backup
      --issue-events        include issue events in backup
      --pulls               include pull requests in backup
      --pull-comments       include pull request review comments in backup
      --pull-commits        include pull request commits in backup
      --pull-details        include more pull request details in backup [*]
      --labels              include labels in backup
      --hooks               include hooks in backup (works only when
                            authenticated)
      --milestones          include milestones in backup
      --repositories        include repository clone in backup
      --bare                clone bare repositories
      --lfs                 clone LFS repositories (requires Git LFS to be
                            installed, https://git-lfs.github.com) [*]
      --wikis               include wiki clone in backup
      --gists               include gists in backup [*]
      --starred-gists       include starred gists in backup [*]
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
      -P, --private         include private repositories [*]
      -F, --fork            include forked repositories [*]
      --prefer-ssh          Clone repositories using SSH instead of HTTPS
      -v, --version         show program's version number and exit
      --keychain-name OSX_KEYCHAIN_ITEM_NAME
                            OSX ONLY: name field of password item in OSX keychain
                            that holds the personal access or OAuth token
      --keychain-account OSX_KEYCHAIN_ITEM_ACCOUNT
                            OSX ONLY: account field of password item in OSX
                            keychain that holds the personal access or OAuth token
      --releases            include release information, not including assets or
                            binaries
      --latest-releases NUMBER_OF_LATEST_RELEASES
                            include certain number of the latest releases;
                            only applies if including releases
      --skip-prerelease     skip prerelease and draft versions; only applies if including releases
      --assets              include assets alongside release information; only
                            applies if including releases
      --exclude [REPOSITORY [REPOSITORY ...]]
                            names of repositories to exclude from backup.
      --throttle-limit THROTTLE_LIMIT
                            start throttling of GitHub API requests after this
                            amount of API requests remain
      --throttle-pause THROTTLE_PAUSE
                            wait this amount of seconds when API request
                            throttling is active (default: 30.0, requires
                            --throttle-limit to be set)


Usage Details
=============

Authentication
--------------

**Password-based authentication** will fail if you have two-factor authentication enabled, and will `be deprecated <https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/>`_ by 2023 EOY.

``--username`` is used for basic password authentication and separate from the positional argument ``USER``, which specifies the user account you wish to back up.

**Classic tokens** are `slightly less secure <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#personal-access-tokens-classic>`_ as they provide very coarse-grained permissions.

If you need authentication for long-running backups (e.g. for a cron job) it is recommended to use **fine-grained personal access token** ``-f TOKEN_FINE``.


Fine Tokens
~~~~~~~~~~~

You can "generate new token", choosing the repository scope by selecting specific repos or all repos. On Github this is under *Settings -> Developer Settings -> Personal access tokens -> Fine-grained Tokens*

Customise the permissions for your use case, but for a personal account full backup you'll need to enable the following permissions:

**User permissions**: Read access to followers, starring, and watching.

**Repository permissions**: Read access to code, commit statuses, issues, metadata, pages, pull requests, and repository hooks.


Prefer SSH
~~~~~~~~~~

If cloning repos is enabled with ``--repositories``, ``--all-starred``, ``--wikis``, ``--gists``, ``--starred-gists`` using the ``--prefer-ssh`` argument will use ssh for cloning the git repos, but all other connections will still use their own protocol, e.g. API requests for issues uses HTTPS.

To clone with SSH, you'll need SSH authentication setup `as usual with Github <https://docs.github.com/en/authentication/connecting-to-github-with-ssh>`_, e.g. via SSH public and private keys.


Using the Keychain on Mac OSX
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note: On Mac OSX the token can be stored securely in the user's keychain. To do this:

1. Open Keychain from "Applications -> Utilities -> Keychain Access"
2. Add a new password item using "File -> New Password Item"
3. Enter a name in the "Keychain Item Name" box. You must provide this name to github-backup using the --keychain-name argument.
4. Enter an account name in the "Account Name" box, enter your Github username as set above. You must provide this name to github-backup using the --keychain-account argument.
5. Enter your Github personal access token in the "Password" box

Note:  When you run github-backup, you will be asked whether you want to allow "security" to use your confidential information stored in your keychain. You have two options:

1. **Allow:** In this case you will need to click "Allow" each time you run `github-backup`
2. **Always Allow:** In this case, you will not be asked for permission when you run `github-backup` in future. This is less secure, but is required if you want to schedule `github-backup` to run automatically


Github Rate-limit and Throttling
--------------------------------

"github-backup" will automatically throttle itself based on feedback from the Github API. 

Their API is usually rate-limited to 5000 calls per hour. The API will ask github-backup to pause until a specific time when the limit is reset again (at the start of the next hour). This continues until the backup is complete.

During a large backup, such as ``--all-starred``, and on a fast connection this can result in (~20 min) pauses with bursts of API calls periodically maxing out the API limit. If this is not suitable `it has been observed <https://github.com/josegonzalez/python-github-backup/issues/76#issuecomment-636158717>`_ under real-world conditions that overriding the throttle with ``--throttle-limit 5000 --throttle-pause 0.6`` provides a smooth rate across the hour, although a ``--throttle-pause 0.72`` (3600 seconds [1 hour] / 5000 limit) is theoretically safer to prevent large rate-limit pauses.


About Git LFS
-------------

When you use the ``--lfs`` option, you will need to make sure you have Git LFS installed.

Instructions on how to do this can be found on https://git-lfs.github.com.


Gotchas / Known-issues
======================

All is not everything
---------------------

The ``--all`` argument does not include; cloning private repos (``-P, --private``), cloning forks (``-F, --fork``) cloning starred repositories (``--all-starred``), ``--pull-details``, cloning LFS repositories (``--lfs``), cloning gists (``--starred-gists``) or cloning starred gist repos (``--starred-gists``). See examples for more.

Cloning all starred size
------------------------

Using the ``--all-starred`` argument to clone all starred repositories may use a large amount of storage space, especially if ``--all`` or more arguments are used. e.g. commonly starred repos can have tens of thousands of issues, many large assets and the repo itself etc. Consider just storing links to starred repos in JSON format with ``--starred``.

Incremental Backup
------------------

Using (``-i, --incremental``) will only request new data from the API **since the last run (successful or not)**. e.g. only request issues from the API since the last run. 

This means any blocking errors on previous runs can cause a large amount of missing data in backups.

Known blocking errors
---------------------

Some errors will block the backup run by exiting the script. e.g. receiving a 403 Forbidden error from the Github API.

If the incremental argument is used, this will result in the next backup only requesting API data since the last blocked/failed run. Potentially causing unexpected large amounts of missing data.

It's therefore recommended to only use the incremental argument if the output/result is being actively monitored, or complimented with periodic full non-incremental runs, to avoid unexpected missing data in a regular backup runs.

1. **Starred public repo hooks blocking**

   Since the ``--all`` argument includes ``--hooks``, if you use ``--all`` and ``--all-starred`` together to clone a users starred public repositories, the backup will likely error and block the backup continuing. 

   This is due to needing the correct permission for ``--hooks`` on public repos.

2. **Releases blocking**

   A known ``--releases`` (required for ``--assets``) error will sometimes block the backup. 

   If you're backing up a lot of repositories with releases e.g. an organisation or ``--all-starred``. You may need to remove ``--releases`` (and therefore ``--assets``) to complete a backup. Documented in `issue 209 <https://github.com/josegonzalez/python-github-backup/issues/209>`_.


"bare" is actually "mirror"
---------------------------

Using the bare clone argument (``--bare``) will actually call git's ``clone --mirror`` command. There's a subtle difference between `bare <https://www.git-scm.com/docs/git-clone#Documentation/git-clone.txt---bare>`_ and `mirror <https://www.git-scm.com/docs/git-clone#Documentation/git-clone.txt---mirror>`_ clone.

*From git docs "Compared to --bare, --mirror not only maps local branches of the source to local branches of the target, it maps all refs (including remote-tracking branches, notes etc.) and sets up a refspec configuration such that all these refs are overwritten by a git remote update in the target repository."*


Starred gists vs starred repo behaviour
---------------------------------------

The starred normal repo cloning (``--all-starred``) argument stores starred repos separately to the users own repositories. However, using ``--starred-gists`` will store starred gists within the same directory as the users own gists ``--gists``. Also, all gist repo directory names are IDs not the gist's name.


Skip existing on incomplete backups
-----------------------------------

The ``--skip-existing`` argument will skip a backup if the directory already exists, even if the backup in that directory failed (perhaps due to a blocking error). This may result in unexpected missing data in a regular backup.


Github Backup Examples
======================

Backup all repositories, including private ones using a classic token::

    export ACCESS_TOKEN=SOME-GITHUB-TOKEN
    github-backup WhiteHouse --token $ACCESS_TOKEN --organization --output-directory /tmp/white-house --repositories --private

Use a fine-grained access token to backup a single organization repository with everything else (wiki, pull requests, comments, issues etc)::

    export FINE_ACCESS_TOKEN=SOME-GITHUB-TOKEN
    ORGANIZATION=docker
    REPO=cli
    # e.g. git@github.com:docker/cli.git
    github-backup $ORGANIZATION -P -f $FINE_ACCESS_TOKEN -o . --all -O -R $REPO

Quietly and incrementally backup useful Github user data (public and private repos with SSH) including; all issues, pulls, all public starred repos and gists (omitting "hooks", "releases" and therefore "assets" to prevent blocking). *Great for a cron job.* ::

    export FINE_ACCESS_TOKEN=SOME-GITHUB-TOKEN
    GH_USER=YOUR-GITHUB-USER

    github-backup -f $FINE_ACCESS_TOKEN --prefer-ssh -o ~/github-backup/ -l error -P -i --all-starred --starred --watched --followers --following --issues --issue-comments --issue-events --pulls --pull-comments --pull-commits --labels --milestones --repositories --wikis --releases --assets --pull-details --gists --starred-gists $GH_USER
    
Debug an error/block or incomplete backup into a temporary directory. Omit "incremental" to fill a previous incomplete backup. ::

    export FINE_ACCESS_TOKEN=SOME-GITHUB-TOKEN
    GH_USER=YOUR-GITHUB-USER

    github-backup -f $FINE_ACCESS_TOKEN -o /tmp/github-backup/ -l debug -P --all-starred --starred --watched --followers --following --issues --issue-comments --issue-events --pulls --pull-comments --pull-commits --labels --milestones --repositories --wikis --releases --assets --pull-details --gists --starred-gists $GH_USER



Development
===========

This project is considered feature complete for the primary maintainer @josegonzalez. If you would like a bugfix or enhancement, pull requests are welcome. Feel free to contact the maintainer for consulting estimates if you'd like to sponsor the work instead.

Contibuters
-----------

A huge thanks to all the contibuters!

.. image:: https://contrib.rocks/image?repo=josegonzalez/python-github-backup
   :target: https://github.com/josegonzalez/python-github-backup/graphs/contributors
   :alt: contributors

Testing
-------

This project currently contains no unit tests.  To run linting::

    pip install flake8
    flake8 --ignore=E501


.. |PyPI| image:: https://img.shields.io/pypi/v/github-backup.svg
   :target: https://pypi.python.org/pypi/github-backup/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/github-backup.svg
   :target: https://github.com/josegonzalez/python-github-backup

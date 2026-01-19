=============
github-backup
=============

|PyPI| |Python Versions|

The package can be used to backup an *entire* `Github <https://github.com/>`_ organization, repository or user account, including starred repos, issues and wikis in the most appropriate format (clones for wikis, json files for issues).

Requirements
============

- Python 3.10 or higher
- GIT 1.9+

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

    github-backup [-h] [-t TOKEN_CLASSIC] [-f TOKEN_FINE] [-q] [--as-app]
                  [-o OUTPUT_DIRECTORY] [-l LOG_LEVEL] [-i]
                  [--incremental-by-files]
                  [--starred] [--all-starred] [--starred-skip-size-over MB]
                  [--watched] [--followers] [--following] [--all]
                  [--issues] [--issue-comments] [--issue-events] [--pulls]
                  [--pull-comments] [--pull-commits] [--pull-details]
                  [--labels] [--hooks] [--milestones] [--security-advisories]
                  [--repositories] [--bare] [--no-prune] [--lfs] [--wikis]
                  [--gists] [--starred-gists] [--skip-archived] [--skip-existing]
                  [-L [LANGUAGES ...]] [-N NAME_REGEX] [-H GITHUB_HOST]
                  [-O] [-R REPOSITORY] [-P] [-F] [--prefer-ssh] [-v]
                  [--keychain-name OSX_KEYCHAIN_ITEM_NAME]
                  [--keychain-account OSX_KEYCHAIN_ITEM_ACCOUNT]
                  [--releases] [--latest-releases NUMBER_OF_LATEST_RELEASES]
                  [--skip-prerelease] [--assets]
                  [--skip-assets-on [SKIP_ASSETS_ON ...]] [--attachments]
                  [--throttle-limit THROTTLE_LIMIT]
                  [--throttle-pause THROTTLE_PAUSE]
                  [--exclude [EXCLUDE ...]] [--retries MAX_RETRIES]
                  USER

    Backup a github account

    positional arguments:
      USER                  github username

    options:
      -h, --help            show this help message and exit
      -t, --token TOKEN_CLASSIC
                            personal access, OAuth, or JSON Web token, or path to
                            token (file://...)
      -f, --token-fine TOKEN_FINE
                            fine-grained personal access token (github_pat_....),
                            or path to token (file://...)
      -q, --quiet           supress log messages less severe than warning, e.g.
                            info
      --as-app              authenticate as github app instead of as a user.
      -o, --output-directory OUTPUT_DIRECTORY
                            directory at which to backup the repositories
      -l, --log-level LOG_LEVEL
                            log level to use (default: info, possible levels:
                            debug, info, warning, error, critical)
      -i, --incremental     incremental backup
      --incremental-by-files
                            incremental backup based on modification date of files
      --starred             include JSON output of starred repositories in backup
      --all-starred         include starred repositories in backup [*]
      --starred-skip-size-over MB
                            skip starred repositories larger than this size in MB
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
      --security-advisories
                            include security advisories in backup
      --repositories        include repository clone in backup
      --bare                clone bare repositories
      --no-prune            disable prune option for git fetch
      --lfs                 clone LFS repositories (requires Git LFS to be
                            installed, https://git-lfs.github.com) [*]
      --wikis               include wiki clone in backup
      --gists               include gists in backup [*]
      --starred-gists       include starred gists in backup [*]
      --skip-archived       skip project if it is archived
      --skip-existing       skip project if a backup directory exists
      -L, --languages [LANGUAGES ...]
                            only allow these languages
      -N, --name-regex NAME_REGEX
                            python regex to match names against
      -H, --github-host GITHUB_HOST
                            GitHub Enterprise hostname
      -O, --organization    whether or not this is an organization user
      -R, --repository REPOSITORY
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
                            include certain number of the latest releases; only
                            applies if including releases
      --skip-prerelease     skip prerelease and draft versions; only applies if
                            including releases
      --assets              include assets alongside release information; only
                            applies if including releases
      --skip-assets-on [SKIP_ASSETS_ON ...]
                            skip asset downloads for these repositories
      --attachments         download user-attachments from issues and pull
                            requests
      --throttle-limit THROTTLE_LIMIT
                            start throttling of GitHub API requests after this
                            amount of API requests remain
      --throttle-pause THROTTLE_PAUSE
                            wait this amount of seconds when API request
                            throttling is active (default: 30.0, requires
                            --throttle-limit to be set)
      --exclude [EXCLUDE ...]
                            names of repositories to exclude
      --retries MAX_RETRIES
                            maximum number of retries for API calls (default: 5)

Usage Details
=============

Authentication
--------------

GitHub requires token-based authentication for API access. Password authentication was `removed in November 2020 <https://developer.github.com/changes/2020-02-14-deprecating-password-auth/>`_.

The positional argument ``USER`` specifies the user or organization account you wish to back up.

**Fine-grained tokens** (``-f TOKEN_FINE``) are recommended for most use cases, especially long-running backups (e.g. cron jobs), as they provide precise permission control.

**Classic tokens** (``-t TOKEN``) are `slightly less secure <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#personal-access-tokens-classic>`_ as they provide very coarse-grained permissions.


Fine Tokens
~~~~~~~~~~~

You can "generate new token", choosing the repository scope by selecting specific repos or all repos. On Github this is under *Settings -> Developer Settings -> Personal access tokens -> Fine-grained Tokens*

Customise the permissions for your use case, but for a personal account full backup you'll need to enable the following permissions:

**User permissions**: Read access to followers, starring, and watching.

**Repository permissions**: Read access to contents, issues, metadata, pull requests, and webhooks.


GitHub Apps
~~~~~~~~~~~

GitHub Apps are ideal for organization backups in CI/CD. Tokens are scoped to specific repositories and expire after 1 hour.

**One-time setup:**

1. Create a GitHub App at *Settings -> Developer Settings -> GitHub Apps -> New GitHub App*
2. Set a name and homepage URL (can be any URL)
3. Uncheck "Webhook > Active" (not needed for backups)
4. Set permissions (same as fine-grained tokens above)
5. Click "Create GitHub App", then note the **App ID** shown on the next page
6. Under "Private keys", click "Generate a private key" and save the downloaded file
7. Go to *Install App* in your app's settings
8. Select the account/organization and which repositories to back up

**CI/CD usage with GitHub Actions:**

Store the App ID as a repository variable and the private key contents as a secret, then use ``actions/create-github-app-token``::

    - uses: actions/create-github-app-token@v1
      id: app-token
      with:
        app-id: ${{ vars.APP_ID }}
        private-key: ${{ secrets.APP_PRIVATE_KEY }}

    - run: github-backup myorg -t ${{ steps.app-token.outputs.token }} --as-app -o ./backup --all

Note: Installation tokens expire after 1 hour. For long-running backups, use a fine-grained personal access token instead.


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

LFS objects are fetched for all refs, not just the current checkout, ensuring a complete backup of all LFS content across all branches and history.


About Attachments
-----------------

When you use the ``--attachments`` option with ``--issues`` or ``--pulls``, the tool will download user-uploaded attachments (images, videos, documents, etc.) from issue and pull request descriptions and comments. In some circumstances attachments contain valuable data related to the topic, and without their backup important information or context might be lost inadvertently.

Attachments are saved to ``issues/attachments/{issue_number}/`` and ``pulls/attachments/{pull_number}/`` directories, where ``{issue_number}`` is the GitHub issue number (e.g., issue #123 saves to ``issues/attachments/123/``). Each attachment directory contains:

- The downloaded attachment files (named by their GitHub identifier with appropriate file extensions)
- If multiple attachments have the same filename, conflicts are resolved with numeric suffixes (e.g., ``report.pdf``, ``report_1.pdf``, ``report_2.pdf``)
- A ``manifest.json`` file documenting all downloads, including URLs, file metadata, and download status

The tool automatically extracts file extensions from HTTP headers to ensure files can be more easily opened by your operating system.

**Supported URL formats:**

- Modern: ``github.com/user-attachments/{assets,files}/*``
- Legacy: ``user-images.githubusercontent.com/*`` and ``private-user-images.githubusercontent.com/*``
- Repo files: ``github.com/{owner}/{repo}/files/*`` (filtered to current repository)
- Repo assets: ``github.com/{owner}/{repo}/assets/*`` (filtered to current repository)

**Repository filtering** for repo files/assets handles renamed and transferred repositories gracefully. URLs are included if they either match the current repository name directly, or redirect to it (e.g., ``willmcgugan/rich`` redirects to ``Textualize/rich`` after transfer).

**Fine-grained token limitation:** Due to a GitHub platform limitation, fine-grained personal access tokens (``github_pat_...``) cannot download attachments from private repositories directly. This affects both ``/assets/`` (images) and ``/files/`` (documents) URLs. The tool implements a workaround for image attachments using GitHub's Markdown API, which converts URLs to temporary JWT-signed URLs that can be downloaded. However, this workaround only works for images - document attachments (PDFs, text files, etc.) will fail with 404 errors when using fine-grained tokens on private repos. For full attachment support on private repositories, use a classic token (``-t``) instead of a fine-grained token (``-f``). See `#477 <https://github.com/josegonzalez/python-github-backup/issues/477>`_ for details.


About security advisories
-------------------------

GitHub security advisories are only available in public repositories. GitHub does not provide the respective API endpoint for private repositories.

Therefore the logic is implemented as follows:
- Security advisories are included in the `--all` option.
- If only the `--all` option was provided, backups of security advisories are skipped for private repositories.
- If the `--security-advisories` option is provided (on its own or in addition to `--all`), a backup of security advisories is attempted for all repositories, with graceful handling if the GitHub API doesn't return any.


Run in Docker container
-----------------------

To run the tool in a Docker container use the following command:

    sudo docker run --rm -v /path/to/backup:/data --name github-backup ghcr.io/josegonzalez/python-github-backup -o /data $OPTIONS $USER

Gotchas / Known-issues
======================

All is not everything
---------------------

The ``--all`` argument does not include: cloning private repos (``-P, --private``), cloning forks (``-F, --fork``), cloning starred repositories (``--all-starred``), ``--pull-details``, cloning LFS repositories (``--lfs``), cloning gists (``--gists``) or cloning starred gist repos (``--starred-gists``). See examples for more.

Starred repository size
-----------------------

Using the ``--all-starred`` argument to clone all starred repositories may use a large amount of storage space.

To see your starred repositories sorted by size (requires `GitHub CLI <https://cli.github.com>`_)::

    gh api user/starred --paginate --jq 'sort_by(-.size)[]|"\(.full_name) \(.size/1024|round)MB"'

To limit which starred repositories are cloned, use ``--starred-skip-size-over SIZE`` where SIZE is in MB. For example, ``--starred-skip-size-over 500`` will skip any starred repository where the git repository size (code and history) exceeds 500 MB. Note that this size limit only applies to the repository itself, not issues, release assets or other metadata. This filter only affects starred repositories; your own repositories are always included regardless of size.

For finer control, avoid using ``--assets`` with starred repos, or use ``--skip-assets-on`` for specific repositories with large release binaries.

Alternatively, consider just storing links to starred repos in JSON format with ``--starred``.

Incremental Backup
------------------

Using (``-i, --incremental``) will only request new data from the API **since the last run (successful or not)**. e.g. only request issues from the API since the last run. 

This means any blocking errors on previous runs can cause a large amount of missing data in backups.

Using (``--incremental-by-files``) will request new data from the API **based on when the file was modified on filesystem**. e.g. if you modify the file yourself you may miss something.

Still saver than the previous version.

Specifically, issues and pull requests are handled like this.

Known blocking errors
---------------------

Some errors will block the backup run by exiting the script. e.g. receiving a 403 Forbidden error from the Github API.

If the incremental argument is used, this will result in the next backup only requesting API data since the last blocked/failed run. Potentially causing unexpected large amounts of missing data.

It's therefore recommended to only use the incremental argument if the output/result is being actively monitored, or complimented with periodic full non-incremental runs, to avoid unexpected missing data in a regular backup runs.

**Starred public repo hooks blocking**

Since the ``--all`` argument includes ``--hooks``, if you use ``--all`` and ``--all-starred`` together to clone a users starred public repositories, the backup will likely error and block the backup continuing.

This is due to needing the correct permission for ``--hooks`` on public repos.


"bare" is actually "mirror"
---------------------------

Using the bare clone argument (``--bare``) will actually call git's ``clone --mirror`` command. There's a subtle difference between `bare <https://www.git-scm.com/docs/git-clone#Documentation/git-clone.txt---bare>`_ and `mirror <https://www.git-scm.com/docs/git-clone#Documentation/git-clone.txt---mirror>`_ clone.

*From git docs "Compared to --bare, --mirror not only maps local branches of the source to local branches of the target, it maps all refs (including remote-tracking branches, notes etc.) and sets up a refspec configuration such that all these refs are overwritten by a git remote update in the target repository."*


Starred gists vs starred repo behaviour
---------------------------------------

The starred normal repo cloning (``--all-starred``) argument stores starred repos separately to the users own repositories. However, using ``--starred-gists`` will store starred gists within the same directory as the users own gists ``--gists``. Also, all gist repo directory names are IDs not the gist's name.

Note: ``--starred-gists`` only retrieves starred gists for the authenticated user, not the target user, due to a GitHub API limitation.


Skip existing on incomplete backups
-----------------------------------

The ``--skip-existing`` argument will skip a backup if the directory already exists, even if the backup in that directory failed (perhaps due to a blocking error). This may result in unexpected missing data in a regular backup.


Updates use fetch, not pull
---------------------------

When updating an existing repository backup, ``github-backup`` uses ``git fetch`` rather than ``git pull``. This is intentional - a backup tool should reliably download data without risk of failure. Using ``git pull`` would require handling merge conflicts, which adds complexity and could cause backups to fail unexpectedly.

With fetch, **all branches and commits are downloaded** safely into remote-tracking branches. The working directory files won't change, but your backup is complete.

If you look at files directly (e.g., ``cat README.md``), you'll see the old content. The new data is in the remote-tracking branches (confusingly named "remote" but stored locally). To view or use the latest files::

    git show origin/main:README.md           # view a file
    git merge origin/main                    # update working directory

All branches are backed up as remote refs (``origin/main``, ``origin/feature-branch``, etc.).

If you want to browse files directly without merging, consider using ``--bare`` which skips the working directory entirely - the backup is just the git data.

See `#269 <https://github.com/josegonzalez/python-github-backup/issues/269>`_ for more discussion.


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

    github-backup -f $FINE_ACCESS_TOKEN --prefer-ssh -o ~/github-backup/ -l error -P -i --all-starred --starred --watched --followers --following --issues --issue-comments --issue-events --pulls --pull-comments --pull-commits --labels --milestones --security-advisories --repositories --wikis --releases --assets --attachments --pull-details --gists --starred-gists $GH_USER
    
Debug an error/block or incomplete backup into a temporary directory. Omit "incremental" to fill a previous incomplete backup. ::

    export FINE_ACCESS_TOKEN=SOME-GITHUB-TOKEN
    GH_USER=YOUR-GITHUB-USER

    github-backup -f $FINE_ACCESS_TOKEN -o /tmp/github-backup/ -l debug -P --all-starred --starred --watched --followers --following --issues --issue-comments --issue-events --pulls --pull-comments --pull-commits --labels --milestones --repositories --wikis --releases --assets --pull-details --gists --starred-gists $GH_USER

Pipe a token from stdin to avoid storing it in environment variables or command history (Unix-like systems only)::

    my-secret-manager get github-token | github-backup user -t file:///dev/stdin -o /backup --repositories

Restoring from Backup
=====================

This tool creates backups only, there is no inbuilt restore command.

**Git repositories, wikis, and gists** can be restored by pushing them back to GitHub as you would any git repository. For example, to restore a bare repository backup::

    cd /tmp/white-house/repositories/petitions/repository
    git push --mirror git@github.com:WhiteHouse/petitions.git

**Issues, pull requests, comments, and other metadata** are saved as JSON files for archival purposes. The GitHub API does not support recreating this data faithfully, creating issues via the API has limitations:

- New issue/PR numbers are assigned (original numbers cannot be set)
- Timestamps reflect creation time (original dates cannot be set)
- The API caller becomes the author (original authors cannot be set)
- Cross-references between issues and PRs will break

These are GitHub API limitations that affect all backup and migration tools, not just this one. Recreating issues with these limitations via the GitHub API is an exercise for the reader. The JSON backups remain useful for searching, auditing, or manual reference.


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

To run the test suite::

    pip install pytest
    pytest

To run linting::

    pip install flake8
    flake8 --ignore=E501


.. |PyPI| image:: https://img.shields.io/pypi/v/github-backup.svg
   :target: https://pypi.python.org/pypi/github-backup/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/github-backup.svg
   :target: https://github.com/josegonzalez/python-github-backup

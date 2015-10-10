Changelog
=========

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



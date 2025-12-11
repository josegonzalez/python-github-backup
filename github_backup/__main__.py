"""Allow running as: python -m github_backup"""

import sys

from github_backup.cli import main
from github_backup.github_backup import logger

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

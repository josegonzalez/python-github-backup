"""Shared pytest fixtures for github-backup tests."""

import pytest

from github_backup.github_backup import parse_args


@pytest.fixture
def create_args():
    """Factory fixture that creates args with real CLI defaults.

    Uses the actual argument parser so new CLI args are automatically
    available with their defaults - no test updates needed.

    Usage:
        def test_something(self, create_args):
            args = create_args(include_releases=True, user="myuser")
    """
    def _create(**overrides):
        # Use real parser to get actual defaults
        args = parse_args(["testuser"])
        for key, value in overrides.items():
            setattr(args, key, value)
        return args
    return _create

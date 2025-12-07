"""Tests for case-insensitive username/organization filtering."""

import pytest
from unittest.mock import Mock

from github_backup import github_backup


class TestCaseSensitivity:
    """Test suite for case-insensitive username matching in filter_repositories."""

    def test_filter_repositories_case_insensitive_user(self):
        """Should filter repositories case-insensitively for usernames.

        Reproduces issue #198 where typing 'iamrodos' fails to match
        repositories with owner.login='Iamrodos' (the canonical case from GitHub API).
        """
        # Simulate user typing lowercase username
        args = Mock()
        args.user = "iamrodos"  # lowercase (what user typed)
        args.repository = None
        args.name_regex = None
        args.languages = None
        args.exclude = None
        args.fork = False
        args.private = False
        args.public = False
        args.all = True

        # Simulate GitHub API returning canonical case
        repos = [
            {
                "name": "repo1",
                "owner": {"login": "Iamrodos"},  # Capital I (canonical from API)
                "private": False,
                "fork": False,
            },
            {
                "name": "repo2",
                "owner": {"login": "Iamrodos"},
                "private": False,
                "fork": False,
            },
        ]

        filtered = github_backup.filter_repositories(args, repos)

        # Should match despite case difference
        assert len(filtered) == 2
        assert filtered[0]["name"] == "repo1"
        assert filtered[1]["name"] == "repo2"

    def test_filter_repositories_case_insensitive_org(self):
        """Should filter repositories case-insensitively for organizations.

        Tests the example from issue #198 where 'prai-org' doesn't match 'PRAI-Org'.
        """
        args = Mock()
        args.user = "prai-org"  # lowercase (what user typed)
        args.repository = None
        args.name_regex = None
        args.languages = None
        args.exclude = None
        args.fork = False
        args.private = False
        args.public = False
        args.all = True

        repos = [
            {
                "name": "repo1",
                "owner": {"login": "PRAI-Org"},  # Different case (canonical from API)
                "private": False,
                "fork": False,
            },
        ]

        filtered = github_backup.filter_repositories(args, repos)

        # Should match despite case difference
        assert len(filtered) == 1
        assert filtered[0]["name"] == "repo1"

    def test_filter_repositories_case_variations(self):
        """Should handle various case combinations correctly."""
        args = Mock()
        args.user = "TeSt-UsEr"  # Mixed case
        args.repository = None
        args.name_regex = None
        args.languages = None
        args.exclude = None
        args.fork = False
        args.private = False
        args.public = False
        args.all = True

        repos = [
            {"name": "repo1", "owner": {"login": "test-user"}, "private": False, "fork": False},
            {"name": "repo2", "owner": {"login": "TEST-USER"}, "private": False, "fork": False},
            {"name": "repo3", "owner": {"login": "TeSt-UsEr"}, "private": False, "fork": False},
            {"name": "repo4", "owner": {"login": "other-user"}, "private": False, "fork": False},
        ]

        filtered = github_backup.filter_repositories(args, repos)

        # Should match first 3 (all case variations of same user)
        assert len(filtered) == 3
        assert set(r["name"] for r in filtered) == {"repo1", "repo2", "repo3"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

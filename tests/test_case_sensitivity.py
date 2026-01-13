"""Tests for case-insensitive username/organization filtering."""

import pytest

from github_backup import github_backup


class TestCaseSensitivity:
    """Test suite for case-insensitive username matching in filter_repositories."""

    def test_filter_repositories_case_insensitive_user(self, create_args):
        """Should filter repositories case-insensitively for usernames.

        Reproduces issue #198 where typing 'iamrodos' fails to match
        repositories with owner.login='Iamrodos' (the canonical case from GitHub API).
        """
        # Simulate user typing lowercase username
        args = create_args(user="iamrodos")

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

    def test_filter_repositories_case_insensitive_org(self, create_args):
        """Should filter repositories case-insensitively for organizations.

        Tests the example from issue #198 where 'prai-org' doesn't match 'PRAI-Org'.
        """
        args = create_args(user="prai-org")

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

    def test_filter_repositories_case_variations(self, create_args):
        """Should handle various case combinations correctly."""
        args = create_args(user="TeSt-UsEr")

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

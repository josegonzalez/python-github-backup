"""Tests for --starred-skip-size-over flag behavior (issue #108)."""

import pytest
from unittest.mock import Mock

from github_backup import github_backup


class TestStarredSkipSizeOver:
    """Test suite for --starred-skip-size-over flag.

    Issue #108: Allow restricting size of starred repositories before cloning.
    The size is based on the GitHub API's 'size' field (in KB), but the CLI
    argument accepts MB for user convenience.
    """

    def _create_mock_args(self, **overrides):
        """Create a mock args object with sensible defaults."""
        args = Mock()
        args.user = "testuser"
        args.repository = None
        args.name_regex = None
        args.languages = None
        args.fork = False
        args.private = False
        args.skip_archived = False
        args.starred_skip_size_over = None
        args.exclude = None

        for key, value in overrides.items():
            setattr(args, key, value)

        return args


class TestStarredSkipSizeOverArgumentParsing(TestStarredSkipSizeOver):
    """Tests for --starred-skip-size-over argument parsing."""

    def test_starred_skip_size_over_not_set_defaults_to_none(self):
        """When --starred-skip-size-over is not specified, it should default to None."""
        args = github_backup.parse_args(["testuser"])
        assert args.starred_skip_size_over is None

    def test_starred_skip_size_over_accepts_integer(self):
        """--starred-skip-size-over should accept an integer value."""
        args = github_backup.parse_args(["testuser", "--starred-skip-size-over", "500"])
        assert args.starred_skip_size_over == 500

    def test_starred_skip_size_over_rejects_non_integer(self):
        """--starred-skip-size-over should reject non-integer values."""
        with pytest.raises(SystemExit):
            github_backup.parse_args(["testuser", "--starred-skip-size-over", "abc"])


class TestStarredSkipSizeOverFiltering(TestStarredSkipSizeOver):
    """Tests for --starred-skip-size-over filtering behavior."""

    def test_starred_repo_under_limit_is_kept(self):
        """Starred repos under the size limit should be kept."""
        args = self._create_mock_args(starred_skip_size_over=500)

        repos = [
            {
                "name": "small-repo",
                "owner": {"login": "otheruser"},
                "size": 100 * 1024,  # 100 MB in KB
                "is_starred": True,
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 1
        assert result[0]["name"] == "small-repo"

    def test_starred_repo_over_limit_is_filtered(self):
        """Starred repos over the size limit should be filtered out."""
        args = self._create_mock_args(starred_skip_size_over=500)

        repos = [
            {
                "name": "huge-repo",
                "owner": {"login": "otheruser"},
                "size": 600 * 1024,  # 600 MB in KB
                "is_starred": True,
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 0

    def test_own_repo_over_limit_is_kept(self):
        """User's own repos should not be affected by the size limit."""
        args = self._create_mock_args(starred_skip_size_over=500)

        repos = [
            {
                "name": "my-huge-repo",
                "owner": {"login": "testuser"},
                "size": 600 * 1024,  # 600 MB in KB
                # No is_starred flag - this is the user's own repo
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 1
        assert result[0]["name"] == "my-huge-repo"

    def test_starred_repo_at_exact_limit_is_kept(self):
        """Starred repos at exactly the size limit should be kept."""
        args = self._create_mock_args(starred_skip_size_over=500)

        repos = [
            {
                "name": "exact-limit-repo",
                "owner": {"login": "otheruser"},
                "size": 500 * 1024,  # Exactly 500 MB in KB
                "is_starred": True,
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 1
        assert result[0]["name"] == "exact-limit-repo"

    def test_mixed_repos_filtered_correctly(self):
        """Mix of own and starred repos should be filtered correctly."""
        args = self._create_mock_args(starred_skip_size_over=500)

        repos = [
            {
                "name": "my-huge-repo",
                "owner": {"login": "testuser"},
                "size": 1000 * 1024,  # 1 GB - own repo, should be kept
            },
            {
                "name": "starred-small",
                "owner": {"login": "otheruser"},
                "size": 100 * 1024,  # 100 MB - under limit
                "is_starred": True,
            },
            {
                "name": "starred-huge",
                "owner": {"login": "anotheruser"},
                "size": 2000 * 1024,  # 2 GB - over limit
                "is_starred": True,
            },
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 2
        names = [r["name"] for r in result]
        assert "my-huge-repo" in names
        assert "starred-small" in names
        assert "starred-huge" not in names

    def test_no_size_limit_keeps_all_starred(self):
        """When no size limit is set, all starred repos should be kept."""
        args = self._create_mock_args(starred_skip_size_over=None)

        repos = [
            {
                "name": "huge-starred-repo",
                "owner": {"login": "otheruser"},
                "size": 10000 * 1024,  # 10 GB
                "is_starred": True,
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 1

    def test_repo_without_size_field_is_kept(self):
        """Repos without a size field should be kept (size defaults to 0)."""
        args = self._create_mock_args(starred_skip_size_over=500)

        repos = [
            {
                "name": "no-size-repo",
                "owner": {"login": "otheruser"},
                "is_starred": True,
                # No size field
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 1

    def test_zero_value_warns_and_is_ignored(self, caplog):
        """Zero value should warn and keep all repos."""
        args = self._create_mock_args(starred_skip_size_over=0)

        repos = [
            {
                "name": "huge-starred-repo",
                "owner": {"login": "otheruser"},
                "size": 10000 * 1024,  # 10 GB
                "is_starred": True,
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 1
        assert "must be greater than 0" in caplog.text

    def test_negative_value_warns_and_is_ignored(self, caplog):
        """Negative value should warn and keep all repos."""
        args = self._create_mock_args(starred_skip_size_over=-5)

        repos = [
            {
                "name": "huge-starred-repo",
                "owner": {"login": "otheruser"},
                "size": 10000 * 1024,  # 10 GB
                "is_starred": True,
            }
        ]

        result = github_backup.filter_repositories(args, repos)
        assert len(result) == 1
        assert "must be greater than 0" in caplog.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

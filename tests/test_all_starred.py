"""Tests for --all-starred flag behavior (issue #225)."""

import pytest
from unittest.mock import Mock, patch

from github_backup import github_backup


class TestAllStarredCloning:
    """Test suite for --all-starred repository cloning behavior.

    Issue #225: --all-starred should clone starred repos without requiring --repositories.
    """

    def _create_mock_args(self, **overrides):
        """Create a mock args object with sensible defaults."""
        args = Mock()
        args.user = "testuser"
        args.output_directory = "/tmp/backup"
        args.include_repository = False
        args.include_everything = False
        args.include_gists = False
        args.include_starred_gists = False
        args.all_starred = False
        args.skip_existing = False
        args.bare_clone = False
        args.lfs_clone = False
        args.no_prune = False
        args.include_wiki = False
        args.include_issues = False
        args.include_issue_comments = False
        args.include_issue_events = False
        args.include_pulls = False
        args.include_pull_comments = False
        args.include_pull_commits = False
        args.include_pull_details = False
        args.include_labels = False
        args.include_hooks = False
        args.include_milestones = False
        args.include_releases = False
        args.include_assets = False
        args.include_attachments = False
        args.incremental = False
        args.incremental_by_files = False
        args.github_host = None
        args.prefer_ssh = False
        args.token_classic = None
        args.token_fine = None
        args.as_app = False
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None

        for key, value in overrides.items():
            setattr(args, key, value)

        return args

    @patch('github_backup.github_backup.fetch_repository')
    @patch('github_backup.github_backup.get_github_repo_url')
    def test_all_starred_clones_without_repositories_flag(self, mock_get_url, mock_fetch):
        """--all-starred should clone starred repos without --repositories flag.

        This is the core fix for issue #225.
        """
        args = self._create_mock_args(all_starred=True)
        mock_get_url.return_value = "https://github.com/otheruser/awesome-project.git"

        # A starred repository (is_starred flag set by retrieve_repositories)
        starred_repo = {
            "name": "awesome-project",
            "full_name": "otheruser/awesome-project",
            "owner": {"login": "otheruser"},
            "private": False,
            "fork": False,
            "has_wiki": False,
            "is_starred": True,  # This flag is set for starred repos
        }

        with patch('github_backup.github_backup.mkdir_p'):
            github_backup.backup_repositories(args, "/tmp/backup", [starred_repo])

        # fetch_repository should be called for the starred repo
        assert mock_fetch.called, "--all-starred should trigger repository cloning"
        mock_fetch.assert_called_once()
        call_args = mock_fetch.call_args
        assert call_args[0][0] == "awesome-project"  # repo name

    @patch('github_backup.github_backup.fetch_repository')
    @patch('github_backup.github_backup.get_github_repo_url')
    def test_starred_repo_not_cloned_without_all_starred_flag(self, mock_get_url, mock_fetch):
        """Starred repos should NOT be cloned if --all-starred is not set."""
        args = self._create_mock_args(all_starred=False)
        mock_get_url.return_value = "https://github.com/otheruser/awesome-project.git"

        starred_repo = {
            "name": "awesome-project",
            "full_name": "otheruser/awesome-project",
            "owner": {"login": "otheruser"},
            "private": False,
            "fork": False,
            "has_wiki": False,
            "is_starred": True,
        }

        with patch('github_backup.github_backup.mkdir_p'):
            github_backup.backup_repositories(args, "/tmp/backup", [starred_repo])

        # fetch_repository should NOT be called
        assert not mock_fetch.called, "Starred repos should not be cloned without --all-starred"

    @patch('github_backup.github_backup.fetch_repository')
    @patch('github_backup.github_backup.get_github_repo_url')
    def test_non_starred_repo_not_cloned_with_only_all_starred(self, mock_get_url, mock_fetch):
        """Non-starred repos should NOT be cloned when only --all-starred is set."""
        args = self._create_mock_args(all_starred=True)
        mock_get_url.return_value = "https://github.com/testuser/my-project.git"

        # A regular (non-starred) repository
        regular_repo = {
            "name": "my-project",
            "full_name": "testuser/my-project",
            "owner": {"login": "testuser"},
            "private": False,
            "fork": False,
            "has_wiki": False,
            # No is_starred flag
        }

        with patch('github_backup.github_backup.mkdir_p'):
            github_backup.backup_repositories(args, "/tmp/backup", [regular_repo])

        # fetch_repository should NOT be called for non-starred repos
        assert not mock_fetch.called, "Non-starred repos should not be cloned with only --all-starred"

    @patch('github_backup.github_backup.fetch_repository')
    @patch('github_backup.github_backup.get_github_repo_url')
    def test_repositories_flag_still_works(self, mock_get_url, mock_fetch):
        """--repositories flag should still clone repos as before."""
        args = self._create_mock_args(include_repository=True)
        mock_get_url.return_value = "https://github.com/testuser/my-project.git"

        regular_repo = {
            "name": "my-project",
            "full_name": "testuser/my-project",
            "owner": {"login": "testuser"},
            "private": False,
            "fork": False,
            "has_wiki": False,
        }

        with patch('github_backup.github_backup.mkdir_p'):
            github_backup.backup_repositories(args, "/tmp/backup", [regular_repo])

        # fetch_repository should be called
        assert mock_fetch.called, "--repositories should trigger repository cloning"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

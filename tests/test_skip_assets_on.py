"""Tests for --skip-assets-on flag behavior (issue #135)."""

import pytest
from unittest.mock import patch

from github_backup import github_backup


class TestSkipAssetsOn:
    """Test suite for --skip-assets-on flag.

    Issue #135: Allow skipping asset downloads for specific repositories
    while still backing up release metadata.
    """

    def _create_mock_repository(self, name="test-repo", owner="testuser"):
        """Create a mock repository object."""
        return {
            "name": name,
            "full_name": f"{owner}/{name}",
            "owner": {"login": owner},
            "private": False,
            "fork": False,
            "has_wiki": False,
        }

    def _create_mock_release(self, tag="v1.0.0"):
        """Create a mock release object."""
        return {
            "tag_name": tag,
            "name": tag,
            "prerelease": False,
            "draft": False,
            "assets_url": f"https://api.github.com/repos/testuser/test-repo/releases/{tag}/assets",
        }

    def _create_mock_asset(self, name="asset.zip"):
        """Create a mock asset object."""
        return {
            "name": name,
            "url": f"https://api.github.com/repos/testuser/test-repo/releases/assets/{name}",
        }


class TestSkipAssetsOnArgumentParsing(TestSkipAssetsOn):
    """Tests for --skip-assets-on argument parsing."""

    def test_skip_assets_on_not_set_defaults_to_none(self):
        """When --skip-assets-on is not specified, it should default to None."""
        args = github_backup.parse_args(["testuser"])
        assert args.skip_assets_on is None

    def test_skip_assets_on_single_repo(self):
        """Single --skip-assets-on should create list with one item."""
        args = github_backup.parse_args(["testuser", "--skip-assets-on", "big-repo"])
        assert args.skip_assets_on == ["big-repo"]

    def test_skip_assets_on_multiple_repos(self):
        """Multiple repos can be specified space-separated (like --exclude)."""
        args = github_backup.parse_args(
            [
                "testuser",
                "--skip-assets-on",
                "big-repo",
                "another-repo",
                "owner/third-repo",
            ]
        )
        assert args.skip_assets_on == ["big-repo", "another-repo", "owner/third-repo"]


class TestSkipAssetsOnBehavior(TestSkipAssetsOn):
    """Tests for --skip-assets-on behavior in backup_releases."""

    @patch("github_backup.github_backup.download_file")
    @patch("github_backup.github_backup.retrieve_data")
    @patch("github_backup.github_backup.mkdir_p")
    @patch("github_backup.github_backup.json_dump_if_changed")
    def test_assets_downloaded_when_not_skipped(
        self, mock_json_dump, mock_mkdir, mock_retrieve, mock_download, create_args
    ):
        """Assets should be downloaded when repo is not in skip list."""
        args = create_args(skip_assets_on=[])
        repository = self._create_mock_repository(name="normal-repo")
        release = self._create_mock_release()
        asset = self._create_mock_asset()

        mock_json_dump.return_value = True
        mock_retrieve.side_effect = [
            [release],  # First call: get releases
            [asset],  # Second call: get assets
        ]

        with patch("os.path.join", side_effect=lambda *args: "/".join(args)):
            github_backup.backup_releases(
                args,
                "/tmp/backup/repositories/normal-repo",
                repository,
                "https://api.github.com/repos/{owner}/{repo}",
                include_assets=True,
            )

        # download_file should have been called for the asset
        mock_download.assert_called_once()

    @patch("github_backup.github_backup.download_file")
    @patch("github_backup.github_backup.retrieve_data")
    @patch("github_backup.github_backup.mkdir_p")
    @patch("github_backup.github_backup.json_dump_if_changed")
    def test_assets_skipped_when_repo_name_matches(
        self, mock_json_dump, mock_mkdir, mock_retrieve, mock_download, create_args
    ):
        """Assets should be skipped when repo name is in skip list."""
        args = create_args(skip_assets_on=["big-repo"])
        repository = self._create_mock_repository(name="big-repo")
        release = self._create_mock_release()

        mock_json_dump.return_value = True
        mock_retrieve.return_value = [release]

        github_backup.backup_releases(
            args,
            "/tmp/backup/repositories/big-repo",
            repository,
            "https://api.github.com/repos/{owner}/{repo}",
            include_assets=True,
        )

        # download_file should NOT have been called
        mock_download.assert_not_called()

    @patch("github_backup.github_backup.download_file")
    @patch("github_backup.github_backup.retrieve_data")
    @patch("github_backup.github_backup.mkdir_p")
    @patch("github_backup.github_backup.json_dump_if_changed")
    def test_assets_skipped_when_full_name_matches(
        self, mock_json_dump, mock_mkdir, mock_retrieve, mock_download, create_args
    ):
        """Assets should be skipped when owner/repo format matches."""
        args = create_args(skip_assets_on=["otheruser/big-repo"])
        repository = self._create_mock_repository(name="big-repo", owner="otheruser")
        release = self._create_mock_release()

        mock_json_dump.return_value = True
        mock_retrieve.return_value = [release]

        github_backup.backup_releases(
            args,
            "/tmp/backup/repositories/big-repo",
            repository,
            "https://api.github.com/repos/{owner}/{repo}",
            include_assets=True,
        )

        # download_file should NOT have been called
        mock_download.assert_not_called()

    @patch("github_backup.github_backup.download_file")
    @patch("github_backup.github_backup.retrieve_data")
    @patch("github_backup.github_backup.mkdir_p")
    @patch("github_backup.github_backup.json_dump_if_changed")
    def test_case_insensitive_matching(
        self, mock_json_dump, mock_mkdir, mock_retrieve, mock_download, create_args
    ):
        """Skip matching should be case-insensitive."""
        # User types uppercase, repo name is lowercase
        args = create_args(skip_assets_on=["BIG-REPO"])
        repository = self._create_mock_repository(name="big-repo")
        release = self._create_mock_release()

        mock_json_dump.return_value = True
        mock_retrieve.return_value = [release]

        github_backup.backup_releases(
            args,
            "/tmp/backup/repositories/big-repo",
            repository,
            "https://api.github.com/repos/{owner}/{repo}",
            include_assets=True,
        )

        # download_file should NOT have been called (case-insensitive match)
        assert not mock_download.called

    @patch("github_backup.github_backup.download_file")
    @patch("github_backup.github_backup.retrieve_data")
    @patch("github_backup.github_backup.mkdir_p")
    @patch("github_backup.github_backup.json_dump_if_changed")
    def test_multiple_skip_repos(
        self, mock_json_dump, mock_mkdir, mock_retrieve, mock_download, create_args
    ):
        """Multiple repos in skip list should all be skipped."""
        args = create_args(skip_assets_on=["repo1", "repo2", "repo3"])
        repository = self._create_mock_repository(name="repo2")
        release = self._create_mock_release()

        mock_json_dump.return_value = True
        mock_retrieve.return_value = [release]

        github_backup.backup_releases(
            args,
            "/tmp/backup/repositories/repo2",
            repository,
            "https://api.github.com/repos/{owner}/{repo}",
            include_assets=True,
        )

        # download_file should NOT have been called
        mock_download.assert_not_called()

    @patch("github_backup.github_backup.download_file")
    @patch("github_backup.github_backup.retrieve_data")
    @patch("github_backup.github_backup.mkdir_p")
    @patch("github_backup.github_backup.json_dump_if_changed")
    def test_release_metadata_still_saved_when_assets_skipped(
        self, mock_json_dump, mock_mkdir, mock_retrieve, mock_download, create_args
    ):
        """Release JSON should still be saved even when assets are skipped."""
        args = create_args(skip_assets_on=["big-repo"])
        repository = self._create_mock_repository(name="big-repo")
        release = self._create_mock_release()

        mock_json_dump.return_value = True
        mock_retrieve.return_value = [release]

        github_backup.backup_releases(
            args,
            "/tmp/backup/repositories/big-repo",
            repository,
            "https://api.github.com/repos/{owner}/{repo}",
            include_assets=True,
        )

        # json_dump_if_changed should have been called for release metadata
        mock_json_dump.assert_called_once()
        # But download_file should NOT have been called
        mock_download.assert_not_called()

    @patch("github_backup.github_backup.download_file")
    @patch("github_backup.github_backup.retrieve_data")
    @patch("github_backup.github_backup.mkdir_p")
    @patch("github_backup.github_backup.json_dump_if_changed")
    def test_non_matching_repo_still_downloads_assets(
        self, mock_json_dump, mock_mkdir, mock_retrieve, mock_download, create_args
    ):
        """Repos not in skip list should still download assets."""
        args = create_args(skip_assets_on=["other-repo"])
        repository = self._create_mock_repository(name="normal-repo")
        release = self._create_mock_release()
        asset = self._create_mock_asset()

        mock_json_dump.return_value = True
        mock_retrieve.side_effect = [
            [release],  # First call: get releases
            [asset],  # Second call: get assets
        ]

        with patch("os.path.join", side_effect=lambda *args: "/".join(args)):
            github_backup.backup_releases(
                args,
                "/tmp/backup/repositories/normal-repo",
                repository,
                "https://api.github.com/repos/{owner}/{repo}",
                include_assets=True,
            )

        # download_file SHOULD have been called
        mock_download.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

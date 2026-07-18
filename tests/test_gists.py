"""Tests for gist backup behavior: skipping the repository listing for
gists-only backups, skipping fetches for unchanged gists, and writing
gist.json even when the clone was skipped (e.g. DMCA-blocked gists)."""

import json
import os

import pytest
from unittest.mock import patch

from github_backup.github_backup import (
    backup_repositories,
    gist_backup_is_current,
    repository_list_needed,
    retrieve_repositories,
)


class TestRepositoryListNeeded:
    """The base /user/repos listing should only be fetched when a
    per-repository resource was requested."""

    def test_gists_only_does_not_need_listing(self, create_args):
        args = create_args(include_gists=True, include_starred_gists=True)
        assert not repository_list_needed(args)

    def test_account_level_flags_do_not_need_listing(self, create_args):
        args = create_args(
            include_starred=True,
            include_watched=True,
            include_followers=True,
            include_following=True,
        )
        assert not repository_list_needed(args)

    def test_all_starred_does_not_need_listing(self, create_args):
        # starred repos come from /users/{user}/starred, not /user/repos
        args = create_args(all_starred=True)
        assert not repository_list_needed(args)

    @pytest.mark.parametrize(
        "flag",
        [
            "include_repository",
            "include_everything",
            "include_wiki",
            "include_issues",
            "include_pulls",
            "include_releases",
            "include_attachments",
        ],
    )
    def test_repository_scoped_flags_need_listing(self, create_args, flag):
        args = create_args(**{flag: True})
        assert repository_list_needed(args)

    def test_single_repository_needs_listing(self, create_args):
        args = create_args(repository="some-repo")
        assert repository_list_needed(args)

    def test_unknown_include_flag_defaults_to_needing_listing(self, create_args):
        # Fail-safe: a future include_* flag that nobody registered in
        # NON_REPOSITORY_RESOURCES must not silently skip the listing.
        args = create_args(include_some_future_resource=True)
        assert repository_list_needed(args)


class TestRetrieveRepositoriesSkipsListing:
    """retrieve_repositories should not hit the repository endpoints for a
    gists-only backup, but must still fetch gists and starred gists."""

    @patch("github_backup.github_backup.retrieve_data")
    def test_gists_only_skips_repo_listing(self, mock_retrieve, create_args):
        args = create_args(include_gists=True, include_starred_gists=True)
        mock_retrieve.return_value = [{"id": "abc123"}]

        repos = retrieve_repositories(args, {"login": "testuser"})

        requested = [call.args[1] for call in mock_retrieve.call_args_list]
        assert not any("/repos" in url for url in requested), requested
        assert any(url.endswith("/users/testuser/gists") for url in requested)
        assert any(url.endswith("/gists/starred") for url in requested)
        assert all(r["is_gist"] for r in repos)

    @patch("github_backup.github_backup.retrieve_data")
    def test_repository_backup_still_fetches_listing(self, mock_retrieve, create_args):
        args = create_args(include_repository=True)
        mock_retrieve.return_value = []

        retrieve_repositories(args, {"login": "testuser"})

        requested = [call.args[1] for call in mock_retrieve.call_args_list]
        assert any(url.endswith("/user/repos") for url in requested), requested


class TestGistBackupIsCurrent:
    """A gist fetch is skipped only when a clone exists and the stored
    gist.json updated_at matches the listing."""

    GIST = {"id": "abc123", "is_gist": True, "updated_at": "2026-07-17T10:00:00Z"}

    def _write_backup(self, repo_cwd, updated_at="2026-07-17T10:00:00Z", clone=True):
        if clone:
            os.makedirs(os.path.join(repo_cwd, "repository"))
        else:
            os.makedirs(repo_cwd)
        with open(os.path.join(repo_cwd, "gist.json"), "w") as f:
            json.dump({"id": "abc123", "updated_at": updated_at}, f)

    def test_current_when_unchanged(self, tmp_path):
        repo_cwd = str(tmp_path / "gists" / "abc123")
        self._write_backup(repo_cwd)
        assert gist_backup_is_current(
            self.GIST, repo_cwd, os.path.join(repo_cwd, "repository")
        )

    def test_not_current_when_updated(self, tmp_path):
        repo_cwd = str(tmp_path / "gists" / "abc123")
        self._write_backup(repo_cwd, updated_at="2020-01-01T00:00:00Z")
        assert not gist_backup_is_current(
            self.GIST, repo_cwd, os.path.join(repo_cwd, "repository")
        )

    def test_not_current_without_clone(self, tmp_path):
        # gist.json alone is not enough; e.g. the clone was skipped because
        # the gist was inaccessible, so keep retrying the fetch
        repo_cwd = str(tmp_path / "gists" / "abc123")
        self._write_backup(repo_cwd, clone=False)
        assert not gist_backup_is_current(
            self.GIST, repo_cwd, os.path.join(repo_cwd, "repository")
        )

    def test_not_current_with_corrupt_gist_json(self, tmp_path):
        repo_cwd = str(tmp_path / "gists" / "abc123")
        os.makedirs(os.path.join(repo_cwd, "repository"))
        with open(os.path.join(repo_cwd, "gist.json"), "w") as f:
            f.write("{not json")
        assert not gist_backup_is_current(
            self.GIST, repo_cwd, os.path.join(repo_cwd, "repository")
        )

    def test_not_current_without_updated_at(self, tmp_path):
        repo_cwd = str(tmp_path / "gists" / "abc123")
        self._write_backup(repo_cwd)
        assert not gist_backup_is_current(
            {"id": "abc123", "is_gist": True},
            repo_cwd,
            os.path.join(repo_cwd, "repository"),
        )


class TestGistBackup:
    """End-to-end behavior of backup_repositories for gists."""

    def _gist(self, **extra):
        gist = {
            "id": "abc123",
            "is_gist": True,
            "updated_at": "2026-07-17T10:00:00Z",
            "git_pull_url": "https://gist.github.com/abc123.git",
        }
        gist.update(extra)
        return gist

    @patch("github_backup.github_backup.fetch_repository")
    def test_new_gist_is_fetched_and_metadata_written(
        self, mock_fetch, create_args, tmp_path
    ):
        args = create_args(include_gists=True)

        backup_repositories(args, str(tmp_path), [self._gist()])

        mock_fetch.assert_called_once()
        gist_json = tmp_path / "gists" / "abc123" / "gist.json"
        assert json.loads(gist_json.read_text())["id"] == "abc123"

    @patch("github_backup.github_backup.fetch_repository")
    def test_unchanged_gist_skips_fetch_but_refreshes_metadata(
        self, mock_fetch, create_args, tmp_path
    ):
        args = create_args(include_gists=True)
        repo_cwd = tmp_path / "gists" / "abc123"
        (repo_cwd / "repository").mkdir(parents=True)
        (repo_cwd / "gist.json").write_text(
            json.dumps({"id": "abc123", "updated_at": "2026-07-17T10:00:00Z"})
        )

        backup_repositories(args, str(tmp_path), [self._gist(forks=5)])

        assert not mock_fetch.called, "unchanged gist should not be fetched"
        # gist.json is rewritten from the listing so metadata that changes
        # without bumping updated_at (fork counts etc.) stays fresh
        assert json.loads((repo_cwd / "gist.json").read_text())["forks"] == 5

    @patch("github_backup.github_backup.fetch_repository")
    def test_updated_gist_is_fetched(self, mock_fetch, create_args, tmp_path):
        args = create_args(include_gists=True)
        repo_cwd = tmp_path / "gists" / "abc123"
        (repo_cwd / "repository").mkdir(parents=True)
        (repo_cwd / "gist.json").write_text(
            json.dumps({"id": "abc123", "updated_at": "2020-01-01T00:00:00Z"})
        )

        backup_repositories(args, str(tmp_path), [self._gist()])

        mock_fetch.assert_called_once()

    @patch("github_backup.github_backup.fetch_repository")
    def test_inaccessible_gist_does_not_crash_backup(
        self, mock_fetch, create_args, tmp_path
    ):
        """Regression test: fetch_repository skips inaccessible gists (e.g.
        DMCA-blocked) without creating the clone directory; writing gist.json
        must not crash and the next gist must still be processed."""
        args = create_args(include_gists=True)
        # mock fetch never creates the directory, like a skipped clone
        blocked = self._gist(id="deadbeef")
        second = self._gist()

        backup_repositories(args, str(tmp_path), [blocked, second])

        assert (tmp_path / "gists" / "deadbeef" / "gist.json").is_file()
        assert (tmp_path / "gists" / "abc123" / "gist.json").is_file()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

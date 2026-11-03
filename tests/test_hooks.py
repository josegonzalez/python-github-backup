"""Tests for hooks backup permissions (GitHub issue #532).

Reading ``/repos/{owner}/{repo}/hooks`` needs admin access to the repository.
Without it GitHub responds with HTTP 404 rather than 403, which used to log an
API error for every repository the user doesn't administer.
"""

import logging
from urllib.error import HTTPError

import pytest

from github_backup import github_backup

REPOS_TEMPLATE = "https://api.github.com/repos"


@pytest.fixture
def hook_args(create_args):
    return create_args(include_hooks=True, token_classic="ghp_token")


def _repository(**fields):
    return {"full_name": "owner/repo", **fields}


def test_hooks_skipped_without_request_when_not_admin(
    hook_args, tmp_path, monkeypatch, caplog
):
    def fail_retrieve_data(*args, **kwargs):
        raise AssertionError("hooks should not be requested without admin access")

    monkeypatch.setattr(github_backup, "retrieve_data", fail_retrieve_data)

    with caplog.at_level(logging.INFO, logger=github_backup.logger.name):
        github_backup.backup_hooks(
            hook_args,
            tmp_path,
            _repository(permissions={"admin": False, "push": True, "pull": True}),
            REPOS_TEMPLATE,
        )

    assert "Skipping hooks for owner/repo since admin access is required" in caplog.text
    assert not (tmp_path / "hooks").exists()


@pytest.mark.parametrize(
    "repository",
    [
        _repository(permissions={"admin": True, "push": True, "pull": True}),
        _repository(),
    ],
    ids=["admin", "no-permissions-field"],
)
def test_hooks_requested_when_admin_or_permissions_unknown(
    hook_args, tmp_path, monkeypatch, repository
):
    requested = []

    def fake_retrieve_data(passed_args, template, *args, **kwargs):
        requested.append(template)
        return [{"id": 1, "name": "web"}]

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    github_backup.backup_hooks(hook_args, tmp_path, repository, REPOS_TEMPLATE)

    assert requested == ["https://api.github.com/repos/owner/repo/hooks"]
    assert (tmp_path / "hooks" / "hooks.json").exists()


def test_hooks_404_is_skipped_with_reason(hook_args, tmp_path, monkeypatch, caplog):
    def fake_retrieve_data(passed_args, template, *args, **kwargs):
        raise HTTPError(template, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    with caplog.at_level(logging.INFO, logger=github_backup.logger.name):
        github_backup.backup_hooks(
            hook_args,
            tmp_path,
            _repository(permissions={"admin": True}),
            REPOS_TEMPLATE,
        )

    assert "Unable to read hooks for owner/repo, skipping" in caplog.text


def test_hooks_non_404_error_propagates(hook_args, tmp_path, monkeypatch):
    def fake_retrieve_data(passed_args, template, *args, **kwargs):
        raise HTTPError(template, 500, "Server Error", hdrs=None, fp=None)

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    with pytest.raises(HTTPError):
        github_backup.backup_hooks(hook_args, tmp_path, _repository(), REPOS_TEMPLATE)

"""Tests for repositories with pull requests disabled (GitHub issue #511).

When pull requests are disabled on a repository, the ``/pulls`` endpoint
responds with HTTP 404. The backup should treat that as "no pull requests"
and continue, rather than aborting the whole run. (The ``/issues`` endpoint
returns 200 with an empty list when issues are disabled, so it needs no such
handling.)
"""

import logging
from urllib.error import HTTPError

from github_backup import github_backup


def _http_error(template, code, reason):
    return HTTPError(template, code, reason, hdrs=None, fp=None)


def test_backup_pulls_skips_on_404(create_args, tmp_path, monkeypatch, caplog):
    args = create_args(include_pulls=True, since=None)
    repository = {"full_name": "owner/repo"}

    def fake_retrieve_data(passed_args, template, query_args=None, lazy=False, **kwargs):
        # retrieve_data is called lazily for the pull listing; the 404 must
        # surface while iterating the returned generator.
        def gen():
            raise _http_error(template, 404, "Not Found")
            yield  # pragma: no cover - generator marker

        if lazy:
            return gen()
        raise _http_error(template, 404, "Not Found")

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    # Should not raise, and should log that it skipped.
    with caplog.at_level(logging.INFO, logger=github_backup.logger.name):
        github_backup.backup_pulls(
            args, tmp_path, repository, "https://api.github.com/repos"
        )

    assert "Pull requests are disabled for this repository, skipping" in caplog.text

    pulls_dir = tmp_path / "pulls"
    if pulls_dir.exists():
        assert not [p for p in pulls_dir.iterdir() if p.suffix == ".json"]


def test_backup_pulls_reraises_non_404(create_args, tmp_path, monkeypatch):
    args = create_args(include_pulls=True, since=None)
    repository = {"full_name": "owner/repo"}

    def fake_retrieve_data(passed_args, template, query_args=None, lazy=False, **kwargs):
        def gen():
            raise _http_error(template, 500, "Server Error")
            yield  # pragma: no cover - generator marker

        if lazy:
            return gen()
        raise _http_error(template, 500, "Server Error")

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    try:
        github_backup.backup_pulls(
            args, tmp_path, repository, "https://api.github.com/repos"
        )
    except HTTPError as exc:
        assert exc.code == 500
    else:
        raise AssertionError("Expected non-404 error to propagate")


def test_backup_pulls_details_individual_404_propagates(
    create_args, tmp_path, monkeypatch
):
    # With --pull-details the listing succeeds (feature is enabled), but an
    # individual pull's detail fetch 404s (e.g. deleted mid-backup). That must
    # propagate, NOT be swallowed as "pull requests are disabled".
    args = create_args(include_pulls=True, include_pull_details=True, since=None)
    repository = {"full_name": "owner/repo"}

    listing = "https://api.github.com/repos/owner/repo/pulls"

    def fake_retrieve_data(passed_args, template, query_args=None, lazy=False, **kwargs):
        if template == listing:
            # Listing works fine -> pull requests are clearly not disabled.
            def gen():
                yield {"number": 1, "updated_at": "2026-02-01T00:00:00Z"}

            return gen()
        # Individual pull detail fetch (.../pulls/1) is missing.
        raise _http_error(template, 404, "Not Found")

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    try:
        github_backup.backup_pulls(
            args, tmp_path, repository, "https://api.github.com/repos"
        )
    except HTTPError as exc:
        assert exc.code == 404
    else:
        raise AssertionError("Expected individual-pull 404 to propagate")

"""Tests for --incremental-by-files timestamp comparison.

A saved file is skipped when its modification time is newer than the item's
``updated_at``. GitHub's timestamps are UTC, so the file's modification time
must be compared in UTC too, whatever the local time zone is.
"""

import calendar
import json
import os
import time

import pytest

from github_backup import github_backup

UPDATED_AT = "2026-07-01T12:00:00Z"


@pytest.fixture
def east_of_utc(monkeypatch):
    """Run the test with the local time zone at UTC+10 (no daylight saving)."""
    monkeypatch.setenv("TZ", "Etc/GMT-10")
    time.tzset()
    yield
    monkeypatch.undo()
    time.tzset()


def _stored(path, number, written_at):
    """Save an item file whose modification time is ``written_at`` (UTC)."""
    path.mkdir(parents=True, exist_ok=True)
    item_file = path / "{0}.json".format(number)
    item_file.write_text(json.dumps({"number": number, "title": "stored"}))
    mtime = calendar.timegm(time.strptime(written_at, "%Y-%m-%dT%H:%M:%SZ"))
    os.utime(item_file, (mtime, mtime))
    return item_file


def _fake_retrieve(items):
    def _retrieve(args, template, query_args=None, **kwargs):
        return items if template.endswith(("/issues", "/pulls")) else []

    return _retrieve


@pytest.mark.parametrize(
    "written_at, refetched",
    [
        ("2026-07-01T10:00:00Z", True),  # updated 2 hours after it was saved
        ("2026-07-01T14:00:00Z", False),  # saved 2 hours after the update
    ],
)
def test_issue_skip_compares_in_utc(
    create_args, tmp_path, monkeypatch, east_of_utc, written_at, refetched
):
    issue_file = _stored(tmp_path / "issues", 1, written_at)
    issue = {"number": 1, "title": "updated", "updated_at": UPDATED_AT}
    monkeypatch.setattr(github_backup, "retrieve_data", _fake_retrieve([issue]))
    args = create_args(include_issues=True, incremental_by_files=True, since=None)

    github_backup.backup_issues(
        args, str(tmp_path), {"full_name": "owner/repo"}, "https://api.github.com/repos"
    )

    title = json.loads(issue_file.read_text())["title"]
    assert title == ("updated" if refetched else "stored")


@pytest.mark.parametrize(
    "written_at, refetched",
    [
        ("2026-07-01T10:00:00Z", True),
        ("2026-07-01T14:00:00Z", False),
    ],
)
def test_pull_skip_compares_in_utc(
    create_args, tmp_path, monkeypatch, east_of_utc, written_at, refetched
):
    pull_file = _stored(tmp_path / "pulls", 1, written_at)
    pull = {"number": 1, "title": "updated", "updated_at": UPDATED_AT}
    monkeypatch.setattr(github_backup, "retrieve_data", _fake_retrieve([pull]))
    args = create_args(include_pulls=True, incremental_by_files=True, since=None)

    github_backup.backup_pulls(
        args, str(tmp_path), {"full_name": "owner/repo"}, "https://api.github.com/repos"
    )

    title = json.loads(pull_file.read_text())["title"]
    assert title == ("updated" if refetched else "stored")


@pytest.mark.parametrize(
    "written_at, refetched",
    [
        ("2026-07-01T10:00:00Z", True),
        ("2026-07-01T14:00:00Z", False),
    ],
)
def test_discussion_skip_compares_in_utc(
    create_args, tmp_path, monkeypatch, east_of_utc, written_at, refetched
):
    discussion_file = _stored(tmp_path / "discussions", 1, written_at)
    summary = {"number": 1, "updatedAt": UPDATED_AT}
    monkeypatch.setattr(
        github_backup,
        "retrieve_discussion_summaries",
        lambda args, repository, since=None: ([summary], UPDATED_AT, True, 1),
    )
    monkeypatch.setattr(
        github_backup,
        "retrieve_discussion",
        lambda args, repository, number: {"number": number, "title": "updated"},
    )
    args = create_args(
        include_discussions=True, incremental_by_files=True, token_classic="ghp_test"
    )

    github_backup.backup_discussions(args, str(tmp_path), {"full_name": "owner/repo"})

    title = json.loads(discussion_file.read_text())["title"]
    assert title == ("updated" if refetched else "stored")


def test_checkpoint_fallback_time_is_utc(east_of_utc):
    before = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    checkpoint = github_backup.get_repository_checkpoint_time({})
    after = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    assert before <= checkpoint <= after

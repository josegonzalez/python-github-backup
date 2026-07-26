"""Tests for issue timeline backup (GitHub issue #168).

The ``/issues/{number}/events`` endpoint never returns cross-reference events
("mentioned in #22"); GitHub only exposes those via ``/issues/{number}/timeline``.
``--issue-timeline`` backs up the timeline alongside the events, so those
references are captured.
"""

import json

from github_backup import github_backup


def _issue(number=1, **extra):
    issue = {
        "number": number,
        "title": "an issue",
        "updated_at": "2026-07-01T00:00:00Z",
    }
    issue.update(extra)
    return issue


def _fake_retrieve(responses, calls):
    """Return a retrieve_data stub serving ``responses`` keyed by URL suffix."""

    def _retrieve(args, template, query_args=None, **kwargs):
        calls.append(template)
        for suffix, payload in responses.items():
            if template.endswith(suffix):
                return payload
        return []

    return _retrieve


def _run(create_args, tmp_path, monkeypatch, responses, **arg_overrides):
    args = create_args(include_issues=True, since=None, **arg_overrides)
    calls = []
    monkeypatch.setattr(
        github_backup, "retrieve_data", _fake_retrieve(responses, calls)
    )
    github_backup.backup_issues(
        args, str(tmp_path), {"full_name": "owner/repo"}, "https://api.github.com/repos"
    )
    issue_file = tmp_path / "issues" / "1.json"
    assert issue_file.is_file(), "issue was not written to disk"
    return json.loads(issue_file.read_text()), calls


def test_parse_args_issue_timeline_flag():
    # The create_args fixture sets attributes directly, so only this test
    # catches the flag being wired to the wrong dest.
    args = github_backup.parse_args(["--issue-timeline", "testuser"])
    assert args.include_issue_timeline is True


TIMELINE = [
    {"id": 1, "event": "labeled", "label": {"name": "bug"}},
    {"event": "cross-referenced", "source": {"type": "issue", "issue": {"number": 22}}},
    {"id": 2, "event": "commented", "body": "a comment body"},
    {"event": "committed", "sha": "abc123"},
]


def test_comments_filtered_and_everything_else_stored_verbatim(
    create_args, tmp_path, monkeypatch
):
    saved, calls = _run(
        create_args,
        tmp_path,
        monkeypatch,
        {"/issues": [_issue()], "/1/timeline": TIMELINE},
        include_issue_timeline=True,
    )

    assert any(c.endswith("/1/timeline") for c in calls)
    # "commented" is dropped because --issue-comments already covers it.
    # Everything else is stored exactly as GitHub returned it, including the
    # fat source object on cross-references.
    assert saved["timeline_data"] == [TIMELINE[0], TIMELINE[1], TIMELINE[3]]


def test_timeline_not_fetched_without_flag(create_args, tmp_path, monkeypatch):
    saved, calls = _run(
        create_args,
        tmp_path,
        monkeypatch,
        {"/issues": [_issue()], "/1/timeline": TIMELINE},
    )

    assert not any(c.endswith("/1/timeline") for c in calls)
    assert "timeline_data" not in saved


def test_events_unchanged_by_timeline_flag(create_args, tmp_path, monkeypatch):
    """--issue-events keeps reading /events, so event_data's shape is untouched."""
    events = [{"id": 1, "event": "labeled", "label": {"name": "bug"}}]
    saved, calls = _run(
        create_args,
        tmp_path,
        monkeypatch,
        {"/issues": [_issue()], "/1/events": events, "/1/timeline": TIMELINE},
        include_issue_events=True,
        include_issue_timeline=True,
    )

    assert any(c.endswith("/1/events") for c in calls)
    assert saved["event_data"] == events
    assert len(saved["timeline_data"]) == 3


def test_timeline_included_in_all(create_args, tmp_path, monkeypatch):
    saved, calls = _run(
        create_args,
        tmp_path,
        monkeypatch,
        {"/issues": [_issue()], "/1/timeline": TIMELINE},
        include_everything=True,
    )

    assert any(c.endswith("/1/timeline") for c in calls)
    assert len(saved["timeline_data"]) == 3

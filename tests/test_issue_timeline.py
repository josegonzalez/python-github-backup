"""Tests for issue timeline backup (GitHub issue #168).

The ``/issues/{number}/events`` endpoint never returns cross-reference events
("mentioned in #22"); GitHub only exposes those via ``/issues/{number}/timeline``.
``--issue-timeline`` backs up the timeline alongside the events, so those
references are captured.
"""

import json
import os
import time

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


def _issue_node(number, count, newest):
    """An issues-connection node: totalCount honours the itemTypes filter."""
    return {
        "number": number,
        "timelineItems": {
            "totalCount": count,
            "nodes": [{"createdAt": newest}] if newest else [],
        },
    }


def _pull_node(number, stamps):
    """A pullRequests-connection node.

    GitHub's totalCount ignores itemTypes here, so it is deliberately wrong:
    anything reading it instead of counting the nodes will fail these tests.
    """
    return {
        "number": number,
        "timelineItems": {
            "totalCount": 999,
            "nodes": [{"createdAt": s} for s in stamps],
        },
    }


def _graphql_pages(issue_pages, pull_pages=None):
    """Stub retrieve_graphql_data serving one or more pages per connection."""
    pages = {"issues": issue_pages, "pullRequests": pull_pages or [[]]}
    seen = []

    def _retrieve(args, query, variables=None, log_context=None):
        connection = "pullRequests" if "pullRequests" in query else "issues"
        cursor = (variables or {}).get("after")
        index = 0 if cursor is None else int(cursor)
        seen.append((connection, cursor))
        nodes = pages[connection][index]
        has_next = index + 1 < len(pages[connection])
        return {
            "repository": {
                connection: {
                    "nodes": nodes,
                    "pageInfo": {
                        "hasNextPage": has_next,
                        "endCursor": str(index + 1) if has_next else None,
                    },
                }
            }
        }

    _retrieve.seen = seen
    return _retrieve


def _graphql_state(counts):
    """Single-page issues-only stub, keyed {number: (count, newest)}."""
    return _graphql_pages(
        [[_issue_node(n, c, newest) for n, (c, newest) in counts.items()]]
    )


def _sweep_args(create_args, **overrides):
    """Args for the cross-reference sweep, which needs a token to reach GraphQL."""
    return create_args(token_classic="faketoken", **overrides)


def _stored(tmp_path, number, timeline_data):
    issues = tmp_path / "issues"
    issues.mkdir(parents=True, exist_ok=True)
    (issues / "{0}.json".format(number)).write_text(
        json.dumps({"number": number, "timeline_data": timeline_data})
    )
    return str(issues)


def _xref(created_at):
    return {"event": "cross-referenced", "created_at": created_at}


def test_stale_when_a_cross_reference_is_added(create_args, tmp_path, monkeypatch):
    issue_cwd = _stored(tmp_path, 1, [_xref("2026-01-01T00:00:00Z")])
    monkeypatch.setattr(
        github_backup,
        "retrieve_graphql_data",
        _graphql_state({1: (2, "2026-07-01T00:00:00Z")}),
    )

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args), issue_cwd, {"full_name": "owner/repo"}
    )

    assert stale == {1}


def test_stale_when_one_added_and_one_deleted(create_args, tmp_path, monkeypatch):
    """The count is unchanged, so only the newest timestamp reveals the change."""
    issue_cwd = _stored(
        tmp_path, 1, [_xref("2026-01-01T00:00:00Z"), _xref("2026-02-01T00:00:00Z")]
    )
    monkeypatch.setattr(
        github_backup,
        "retrieve_graphql_data",
        _graphql_state({1: (2, "2026-07-01T00:00:00Z")}),
    )

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args), issue_cwd, {"full_name": "owner/repo"}
    )

    assert stale == {1}


def test_not_stale_when_unchanged(create_args, tmp_path, monkeypatch):
    issue_cwd = _stored(tmp_path, 1, [_xref("2026-01-01T00:00:00Z")])
    monkeypatch.setattr(
        github_backup,
        "retrieve_graphql_data",
        _graphql_state({1: (1, "2026-01-01T00:00:00Z")}),
    )

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args), issue_cwd, {"full_name": "owner/repo"}
    )

    assert stale == set()


def test_graphql_failure_warns_and_continues(
    create_args, tmp_path, monkeypatch, caplog
):
    """A backup must not abort because the cross-reference check failed."""
    issue_cwd = _stored(tmp_path, 1, [])

    def _boom(*a, **kw):
        raise Exception("GraphQL unavailable")

    monkeypatch.setattr(github_backup, "retrieve_graphql_data", _boom)

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args), issue_cwd, {"full_name": "owner/repo"}
    )

    assert stale == set()
    assert "may be missed" in caplog.text


def test_stale_issue_backed_up_though_since_excludes_it(
    create_args, tmp_path, monkeypatch
):
    """A sweep-only issue refreshes just its timeline and preserves its data."""
    issue_cwd = tmp_path / "issues"
    issue_cwd.mkdir()
    stored = _issue(
        7,
        body="stored body",
        comment_data=[{"id": 1, "body": "stored comment"}],
        event_data=[{"id": 2, "event": "referenced"}],
        timeline_data=[],
    )
    (issue_cwd / "7.json").write_text(json.dumps(stored))
    args = _sweep_args(
        create_args,
        include_issues=True,
        include_issue_comments=True,
        include_issue_events=True,
        include_issue_timeline=True,
        include_attachments=True,
        since="2026-07-01T00:00:00Z",
    )
    timeline = [_xref("2026-07-20T00:00:00Z")]
    calls = []
    monkeypatch.setattr(
        github_backup,
        "retrieve_data",
        _fake_retrieve({"/issues": [], "/7/timeline": timeline}, calls),
    )
    monkeypatch.setattr(
        github_backup,
        "retrieve_graphql_data",
        _graphql_state({7: (1, "2026-07-20T00:00:00Z")}),
    )
    attachment_calls = []
    monkeypatch.setattr(
        github_backup,
        "download_attachments",
        lambda *args, **kwargs: attachment_calls.append((args, kwargs)),
    )

    github_backup.backup_issues(
        args, str(tmp_path), {"full_name": "owner/repo"}, "https://api.github.com/repos"
    )

    saved = json.loads((issue_cwd / "7.json").read_text())
    assert saved["timeline_data"] == timeline
    assert saved["body"] == "stored body"
    assert saved["comment_data"] == stored["comment_data"]
    assert saved["event_data"] == stored["event_data"]
    assert calls == [
        "https://api.github.com/repos/owner/repo/issues",
        "https://api.github.com/repos/owner/repo/issues",
        "https://api.github.com/repos/owner/repo/issues/7/timeline",
    ]
    assert attachment_calls == []


def test_sweep_follows_pagination_cursors(create_args, tmp_path, monkeypatch):
    """A cursor bug would silently truncate the sweep and strand later issues."""
    issue_cwd = _stored(tmp_path, 1, [])
    _stored(tmp_path, 2, [])
    _stored(tmp_path, 3, [])
    fake = _graphql_pages(
        [
            [_issue_node(1, 0, None)],
            [_issue_node(2, 0, None)],
            [_issue_node(3, 1, "2026-07-01T00:00:00Z")],
        ]
    )
    monkeypatch.setattr(github_backup, "retrieve_graphql_data", fake)

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args), issue_cwd, {"full_name": "owner/repo"}
    )

    # Issue 3 is only reachable by following two cursors.
    assert stale == {3}
    assert [c for _, c in fake.seen] == [None, "1", "2"]


def test_pull_requests_are_counted_from_nodes_not_total_count(
    create_args, tmp_path, monkeypatch
):
    """totalCount ignores the itemTypes filter on pull requests, so it lies."""
    issue_cwd = _stored(tmp_path, 5, [_xref("2026-01-01T00:00:00Z")])
    monkeypatch.setattr(
        github_backup,
        "retrieve_graphql_data",
        _graphql_pages([[]], [[_pull_node(5, ["2026-01-01T00:00:00Z"])]]),
    )

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args),
        issue_cwd,
        {"full_name": "owner/repo"},
        include_pulls=True,
    )

    # Stored state matches, so nothing to do. Reading totalCount (999) instead
    # of counting the one node would flag this pull request on every run.
    assert stale == set()


def test_pull_requests_not_swept_when_backed_up_separately(
    create_args, tmp_path, monkeypatch
):
    issue_cwd = _stored(tmp_path, 5, [])
    fake = _graphql_pages([[]], [[_pull_node(5, ["2026-07-01T00:00:00Z"])]])
    monkeypatch.setattr(github_backup, "retrieve_graphql_data", fake)

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args),
        issue_cwd,
        {"full_name": "owner/repo"},
        include_pulls=False,
    )

    assert stale == set()
    assert [connection for connection, _ in fake.seen] == ["issues"]


def test_truncated_node_count_compares_on_timestamp_only(
    create_args, tmp_path, monkeypatch
):
    """At the node limit the count is unreliable; comparing it loops forever."""
    limit = github_backup.CROSS_REFERENCE_NODE_LIMIT
    stamps = [
        "2026-01-01T{0:02d}:{1:02d}:00Z".format(i // 60, i % 60) for i in range(limit)
    ]
    # Stored has more cross-references than a single page can return.
    stored = [_xref(s) for s in stamps] + [_xref("2025-12-01T00:00:00Z")]
    issue_cwd = _stored(tmp_path, 5, stored)
    monkeypatch.setattr(
        github_backup,
        "retrieve_graphql_data",
        _graphql_pages([[]], [[_pull_node(5, stamps)]]),
    )

    stale = github_backup.find_stale_timeline_issues(
        _sweep_args(create_args),
        issue_cwd,
        {"full_name": "owner/repo"},
        include_pulls=True,
    )

    # Counts differ (101 stored vs 100 returned) but the newest matches, so
    # this must not be reported stale on every run.
    assert stale == set()


def test_incremental_by_files_still_refreshes_cross_referenced_issues(
    create_args, tmp_path, monkeypatch
):
    """--incremental-by-files sets no since, and skips by mtime, so the
    cross-reference sweep is the only thing that can catch these."""
    _stored(tmp_path, 3, [])
    issue_file = tmp_path / "issues" / "3.json"
    os.utime(issue_file, (0, time.time()))  # mtime newer than updated_at

    args = _sweep_args(
        create_args,
        include_issues=True,
        include_issue_timeline=True,
        incremental_by_files=True,
        since=None,
    )
    timeline = [_xref("2026-07-20T00:00:00Z")]
    monkeypatch.setattr(
        github_backup,
        "retrieve_data",
        _fake_retrieve({"/issues": [_issue(3)], "/3/timeline": timeline}, []),
    )
    monkeypatch.setattr(
        github_backup,
        "retrieve_graphql_data",
        _graphql_pages([[_issue_node(3, 1, "2026-07-20T00:00:00Z")]]),
    )

    github_backup.backup_issues(
        args, str(tmp_path), {"full_name": "owner/repo"}, "https://api.github.com/repos"
    )

    saved = json.loads(issue_file.read_text())
    assert saved["timeline_data"] == timeline

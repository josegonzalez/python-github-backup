"""Tests for GitHub Discussions backup support."""

import json
import os
from unittest.mock import patch

from github_backup import github_backup


def test_parse_args_discussions_flag():
    args = github_backup.parse_args(["--discussions", "testuser"])
    assert args.include_discussions is True


def test_retrieve_discussion_summaries_stops_at_incremental_since(create_args):
    args = create_args()
    repository = {"full_name": "owner/repo"}

    page = {
        "repository": {
            "hasDiscussionsEnabled": True,
            "discussions": {
                "totalCount": 3,
                "nodes": [
                    {"number": 3, "title": "new", "updatedAt": "2026-02-01T00:00:00Z"},
                    {"number": 2, "title": "also new", "updatedAt": "2026-01-10T00:00:00Z"},
                    {"number": 1, "title": "old", "updatedAt": "2025-12-01T00:00:00Z"},
                ],
                "pageInfo": {"hasNextPage": True, "endCursor": "NEXT"},
            },
        }
    }

    with patch(
        "github_backup.github_backup.retrieve_graphql_data", return_value=page
    ) as mock_retrieve:
        summaries, newest, enabled, total = github_backup.retrieve_discussion_summaries(
            args, repository, since="2026-01-01T00:00:00Z"
        )

    assert enabled is True
    assert total == 3
    assert newest == "2026-02-01T00:00:00Z"
    assert [item["number"] for item in summaries] == [3, 2]
    # The old discussion stops pagination, so the next page is not requested.
    assert mock_retrieve.call_count == 1


def test_retrieve_discussion_summaries_excludes_checkpoint_timestamp(create_args):
    args = create_args()
    repository = {"full_name": "owner/repo"}

    page = {
        "repository": {
            "hasDiscussionsEnabled": True,
            "discussions": {
                "totalCount": 1,
                "nodes": [
                    {
                        "number": 1,
                        "title": "already backed up",
                        "updatedAt": "2026-01-01T00:00:00Z",
                    },
                ],
                "pageInfo": {"hasNextPage": True, "endCursor": "NEXT"},
            },
        }
    }

    with patch(
        "github_backup.github_backup.retrieve_graphql_data", return_value=page
    ) as mock_retrieve:
        summaries, newest, enabled, total = github_backup.retrieve_discussion_summaries(
            args, repository, since="2026-01-01T00:00:00Z"
        )

    assert enabled is True
    assert total == 1
    assert newest == "2026-01-01T00:00:00Z"
    assert summaries == []
    assert mock_retrieve.call_count == 1


def test_retrieve_discussion_summaries_disabled_discussions(create_args):
    args = create_args()
    repository = {"full_name": "owner/repo"}

    with patch(
        "github_backup.github_backup.retrieve_graphql_data",
        return_value={"repository": {"hasDiscussionsEnabled": False}},
    ):
        summaries, newest, enabled, total = github_backup.retrieve_discussion_summaries(
            args, repository
        )

    assert summaries == []
    assert newest is None
    assert enabled is False
    assert total == 0


def _comment(comment_id, body, replies=None, replies_has_next=False):
    replies = replies or []
    return {
        "id": comment_id,
        "body": body,
        "replies": {
            "totalCount": len(replies) + (1 if replies_has_next else 0),
            "nodes": replies,
            "pageInfo": {
                "hasNextPage": replies_has_next,
                "endCursor": "REPLIES2" if replies_has_next else None,
            },
        },
    }


def _discussion_page(comment_nodes, has_next=False):
    return {
        "repository": {
            "discussion": {
                "number": 42,
                "title": "Discussion title",
                "updatedAt": "2026-02-01T00:00:00Z",
                "comments": {
                    "totalCount": 2,
                    "nodes": comment_nodes,
                    "pageInfo": {
                        "hasNextPage": has_next,
                        "endCursor": "COMMENTS2" if has_next else None,
                    },
                },
            }
        }
    }


def test_retrieve_discussion_paginates_comments_and_replies(create_args):
    args = create_args()
    repository = {"full_name": "owner/repo"}

    reply_1 = {"id": "reply-1", "body": "first reply"}
    reply_2 = {"id": "reply-2", "body": "second reply"}
    comment_1 = _comment("comment-1", "first comment", [reply_1], replies_has_next=True)
    comment_2 = _comment("comment-2", "second comment")

    responses = [
        _discussion_page([comment_1], has_next=True),
        {
            "node": {
                "replies": {
                    "totalCount": 2,
                    "nodes": [reply_2],
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                }
            }
        },
        _discussion_page([comment_2], has_next=False),
    ]

    with patch(
        "github_backup.github_backup.retrieve_graphql_data", side_effect=responses
    ) as mock_retrieve:
        discussion = github_backup.retrieve_discussion(args, repository, 42)

    assert discussion["number"] == 42
    assert discussion["comment_count"] == 2
    assert len(discussion["comment_data"]) == 2
    assert discussion["comment_data"][0]["body"] == "first comment"
    assert discussion["comment_data"][0]["reply_count"] == 2
    assert [r["body"] for r in discussion["comment_data"][0]["reply_data"]] == [
        "first reply",
        "second reply",
    ]
    assert discussion["comment_data"][1]["body"] == "second comment"
    assert mock_retrieve.call_count == 3


def test_backup_discussions_uses_incremental_checkpoint(create_args, tmp_path):
    args = create_args(token_classic="fake_token", include_discussions=True, incremental=True)
    repository = {"full_name": "owner/repo"}
    discussions_dir = tmp_path / "discussions"
    discussions_dir.mkdir()
    (discussions_dir / "last_update").write_text("2026-01-01T00:00:00Z")

    def fake_summaries(passed_args, passed_repository, since=None):
        assert passed_args is args
        assert passed_repository == repository
        assert since == "2026-01-01T00:00:00Z"
        return (
            [{"number": 7, "title": "updated", "updatedAt": "2026-02-01T00:00:00Z"}],
            "2026-02-01T00:00:00Z",
            True,
            1,
        )

    with patch(
        "github_backup.github_backup.retrieve_discussion_summaries",
        side_effect=fake_summaries,
    ), patch(
        "github_backup.github_backup.retrieve_discussion",
        return_value={"number": 7, "title": "updated"},
    ):
        github_backup.backup_discussions(args, tmp_path, repository)

    with open(discussions_dir / "7.json", encoding="utf-8") as f:
        assert json.load(f) == {"number": 7, "title": "updated"}
    assert (discussions_dir / "last_update").read_text() == "2026-02-01T00:00:00Z"


def test_backup_discussions_does_not_advance_checkpoint_on_discussion_error(
    create_args, tmp_path
):
    args = create_args(token_classic="fake_token", include_discussions=True, incremental=True)
    repository = {"full_name": "owner/repo"}
    discussions_dir = tmp_path / "discussions"
    discussions_dir.mkdir()
    (discussions_dir / "last_update").write_text("2026-01-01T00:00:00Z")

    with patch(
        "github_backup.github_backup.retrieve_discussion_summaries",
        return_value=(
            [{"number": 7, "title": "updated", "updatedAt": "2026-02-01T00:00:00Z"}],
            "2026-02-01T00:00:00Z",
            True,
            1,
        ),
    ), patch(
        "github_backup.github_backup.retrieve_discussion",
        side_effect=Exception("temporary GraphQL error"),
    ):
        github_backup.backup_discussions(args, tmp_path, repository)

    assert (discussions_dir / "last_update").read_text() == "2026-01-01T00:00:00Z"
    assert not os.path.exists(discussions_dir / "7.json")


def test_backup_discussions_skips_without_auth(create_args, tmp_path):
    args = create_args(include_discussions=True)
    repository = {"full_name": "owner/repo"}

    with patch("github_backup.github_backup.retrieve_discussion_summaries") as mock_retrieve:
        github_backup.backup_discussions(args, tmp_path, repository)

    assert not mock_retrieve.called
    assert not os.path.exists(tmp_path / "discussions")

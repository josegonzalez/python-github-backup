"""Tests for pull request review backups."""

import json
import os

from github_backup import github_backup


def test_parse_args_pull_reviews_flag():
    args = github_backup.parse_args(["--pull-reviews", "testuser"])
    assert args.include_pull_reviews is True


def test_backup_pulls_includes_review_data(create_args, tmp_path, monkeypatch):
    args = create_args(include_pulls=True, include_pull_reviews=True)
    repository = {"full_name": "owner/repo"}
    calls = []

    def fake_retrieve_data(passed_args, template, query_args=None, paginated=True, **kwargs):
        calls.append((template, query_args))
        if template == "https://api.github.com/repos/owner/repo/pulls":
            if query_args["state"] == "open":
                return [
                    {
                        "number": 1,
                        "updated_at": "2026-02-01T00:00:00Z",
                        "title": "Add feature",
                    }
                ]
            return []
        if template == "https://api.github.com/repos/owner/repo/pulls/1/reviews":
            return [
                {
                    "id": 123,
                    "state": "APPROVED",
                    "body": "Looks good",
                    "submitted_at": "2026-02-01T00:00:00Z",
                }
            ]
        raise AssertionError("Unexpected template: {0}".format(template))

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    github_backup.backup_pulls(
        args, tmp_path, repository, "https://api.github.com/repos"
    )

    with open(tmp_path / "pulls" / "1.json", encoding="utf-8") as f:
        pull = json.load(f)

    assert pull["review_data"] == [
        {
            "body": "Looks good",
            "id": 123,
            "state": "APPROVED",
            "submitted_at": "2026-02-01T00:00:00Z",
        }
    ]
    assert (
        "https://api.github.com/repos/owner/repo/pulls/1/reviews",
        None,
    ) in calls


def test_pull_reviews_backfill_ignores_repository_checkpoint(
    create_args, tmp_path, monkeypatch
):
    args = create_args(
        include_pulls=True,
        include_pull_reviews=True,
        incremental=True,
    )
    args.since = "2026-01-01T00:00:00Z"
    repository = {"full_name": "owner/repo"}

    def fake_retrieve_data(passed_args, template, query_args=None, paginated=True, **kwargs):
        if template == "https://api.github.com/repos/owner/repo/pulls":
            if query_args["state"] == "open":
                return [
                    {
                        "number": 1,
                        "updated_at": "2025-01-01T00:00:00Z",
                        "title": "Old pull request",
                    }
                ]
            return []
        if template == "https://api.github.com/repos/owner/repo/pulls/1/reviews":
            return [{"id": 123, "state": "APPROVED"}]
        raise AssertionError("Unexpected template: {0}".format(template))

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    github_backup.backup_pulls(
        args, tmp_path, repository, "https://api.github.com/repos"
    )

    with open(tmp_path / "pulls" / "1.json", encoding="utf-8") as f:
        pull = json.load(f)

    assert pull["review_data"] == [{"id": 123, "state": "APPROVED"}]
    assert (tmp_path / "pulls" / "reviews_last_update").read_text() == (
        "2025-01-01T00:00:00Z"
    )


def test_pull_reviews_uses_review_checkpoint_when_older_than_repository_checkpoint(
    create_args, tmp_path, monkeypatch
):
    args = create_args(
        include_pulls=True,
        include_pull_reviews=True,
        incremental=True,
    )
    args.since = "2026-01-01T00:00:00Z"
    repository = {"full_name": "owner/repo"}
    pulls_dir = tmp_path / "pulls"
    pulls_dir.mkdir()
    (pulls_dir / "reviews_last_update").write_text("2025-01-01T00:00:00Z")

    def fake_retrieve_data(passed_args, template, query_args=None, paginated=True, **kwargs):
        if template == "https://api.github.com/repos/owner/repo/pulls":
            if query_args["state"] == "open":
                return [
                    {
                        "number": 1,
                        "updated_at": "2025-06-01T00:00:00Z",
                        "title": "Review changed while feature was disabled",
                    },
                    {
                        "number": 2,
                        "updated_at": "2024-12-01T00:00:00Z",
                        "title": "Too old",
                    },
                ]
            return []
        if template == "https://api.github.com/repos/owner/repo/pulls/1/reviews":
            return [{"id": 123, "state": "COMMENTED"}]
        raise AssertionError("Unexpected template: {0}".format(template))

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    github_backup.backup_pulls(
        args, tmp_path, repository, "https://api.github.com/repos"
    )

    assert os.path.exists(tmp_path / "pulls" / "1.json")
    assert not os.path.exists(tmp_path / "pulls" / "2.json")
    assert (tmp_path / "pulls" / "reviews_last_update").read_text() == (
        "2025-06-01T00:00:00Z"
    )


def test_pull_reviews_preserves_existing_optional_pull_data(
    create_args, tmp_path, monkeypatch
):
    args = create_args(include_pulls=True, include_pull_reviews=True)
    repository = {"full_name": "owner/repo"}
    pulls_dir = tmp_path / "pulls"
    pulls_dir.mkdir()
    with open(pulls_dir / "1.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "number": 1,
                "updated_at": "2026-01-01T00:00:00Z",
                "comment_data": [{"id": 10, "body": "inline comment"}],
                "comment_regular_data": [{"id": 11, "body": "regular comment"}],
                "commit_data": [{"sha": "abc"}],
            },
            f,
        )

    def fake_retrieve_data(passed_args, template, query_args=None, paginated=True, **kwargs):
        if template == "https://api.github.com/repos/owner/repo/pulls":
            if query_args["state"] == "open":
                return [
                    {
                        "number": 1,
                        "updated_at": "2026-02-01T00:00:00Z",
                        "title": "Add reviews",
                    }
                ]
            return []
        if template == "https://api.github.com/repos/owner/repo/pulls/1/reviews":
            return [{"id": 123, "state": "APPROVED"}]
        raise AssertionError("Unexpected template: {0}".format(template))

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    github_backup.backup_pulls(
        args, tmp_path, repository, "https://api.github.com/repos"
    )

    with open(pulls_dir / "1.json", encoding="utf-8") as f:
        pull = json.load(f)

    assert pull["review_data"] == [{"id": 123, "state": "APPROVED"}]
    assert pull["comment_data"] == [{"id": 10, "body": "inline comment"}]
    assert pull["comment_regular_data"] == [{"id": 11, "body": "regular comment"}]
    assert pull["commit_data"] == [{"sha": "abc"}]


def test_pull_reviews_does_not_advance_checkpoint_on_review_error(
    create_args, tmp_path, monkeypatch
):
    args = create_args(
        include_pulls=True,
        include_pull_reviews=True,
        incremental=True,
    )
    args.since = "2026-01-01T00:00:00Z"
    repository = {"full_name": "owner/repo"}
    pulls_dir = tmp_path / "pulls"
    pulls_dir.mkdir()
    (pulls_dir / "reviews_last_update").write_text("2025-01-01T00:00:00Z")

    def fake_retrieve_data(passed_args, template, query_args=None, paginated=True, **kwargs):
        if template == "https://api.github.com/repos/owner/repo/pulls":
            if query_args["state"] == "open":
                return [
                    {
                        "number": 1,
                        "updated_at": "2025-06-01T00:00:00Z",
                        "title": "Review retrieval fails",
                    }
                ]
            return []
        if template == "https://api.github.com/repos/owner/repo/pulls/1/reviews":
            raise Exception("temporary API failure")
        raise AssertionError("Unexpected template: {0}".format(template))

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    github_backup.backup_pulls(
        args, tmp_path, repository, "https://api.github.com/repos"
    )

    assert (pulls_dir / "reviews_last_update").read_text() == "2025-01-01T00:00:00Z"

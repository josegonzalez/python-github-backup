"""Tests for behavior of backups ran for temporary private forks."""

import json
from unittest.mock import patch
from urllib.error import HTTPError

from github_backup import github_backup


def _repo(name, updated_at, pushed_at=None):
    return {
        "name": name,
        "full_name": "owner/{0}".format(name),
        "owner": {"login": "owner"},
        "clone_url": "https://github.com/owner/{0}.git".format(name),
        "private": True,
        "fork": False,
        "has_issues": False,
        "has_projects": False,
        "has_downloads": False,
        "has_wiki": False,
        "has_pages": False,
        "has_discussions": False,
        "updated_at": updated_at,
        "pushed_at": pushed_at,
    }


def _pull_comments_page(comment_nodes, total_count, has_next=False):
    return {
        "repository": {
            "pullRequest": {
                "comments": {
                    "totalCount": total_count,
                    "nodes": comment_nodes,
                    "pageInfo": {
                        "hasNextPage": has_next,
                        "endCursor": "COMMENTS2" if has_next else None,
                    },
                },
            }
        }
    }


# This is an end-to-end test of a full repository backup that's supposed to ensure that
# everything in the process can handle most of the REST API endpoints returning 404s
# without raising errors.
def test_temporary_private_fork_backup_handles_limited_api_endpoints_with_no_errors(
    create_args, tmp_path, monkeypatch
):
    args = create_args(include_everything=True, private=True)
    repo_name = "repo-one-ghsa-01ab-34cd-56ef"
    repositories = [_repo(repo_name, "2026-02-01T00:00:00Z")]
    repo_cwd = tmp_path / "repositories" / repo_name
    pull_file = repo_cwd / "pulls" / "1.json"

    expected_dirs = {"pulls"}
    base_pr_data = {"number": 1, "updated_at": "2026-01-01T00:00:00Z"}
    regular_comments = [{"id": 2, "body": "regular comment"}]
    review_comments = [{"id": 3, "body": "review comment"}]
    commits = [{"sha": "abc"}]

    def fake_retrieve_graphql_data(args, query, variables=None, log_context=None):
        if query == github_backup.PULL_COMMENTS_QUERY:
            return _pull_comments_page(regular_comments, len(regular_comments))
        else:
            raise AssertionError(f"request made with unknown query: {query}")

    def fake_retrieve_data(
        passed_args, template, query_args=None, lazy=False, **kwargs
    ):
        def gen():
            if template.endswith("/pulls"):
                yield base_pr_data
            elif template.endswith("/pulls/1/comments"):
                yield from review_comments
            elif template.endswith("/pulls/1/commits"):
                yield from commits
            else:
                # anything other than above should just be assumed to return 404
                raise HTTPError(template, 404, "Not Found", hdrs=None, fp=None)

        if lazy:
            return gen()
        return list(gen())

    monkeypatch.setattr(
        github_backup, "retrieve_graphql_data", fake_retrieve_graphql_data
    )
    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    with patch("github_backup.github_backup.fetch_repository"):
        github_backup.backup_repositories(args, tmp_path, repositories)

    actual_dirs = {p.name for p in repo_cwd.iterdir()}
    assert expected_dirs == actual_dirs

    pr_data = json.loads(pull_file.read_text())
    for key in base_pr_data:
        assert pr_data[key] == base_pr_data[key]
    assert pr_data["comment_regular_data"] == regular_comments
    assert pr_data["comment_data"] == review_comments
    assert pr_data["commit_data"] == commits


def test_get_pull_comments_with_graphql_paginates(create_args):
    args = create_args()
    repository = {"full_name": "owner/repo"}

    comment_1 = {"id": "comment-1", "body": "first comment"}
    comment_2 = {"id": "comment-2", "body": "second comment"}
    comment_3 = {"id": "comment-3", "body": "third comment"}
    total_count = 3

    responses = [
        _pull_comments_page([comment_1, comment_2], total_count, has_next=True),
        _pull_comments_page([comment_3], total_count, has_next=False),
    ]

    with patch(
        "github_backup.github_backup.retrieve_graphql_data", side_effect=responses
    ) as mock_retrieve:
        comment_data = github_backup.get_pull_comments_with_graphql(
            args, repository, 42
        )

    assert len(comment_data) == total_count
    assert comment_data[0]["body"] == "first comment"
    assert comment_data[1]["body"] == "second comment"
    assert comment_data[2]["body"] == "third comment"
    assert mock_retrieve.call_count == 2
    assert [call.kwargs["log_context"] for call in mock_retrieve.call_args_list] == [
        "pull request owner/repo#42 comments page 1",
        "pull request owner/repo#42 comments page 2",
    ]

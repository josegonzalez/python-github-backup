"""Tests for per-resource incremental checkpoints."""

import json
import os

from github_backup import github_backup


def _repo(name, updated_at, pushed_at=None):
    return {
        "name": name,
        "full_name": "owner/{0}".format(name),
        "owner": {"login": "owner"},
        "clone_url": "https://github.com/owner/{0}.git".format(name),
        "private": False,
        "fork": False,
        "has_wiki": False,
        "updated_at": updated_at,
        "pushed_at": pushed_at,
    }


def test_incremental_uses_per_resource_last_update(
    create_args, tmp_path, monkeypatch
):
    args = create_args(incremental=True, include_issues=True)
    repositories = [
        _repo("repo-one", "2026-02-01T00:00:00Z"),
        _repo("repo-two", "2026-03-01T00:00:00Z"),
    ]
    repo_one_issues = tmp_path / "repositories" / "repo-one" / "issues"
    repo_two_issues = tmp_path / "repositories" / "repo-two" / "issues"
    repo_one_issues.mkdir(parents=True)
    repo_two_issues.mkdir(parents=True)
    (repo_one_issues / "last_update").write_text("2026-01-01T00:00:00Z")
    (repo_two_issues / "last_update").write_text("2025-01-01T00:00:00Z")

    seen_since = []

    def fake_backup_issues(passed_args, repo_cwd, repository, repos_template):
        seen_since.append((repository["name"], passed_args.since))

    monkeypatch.setattr(github_backup, "backup_issues", fake_backup_issues)

    github_backup.backup_repositories(args, tmp_path, repositories)

    assert seen_since == [
        ("repo-one", "2026-01-01T00:00:00Z"),
        ("repo-two", "2025-01-01T00:00:00Z"),
    ]
    assert (repo_one_issues / "last_update").read_text() == "2026-02-01T00:00:00Z"
    assert (repo_two_issues / "last_update").read_text() == "2026-03-01T00:00:00Z"
    assert not os.path.exists(tmp_path / "last_update")


def test_incremental_uses_independent_issue_and_pull_checkpoints(
    create_args, tmp_path, monkeypatch
):
    args = create_args(incremental=True, include_issues=True, include_pulls=True)
    repository = _repo("repo-one", "2026-02-01T00:00:00Z")
    repo_dir = tmp_path / "repositories" / "repo-one"
    issues_dir = repo_dir / "issues"
    pulls_dir = repo_dir / "pulls"
    issues_dir.mkdir(parents=True)
    pulls_dir.mkdir(parents=True)
    (issues_dir / "last_update").write_text("2026-01-01T00:00:00Z")
    (pulls_dir / "last_update").write_text("2025-01-01T00:00:00Z")

    seen_since = []

    def fake_backup_issues(passed_args, repo_cwd, repository, repos_template):
        seen_since.append(("issues", passed_args.since))

    def fake_backup_pulls(passed_args, repo_cwd, repository, repos_template):
        seen_since.append(("pulls", passed_args.since))

    monkeypatch.setattr(github_backup, "backup_issues", fake_backup_issues)
    monkeypatch.setattr(github_backup, "backup_pulls", fake_backup_pulls)

    github_backup.backup_repositories(args, tmp_path, [repository])

    assert seen_since == [
        ("issues", "2026-01-01T00:00:00Z"),
        ("pulls", "2025-01-01T00:00:00Z"),
    ]
    assert (issues_dir / "last_update").read_text() == "2026-02-01T00:00:00Z"
    assert (pulls_dir / "last_update").read_text() == "2026-02-01T00:00:00Z"


def test_incremental_uses_legacy_global_last_update_for_existing_resource_backup(
    create_args, tmp_path, monkeypatch
):
    args = create_args(incremental=True, include_issues=True)
    repository = _repo("repo-one", "2026-02-01T00:00:00Z")
    (tmp_path / "last_update").write_text("2026-01-01T00:00:00Z")
    issues_dir = tmp_path / "repositories" / "repo-one" / "issues"
    issues_dir.mkdir(parents=True)
    with open(issues_dir / "1.json", "w", encoding="utf-8") as f:
        json.dump({"number": 1}, f)

    seen_since = []

    def fake_backup_issues(passed_args, repo_cwd, repository, repos_template):
        seen_since.append(passed_args.since)

    monkeypatch.setattr(github_backup, "backup_issues", fake_backup_issues)

    github_backup.backup_repositories(args, tmp_path, [repository])

    assert seen_since == ["2026-01-01T00:00:00Z"]
    assert (issues_dir / "last_update").read_text() == "2026-02-01T00:00:00Z"
    assert not os.path.exists(tmp_path / "last_update")


def test_incremental_does_not_use_legacy_global_last_update_for_new_resource_backup(
    create_args, tmp_path, monkeypatch
):
    args = create_args(incremental=True, include_issues=True)
    repository = _repo("repo-one", "2026-02-01T00:00:00Z")
    (tmp_path / "last_update").write_text("2099-01-01T00:00:00Z")

    seen_since = []

    def fake_backup_issues(passed_args, repo_cwd, repository, repos_template):
        seen_since.append(passed_args.since)

    monkeypatch.setattr(github_backup, "backup_issues", fake_backup_issues)

    github_backup.backup_repositories(args, tmp_path, [repository])

    assert seen_since == [None]
    assert (
        tmp_path / "repositories" / "repo-one" / "issues" / "last_update"
    ).read_text() == "2026-02-01T00:00:00Z"
    assert not os.path.exists(tmp_path / "last_update")


def test_incremental_keeps_legacy_global_last_update_until_all_existing_resources_migrated(
    create_args, tmp_path, monkeypatch
):
    args = create_args(incremental=True, include_issues=True)
    repository = _repo("repo-one", "2026-02-01T00:00:00Z")
    (tmp_path / "last_update").write_text("2026-01-01T00:00:00Z")
    repo_one_issues = tmp_path / "repositories" / "repo-one" / "issues"
    repo_two_issues = tmp_path / "repositories" / "repo-two" / "issues"
    repo_one_issues.mkdir(parents=True)
    repo_two_issues.mkdir(parents=True)
    with open(repo_one_issues / "1.json", "w", encoding="utf-8") as f:
        json.dump({"number": 1}, f)
    with open(repo_two_issues / "2.json", "w", encoding="utf-8") as f:
        json.dump({"number": 2}, f)

    def fake_backup_issues(passed_args, repo_cwd, repository, repos_template):
        pass

    monkeypatch.setattr(github_backup, "backup_issues", fake_backup_issues)

    github_backup.backup_repositories(args, tmp_path, [repository])

    assert (repo_one_issues / "last_update").read_text() == "2026-02-01T00:00:00Z"
    assert not os.path.exists(repo_two_issues / "last_update")
    assert (tmp_path / "last_update").read_text() == "2026-01-01T00:00:00Z"


def test_incremental_does_not_remove_legacy_checkpoint_without_resource_work(
    create_args, tmp_path
):
    args = create_args(incremental=True, include_repository=True)
    repository = _repo("repo-one", "2026-02-01T00:00:00Z")
    (tmp_path / "last_update").write_text("2026-01-01T00:00:00Z")

    github_backup.backup_repositories(args, tmp_path, [repository])

    assert (tmp_path / "last_update").read_text() == "2026-01-01T00:00:00Z"
    assert not os.path.exists(
        tmp_path / "repositories" / "repo-one" / "issues" / "last_update"
    )


def test_repository_checkpoint_time_uses_newest_available_repo_timestamp():
    repository = _repo(
        "repo-one",
        updated_at="2026-02-01T00:00:00Z",
        pushed_at="2026-03-01T00:00:00Z",
    )

    assert github_backup.get_repository_checkpoint_time(repository) == (
        "2026-03-01T00:00:00Z"
    )

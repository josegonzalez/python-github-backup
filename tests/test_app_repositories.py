"""Tests for listing a user's repositories with a GitHub App installation token."""

from unittest.mock import patch

import pytest

from github_backup import github_backup

NO_USER = {"login": None}


def page(*names):
    return {
        "total_count": 3,
        "repositories": [{"name": name, "private": True} for name in names],
    }


@pytest.fixture
def mock_retrieve_data():
    with patch("github_backup.github_backup.retrieve_data") as mock:
        yield mock


def test_app_lists_user_repositories_from_installation(create_args, mock_retrieve_data):
    args = create_args(as_app=True, include_repository=True)
    mock_retrieve_data.return_value = [page("a", "b"), page("c")]

    repos = github_backup.retrieve_repositories(args, NO_USER)

    assert mock_retrieve_data.call_args.args[1] == (
        "https://api.github.com/installation/repositories"
    )
    assert [r["name"] for r in repos] == ["a", "b", "c"]


def test_app_installation_listing_uses_ghes_host(create_args, mock_retrieve_data):
    args = create_args(
        as_app=True, include_repository=True, github_host="ghe.example.com"
    )
    mock_retrieve_data.return_value = [page("a")]

    github_backup.retrieve_repositories(args, NO_USER)

    assert mock_retrieve_data.call_args.args[1] == (
        "https://ghe.example.com/api/v3/installation/repositories"
    )


def test_app_organization_still_lists_org_repositories(create_args, mock_retrieve_data):
    args = create_args(as_app=True, include_repository=True, organization=True)
    mock_retrieve_data.return_value = [{"name": "a"}]

    repos = github_backup.retrieve_repositories(args, NO_USER)

    assert mock_retrieve_data.call_args.args[1] == (
        "https://api.github.com/orgs/testuser/repos"
    )
    assert repos == [{"name": "a"}]


def test_app_single_repository_is_fetched_directly(create_args, mock_retrieve_data):
    args = create_args(as_app=True, repository="dotfiles")
    mock_retrieve_data.return_value = [{"name": "dotfiles"}]

    repos = github_backup.retrieve_repositories(args, NO_USER)

    assert mock_retrieve_data.call_args.args[1] == (
        "https://api.github.com/repos/testuser/dotfiles"
    )
    assert repos == [{"name": "dotfiles"}]

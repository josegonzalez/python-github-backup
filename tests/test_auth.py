"""Tests for authentication helpers."""

from unittest.mock import patch

import pytest

from github_backup import github_backup


def test_token_from_gh_flag_parses():
    args = github_backup.parse_args(["--token-from-gh", "testuser"])
    assert args.token_from_gh is True


def test_get_auth_reads_token_from_gh_cli(create_args):
    args = create_args(token_from_gh=True)

    with patch(
        "github_backup.github_backup.subprocess.check_output",
        return_value=b"gho_test_token\n",
    ) as mock_check_output:
        auth = github_backup.get_auth(args, encode=False)

    assert auth == "gho_test_token:x-oauth-basic"
    mock_check_output.assert_called_once_with(
        ["gh", "auth", "token"], stderr=github_backup.subprocess.PIPE
    )


def test_get_auth_reads_token_from_gh_cli_for_enterprise_host(create_args):
    args = create_args(token_from_gh=True, github_host="ghe.example.com")

    with patch(
        "github_backup.github_backup.subprocess.check_output",
        return_value=b"gho_enterprise_token\n",
    ) as mock_check_output:
        auth = github_backup.get_auth(args, encode=False)

    assert auth == "gho_enterprise_token:x-oauth-basic"
    mock_check_output.assert_called_once_with(
        ["gh", "auth", "token", "--hostname", "ghe.example.com"],
        stderr=github_backup.subprocess.PIPE,
    )


def test_token_from_gh_is_cached(create_args):
    args = create_args(token_from_gh=True)

    with patch(
        "github_backup.github_backup.subprocess.check_output",
        return_value=b"gho_cached_token\n",
    ) as mock_check_output:
        assert github_backup.get_auth(args, encode=False) == "gho_cached_token:x-oauth-basic"
        assert github_backup.get_auth(args, encode=False) == "gho_cached_token:x-oauth-basic"

    mock_check_output.assert_called_once()


def test_token_from_gh_rejects_as_app(create_args):
    args = create_args(token_from_gh=True, as_app=True)

    with pytest.raises(Exception) as exc_info:
        github_backup.get_auth(args, encode=False)

    assert "--token-from-gh cannot be used with --as-app" in str(exc_info.value)

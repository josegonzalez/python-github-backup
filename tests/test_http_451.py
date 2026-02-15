"""Tests for HTTP 451 (DMCA takedown) and HTTP 403 (TOS) handling."""

import io
import json
from unittest.mock import patch
from urllib.error import HTTPError

import pytest

from github_backup import github_backup


def _make_http_error(code, body_bytes, msg="Error", headers=None):
    """Create an HTTPError with a readable body (like a real urllib response)."""
    if headers is None:
        headers = {"x-ratelimit-remaining": "5000"}
    return HTTPError(
        url="https://api.github.com/repos/test/repo",
        code=code,
        msg=msg,
        hdrs=headers,
        fp=io.BytesIO(body_bytes),
    )


class TestHTTP451Exception:
    """Test suite for HTTP 451 DMCA takedown exception handling."""

    def test_repository_unavailable_error_raised(self, create_args):
        """HTTP 451 should raise RepositoryUnavailableError with DMCA URL."""
        args = create_args()

        dmca_data = {
            "message": "Repository access blocked",
            "block": {
                "reason": "dmca",
                "created_at": "2024-11-12T14:38:04Z",
                "html_url": "https://github.com/github/dmca/blob/master/2024/11/2024-11-04-source-code.md",
            },
        }
        body = json.dumps(dmca_data).encode("utf-8")

        def mock_urlopen(*a, **kw):
            raise _make_http_error(451, body, msg="Unavailable For Legal Reasons")

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with pytest.raises(github_backup.RepositoryUnavailableError) as exc_info:
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/dmca/issues"
                )

            assert (
                exc_info.value.legal_url
                == "https://github.com/github/dmca/blob/master/2024/11/2024-11-04-source-code.md"
            )
            assert "451" in str(exc_info.value)

    def test_repository_unavailable_error_without_legal_url(self, create_args):
        """HTTP 451 without DMCA details should still raise exception."""
        args = create_args()

        def mock_urlopen(*a, **kw):
            raise _make_http_error(451, b'{"message": "Blocked"}')

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with pytest.raises(github_backup.RepositoryUnavailableError) as exc_info:
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/dmca/issues"
                )

            assert exc_info.value.legal_url is None
            assert "451" in str(exc_info.value)

    def test_repository_unavailable_error_with_malformed_json(self, create_args):
        """HTTP 451 with malformed JSON should still raise exception."""
        args = create_args()

        def mock_urlopen(*a, **kw):
            raise _make_http_error(451, b"invalid json {")

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with pytest.raises(github_backup.RepositoryUnavailableError):
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/dmca/issues"
                )


class TestHTTP403TOS:
    """Test suite for HTTP 403 TOS violation handling."""

    def test_403_tos_raises_repository_unavailable(self, create_args):
        """HTTP 403 (non-rate-limit) should raise RepositoryUnavailableError."""
        args = create_args()

        tos_data = {
            "message": "Repository access blocked",
            "block": {
                "reason": "tos",
                "html_url": "https://github.com/contact/tos-violation",
            },
        }
        body = json.dumps(tos_data).encode("utf-8")

        def mock_urlopen(*a, **kw):
            raise _make_http_error(
                403,
                body,
                msg="Forbidden",
                headers={"x-ratelimit-remaining": "5000"},
            )

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with pytest.raises(github_backup.RepositoryUnavailableError) as exc_info:
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/blocked/issues"
                )

            assert (
                exc_info.value.legal_url == "https://github.com/contact/tos-violation"
            )
            assert "403" in str(exc_info.value)

    def test_403_permission_denied_not_converted(self, create_args):
        """HTTP 403 without 'block' in body should propagate as HTTPError, not RepositoryUnavailableError."""
        args = create_args()

        body = json.dumps({"message": "Must have admin rights to Repository."}).encode(
            "utf-8"
        )

        def mock_urlopen(*a, **kw):
            raise _make_http_error(
                403,
                body,
                msg="Forbidden",
                headers={"x-ratelimit-remaining": "5000"},
            )

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with pytest.raises(HTTPError) as exc_info:
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/private/issues"
                )

            assert exc_info.value.code == 403

    def test_403_rate_limit_not_converted(self, create_args):
        """HTTP 403 with rate limit exhausted should NOT become RepositoryUnavailableError."""
        args = create_args()

        call_count = 0

        def mock_urlopen(*a, **kw):
            nonlocal call_count
            call_count += 1
            raise _make_http_error(
                403,
                b'{"message": "rate limit"}',
                msg="Forbidden",
                headers={"x-ratelimit-remaining": "0"},
            )

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with patch(
                "github_backup.github_backup.calculate_retry_delay", return_value=0
            ):
                with pytest.raises(HTTPError) as exc_info:
                    github_backup.retrieve_data(
                        args, "https://api.github.com/repos/test/ratelimit/issues"
                    )

            assert exc_info.value.code == 403
            # Should have retried (not raised immediately as RepositoryUnavailableError)
            assert call_count > 1


class TestRetrieveRepositoriesUnavailable:
    """Test that retrieve_repositories handles RepositoryUnavailableError gracefully."""

    def test_unavailable_repo_returns_empty_list(self, create_args):
        """retrieve_repositories should return [] when the repo is unavailable."""
        args = create_args(repository="blocked-repo")

        def mock_urlopen(*a, **kw):
            raise _make_http_error(
                451,
                json.dumps(
                    {
                        "message": "Blocked",
                        "block": {"html_url": "https://example.com/dmca"},
                    }
                ).encode("utf-8"),
                msg="Unavailable For Legal Reasons",
            )

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            repos = github_backup.retrieve_repositories(args, {"login": None})

        assert repos == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

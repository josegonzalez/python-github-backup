"""Tests for HTTP 451 (DMCA takedown) handling."""

import json
from unittest.mock import Mock, patch

import pytest

from github_backup import github_backup


class TestHTTP451Exception:
    """Test suite for HTTP 451 DMCA takedown exception handling."""

    def test_repository_unavailable_error_raised(self, create_args):
        """HTTP 451 should raise RepositoryUnavailableError with DMCA URL."""
        args = create_args()

        mock_response = Mock()
        mock_response.getcode.return_value = 451

        dmca_data = {
            "message": "Repository access blocked",
            "block": {
                "reason": "dmca",
                "created_at": "2024-11-12T14:38:04Z",
                "html_url": "https://github.com/github/dmca/blob/master/2024/11/2024-11-04-source-code.md",
            },
        }
        mock_response.read.return_value = json.dumps(dmca_data).encode("utf-8")
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Unavailable For Legal Reasons"

        with patch(
            "github_backup.github_backup.make_request_with_retry",
            return_value=mock_response,
        ):
            with pytest.raises(github_backup.RepositoryUnavailableError) as exc_info:
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/dmca/issues"
                )

            assert (
                exc_info.value.dmca_url
                == "https://github.com/github/dmca/blob/master/2024/11/2024-11-04-source-code.md"
            )
            assert "451" in str(exc_info.value)

    def test_repository_unavailable_error_without_dmca_url(self, create_args):
        """HTTP 451 without DMCA details should still raise exception."""
        args = create_args()

        mock_response = Mock()
        mock_response.getcode.return_value = 451
        mock_response.read.return_value = b'{"message": "Blocked"}'
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Unavailable For Legal Reasons"

        with patch(
            "github_backup.github_backup.make_request_with_retry",
            return_value=mock_response,
        ):
            with pytest.raises(github_backup.RepositoryUnavailableError) as exc_info:
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/dmca/issues"
                )

            assert exc_info.value.dmca_url is None
            assert "451" in str(exc_info.value)

    def test_repository_unavailable_error_with_malformed_json(self, create_args):
        """HTTP 451 with malformed JSON should still raise exception."""
        args = create_args()

        mock_response = Mock()
        mock_response.getcode.return_value = 451
        mock_response.read.return_value = b"invalid json {"
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Unavailable For Legal Reasons"

        with patch(
            "github_backup.github_backup.make_request_with_retry",
            return_value=mock_response,
        ):
            with pytest.raises(github_backup.RepositoryUnavailableError):
                github_backup.retrieve_data(
                    args, "https://api.github.com/repos/test/dmca/issues"
                )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

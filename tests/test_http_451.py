"""Tests for HTTP 451 (DMCA takedown) handling."""

import json
from unittest.mock import Mock, patch

import pytest

from github_backup import github_backup


class TestHTTP451Exception:
    """Test suite for HTTP 451 DMCA takedown exception handling."""

    def test_repository_unavailable_error_raised(self):
        """HTTP 451 should raise RepositoryUnavailableError with DMCA URL."""
        # Create mock args
        args = Mock()
        args.as_app = False
        args.token_fine = None
        args.token_classic = None
        args.username = None
        args.password = None
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None
        args.throttle_limit = None
        args.throttle_pause = 0

        # Mock HTTPError 451 response
        mock_response = Mock()
        mock_response.getcode.return_value = 451

        dmca_data = {
            "message": "Repository access blocked",
            "block": {
                "reason": "dmca",
                "created_at": "2024-11-12T14:38:04Z",
                "html_url": "https://github.com/github/dmca/blob/master/2024/11/2024-11-04-source-code.md"
            }
        }
        mock_response.read.return_value = json.dumps(dmca_data).encode("utf-8")
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Unavailable For Legal Reasons"

        def mock_get_response(request, auth, template):
            return mock_response, []

        with patch("github_backup.github_backup._get_response", side_effect=mock_get_response):
            with pytest.raises(github_backup.RepositoryUnavailableError) as exc_info:
                list(github_backup.retrieve_data_gen(args, "https://api.github.com/repos/test/dmca/issues"))

            # Check exception has DMCA URL
            assert exc_info.value.dmca_url == "https://github.com/github/dmca/blob/master/2024/11/2024-11-04-source-code.md"
            assert "451" in str(exc_info.value)

    def test_repository_unavailable_error_without_dmca_url(self):
        """HTTP 451 without DMCA details should still raise exception."""
        args = Mock()
        args.as_app = False
        args.token_fine = None
        args.token_classic = None
        args.username = None
        args.password = None
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None
        args.throttle_limit = None
        args.throttle_pause = 0

        mock_response = Mock()
        mock_response.getcode.return_value = 451
        mock_response.read.return_value = b'{"message": "Blocked"}'
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Unavailable For Legal Reasons"

        def mock_get_response(request, auth, template):
            return mock_response, []

        with patch("github_backup.github_backup._get_response", side_effect=mock_get_response):
            with pytest.raises(github_backup.RepositoryUnavailableError) as exc_info:
                list(github_backup.retrieve_data_gen(args, "https://api.github.com/repos/test/dmca/issues"))

            # Exception raised even without DMCA URL
            assert exc_info.value.dmca_url is None
            assert "451" in str(exc_info.value)

    def test_repository_unavailable_error_with_malformed_json(self):
        """HTTP 451 with malformed JSON should still raise exception."""
        args = Mock()
        args.as_app = False
        args.token_fine = None
        args.token_classic = None
        args.username = None
        args.password = None
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None
        args.throttle_limit = None
        args.throttle_pause = 0

        mock_response = Mock()
        mock_response.getcode.return_value = 451
        mock_response.read.return_value = b"invalid json {"
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Unavailable For Legal Reasons"

        def mock_get_response(request, auth, template):
            return mock_response, []

        with patch("github_backup.github_backup._get_response", side_effect=mock_get_response):
            with pytest.raises(github_backup.RepositoryUnavailableError):
                list(github_backup.retrieve_data_gen(args, "https://api.github.com/repos/test/dmca/issues"))

    def test_other_http_errors_unchanged(self):
        """Other HTTP errors should still raise generic Exception."""
        args = Mock()
        args.as_app = False
        args.token_fine = None
        args.token_classic = None
        args.username = None
        args.password = None
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None
        args.throttle_limit = None
        args.throttle_pause = 0

        mock_response = Mock()
        mock_response.getcode.return_value = 404
        mock_response.read.return_value = b'{"message": "Not Found"}'
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Not Found"

        def mock_get_response(request, auth, template):
            return mock_response, []

        with patch("github_backup.github_backup._get_response", side_effect=mock_get_response):
            # Should raise generic Exception, not RepositoryUnavailableError
            with pytest.raises(Exception) as exc_info:
                list(github_backup.retrieve_data_gen(args, "https://api.github.com/repos/test/notfound/issues"))

            assert not isinstance(exc_info.value, github_backup.RepositoryUnavailableError)
            assert "404" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

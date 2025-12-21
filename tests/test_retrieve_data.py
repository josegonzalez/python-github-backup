"""Tests for retrieve_data function."""

import json
import socket
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

import pytest

from github_backup import github_backup
from github_backup.github_backup import (
    MAX_RETRIES,
    calculate_retry_delay,
    make_request_with_retry,
)


class TestCalculateRetryDelay:
    def test_respects_retry_after_header(self):
        headers = {'retry-after': '30'}
        assert calculate_retry_delay(0, headers) == 30

    def test_respects_rate_limit_reset(self):
        import time
        import calendar
        # Set reset time 60 seconds in the future
        future_reset = calendar.timegm(time.gmtime()) + 60
        headers = {
            'x-ratelimit-remaining': '0',
            'x-ratelimit-reset': str(future_reset)
        }
        delay = calculate_retry_delay(0, headers)
        # Should be approximately 60 seconds (with some tolerance for execution time)
        assert 55 <= delay <= 65

    def test_exponential_backoff(self):
        delay_0 = calculate_retry_delay(0, {})
        delay_1 = calculate_retry_delay(1, {})
        delay_2 = calculate_retry_delay(2, {})
        # Base delay is 1s, so delays should be roughly 1, 2, 4 (plus jitter)
        assert 0.9 <= delay_0 <= 1.2  # ~1s + up to 10% jitter
        assert 1.8 <= delay_1 <= 2.4  # ~2s + up to 10% jitter
        assert 3.6 <= delay_2 <= 4.8  # ~4s + up to 10% jitter

    def test_max_delay_cap(self):
        # Very high attempt number should not exceed 120s + jitter
        delay = calculate_retry_delay(100, {})
        assert delay <= 120 * 1.1  # 120s max + 10% jitter

    def test_minimum_rate_limit_delay(self):
        import time
        import calendar
        # Set reset time in the past (already reset)
        past_reset = calendar.timegm(time.gmtime()) - 100
        headers = {
            'x-ratelimit-remaining': '0',
            'x-ratelimit-reset': str(past_reset)
        }
        delay = calculate_retry_delay(0, headers)
        # Should be minimum 10 seconds even if reset time is in past
        assert delay >= 10


class TestRetrieveDataRetry:
    """Tests for retry behavior in retrieve_data."""

    @pytest.fixture
    def mock_args(self):
        args = Mock()
        args.as_app = False
        args.token_fine = None
        args.token_classic = "fake_token"
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None
        args.throttle_limit = None
        args.throttle_pause = 0
        return args

    def test_json_parse_error_retries_and_fails(self, mock_args):
        """HTTP 200 with invalid JSON should retry and eventually fail."""
        mock_response = Mock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = b"not valid json {"
        mock_response.headers = {"x-ratelimit-remaining": "5000"}

        call_count = 0

        def mock_make_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return mock_response

        with patch("github_backup.github_backup.make_request_with_retry", side_effect=mock_make_request):
            with patch("github_backup.github_backup.calculate_retry_delay", return_value=0):  # No delay in tests
                with pytest.raises(Exception) as exc_info:
                    github_backup.retrieve_data(mock_args, "https://api.github.com/repos/test/repo/issues")

        assert "Failed to read response after" in str(exc_info.value)
        assert call_count == MAX_RETRIES

    def test_json_parse_error_recovers_on_retry(self, mock_args):
        """HTTP 200 with invalid JSON should succeed if retry returns valid JSON."""
        bad_response = Mock()
        bad_response.getcode.return_value = 200
        bad_response.read.return_value = b"not valid json {"
        bad_response.headers = {"x-ratelimit-remaining": "5000"}

        good_response = Mock()
        good_response.getcode.return_value = 200
        good_response.read.return_value = json.dumps([{"id": 1}]).encode("utf-8")
        good_response.headers = {"x-ratelimit-remaining": "5000", "Link": ""}

        responses = [bad_response, bad_response, good_response]
        call_count = 0

        def mock_make_request(*args, **kwargs):
            nonlocal call_count
            result = responses[call_count]
            call_count += 1
            return result

        with patch("github_backup.github_backup.make_request_with_retry", side_effect=mock_make_request):
            with patch("github_backup.github_backup.calculate_retry_delay", return_value=0):
                result = github_backup.retrieve_data(mock_args, "https://api.github.com/repos/test/repo/issues")

        assert result == [{"id": 1}]
        assert call_count == 3  # Failed twice, succeeded on third

    def test_http_error_raises_exception(self, mock_args):
        """Non-success HTTP status codes should raise Exception."""
        mock_response = Mock()
        mock_response.getcode.return_value = 404
        mock_response.read.return_value = b'{"message": "Not Found"}'
        mock_response.headers = {"x-ratelimit-remaining": "5000"}
        mock_response.reason = "Not Found"

        with patch("github_backup.github_backup.make_request_with_retry", return_value=mock_response):
            with pytest.raises(Exception) as exc_info:
                github_backup.retrieve_data(mock_args, "https://api.github.com/repos/test/notfound/issues")

            assert not isinstance(exc_info.value, github_backup.RepositoryUnavailableError)
            assert "404" in str(exc_info.value)


class TestMakeRequestWithRetry:
    """Tests for HTTP error retry behavior in make_request_with_retry."""

    def test_502_error_retries_and_succeeds(self):
        """HTTP 502 should retry and succeed if subsequent request works."""
        good_response = Mock()
        good_response.read.return_value = b'{"ok": true}'

        call_count = 0
        fail_count = MAX_RETRIES - 1  # Fail all but last attempt

        def mock_urlopen(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= fail_count:
                raise HTTPError(
                    url="https://api.github.com/test",
                    code=502,
                    msg="Bad Gateway",
                    hdrs={"x-ratelimit-remaining": "5000"},
                    fp=None,
                )
            return good_response

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with patch("github_backup.github_backup.calculate_retry_delay", return_value=0):
                result = make_request_with_retry(Mock(), None)

        assert result == good_response
        assert call_count == MAX_RETRIES

    def test_503_error_retries_until_exhausted(self):
        """HTTP 503 should retry MAX_RETRIES times then raise."""
        call_count = 0

        def mock_urlopen(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise HTTPError(
                url="https://api.github.com/test",
                code=503,
                msg="Service Unavailable",
                hdrs={"x-ratelimit-remaining": "5000"},
                fp=None,
            )

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with patch("github_backup.github_backup.calculate_retry_delay", return_value=0):
                with pytest.raises(HTTPError) as exc_info:
                    make_request_with_retry(Mock(), None)

        assert exc_info.value.code == 503
        assert call_count == MAX_RETRIES

    def test_404_error_not_retried(self):
        """HTTP 404 should not be retried - raise immediately."""
        call_count = 0

        def mock_urlopen(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise HTTPError(
                url="https://api.github.com/test",
                code=404,
                msg="Not Found",
                hdrs={"x-ratelimit-remaining": "5000"},
                fp=None,
            )

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with pytest.raises(HTTPError) as exc_info:
                make_request_with_retry(Mock(), None)

        assert exc_info.value.code == 404
        assert call_count == 1  # No retries

    def test_rate_limit_403_retried_when_remaining_zero(self):
        """HTTP 403 with x-ratelimit-remaining=0 should retry."""
        good_response = Mock()
        call_count = 0

        def mock_urlopen(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise HTTPError(
                    url="https://api.github.com/test",
                    code=403,
                    msg="Forbidden",
                    hdrs={"x-ratelimit-remaining": "0"},
                    fp=None,
                )
            return good_response

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with patch("github_backup.github_backup.calculate_retry_delay", return_value=0):
                result = make_request_with_retry(Mock(), None)

        assert result == good_response
        assert call_count == 2

    def test_403_not_retried_when_remaining_nonzero(self):
        """HTTP 403 with x-ratelimit-remaining>0 should not retry (permission error)."""
        call_count = 0

        def mock_urlopen(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise HTTPError(
                url="https://api.github.com/test",
                code=403,
                msg="Forbidden",
                hdrs={"x-ratelimit-remaining": "5000"},
                fp=None,
            )

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with pytest.raises(HTTPError) as exc_info:
                make_request_with_retry(Mock(), None)

        assert exc_info.value.code == 403
        assert call_count == 1  # No retries

    def test_connection_error_retries_and_succeeds(self):
        """URLError (connection error) should retry and succeed if subsequent request works."""
        good_response = Mock()
        call_count = 0
        fail_count = MAX_RETRIES - 1  # Fail all but last attempt

        def mock_urlopen(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= fail_count:
                raise URLError("Connection refused")
            return good_response

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with patch("github_backup.github_backup.calculate_retry_delay", return_value=0):
                result = make_request_with_retry(Mock(), None)

        assert result == good_response
        assert call_count == MAX_RETRIES

    def test_socket_error_retries_until_exhausted(self):
        """socket.error should retry MAX_RETRIES times then raise."""
        call_count = 0

        def mock_urlopen(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise socket.error("Connection reset by peer")

        with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
            with patch("github_backup.github_backup.calculate_retry_delay", return_value=0):
                with pytest.raises(socket.error):
                    make_request_with_retry(Mock(), None)

        assert call_count == MAX_RETRIES


class TestRetrieveDataThrottling:
    """Tests for throttling behavior in retrieve_data."""

    @pytest.fixture
    def mock_args(self):
        args = Mock()
        args.as_app = False
        args.token_fine = None
        args.token_classic = "fake_token"
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None
        args.throttle_limit = 10  # Throttle when remaining <= 10
        args.throttle_pause = 5  # Pause 5 seconds
        return args

    def test_throttling_pauses_when_rate_limit_low(self, mock_args):
        """Should pause when x-ratelimit-remaining is at or below throttle_limit."""
        mock_response = Mock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = json.dumps([{"id": 1}]).encode("utf-8")
        mock_response.headers = {"x-ratelimit-remaining": "5", "Link": ""}  # Below throttle_limit

        with patch("github_backup.github_backup.make_request_with_retry", return_value=mock_response):
            with patch("github_backup.github_backup.time.sleep") as mock_sleep:
                github_backup.retrieve_data(mock_args, "https://api.github.com/repos/test/repo/issues")

        mock_sleep.assert_called_once_with(5)  # throttle_pause value


class TestRetrieveDataSingleItem:
    """Tests for single item (dict) responses in retrieve_data."""

    @pytest.fixture
    def mock_args(self):
        args = Mock()
        args.as_app = False
        args.token_fine = None
        args.token_classic = "fake_token"
        args.osx_keychain_item_name = None
        args.osx_keychain_item_account = None
        args.throttle_limit = None
        args.throttle_pause = 0
        return args

    def test_dict_response_returned_as_list(self, mock_args):
        """Single dict response should be returned as a list with one item."""
        mock_response = Mock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = json.dumps({"login": "testuser", "id": 123}).encode("utf-8")
        mock_response.headers = {"x-ratelimit-remaining": "5000", "Link": ""}

        with patch("github_backup.github_backup.make_request_with_retry", return_value=mock_response):
            result = github_backup.retrieve_data(mock_args, "https://api.github.com/user")

        assert result == [{"login": "testuser", "id": 123}]

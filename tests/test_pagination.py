"""Tests for Link header pagination handling."""

import json
from unittest.mock import patch

from github_backup import github_backup


class MockHTTPResponse:
    """Mock HTTP response for paginated API calls."""

    def __init__(self, data, link_header=None):
        self._content = json.dumps(data).encode("utf-8")
        self._link_header = link_header
        self._read = False
        self.reason = "OK"

    def getcode(self):
        return 200

    def read(self):
        if self._read:
            return b""
        self._read = True
        return self._content

    def get_header(self, name, default=None):
        """Mock method for headers.get()."""
        return self.headers.get(name, default)

    @property
    def headers(self):
        headers = {"x-ratelimit-remaining": "5000"}
        if self._link_header:
            headers["Link"] = self._link_header
        return headers


def test_cursor_based_pagination(create_args):
    """Link header with 'after' cursor parameter works correctly."""
    args = create_args(token_classic="fake_token")

    # Simulate issues endpoint behavior: returns cursor in Link header
    responses = [
        # Issues endpoint returns 'after' cursor parameter (not 'page')
        MockHTTPResponse(
            data=[{"issue": i} for i in range(1, 101)],  # Page 1 contents
            link_header='<https://api.github.com/repos/owner/repo/issues?per_page=100&after=ABC123&page=2>; rel="next"',
        ),
        MockHTTPResponse(
            data=[{"issue": i} for i in range(101, 151)],  # Page 2 contents
            link_header=None,  # No Link header - signals end of pagination
        ),
    ]
    requests_made = []

    def mock_urlopen(request, *args, **kwargs):
        url = request.get_full_url()
        requests_made.append(url)
        return responses[len(requests_made) - 1]

    with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
        results = github_backup.retrieve_data(
            args, "https://api.github.com/repos/owner/repo/issues"
        )

    # Verify all items retrieved and cursor was used in second request
    assert len(results) == 150
    assert len(requests_made) == 2
    assert "after=ABC123" in requests_made[1]


def test_page_based_pagination(create_args):
    """Link header with 'page' parameter works correctly."""
    args = create_args(token_classic="fake_token")

    # Simulate pulls/repos endpoint behavior: returns page numbers in Link header
    responses = [
        # Pulls endpoint uses traditional 'page' parameter (not cursor)
        MockHTTPResponse(
            data=[{"pull": i} for i in range(1, 101)],  # Page 1 contents
            link_header='<https://api.github.com/repos/owner/repo/pulls?per_page=100&page=2>; rel="next"',
        ),
        MockHTTPResponse(
            data=[{"pull": i} for i in range(101, 181)],  # Page 2 contents
            link_header=None,  # No Link header - signals end of pagination
        ),
    ]
    requests_made = []

    def mock_urlopen(request, *args, **kwargs):
        url = request.get_full_url()
        requests_made.append(url)
        return responses[len(requests_made) - 1]

    with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
        results = github_backup.retrieve_data(
            args, "https://api.github.com/repos/owner/repo/pulls"
        )

    # Verify all items retrieved and page parameter was used (not cursor)
    assert len(results) == 180
    assert len(requests_made) == 2
    assert "page=2" in requests_made[1]
    assert "after" not in requests_made[1]


def test_no_link_header_stops_pagination(create_args):
    """Pagination stops when Link header is absent."""
    args = create_args(token_classic="fake_token")

    # Simulate endpoint with results that fit in a single page
    responses = [
        MockHTTPResponse(
            data=[{"label": i} for i in range(1, 51)],  # Page contents
            link_header=None,  # No Link header - signals end of pagination
        )
    ]
    requests_made = []

    def mock_urlopen(request, *args, **kwargs):
        requests_made.append(request.get_full_url())
        return responses[len(requests_made) - 1]

    with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
        results = github_backup.retrieve_data(
            args, "https://api.github.com/repos/owner/repo/labels"
        )

    # Verify pagination stopped after first request
    assert len(results) == 50
    assert len(requests_made) == 1

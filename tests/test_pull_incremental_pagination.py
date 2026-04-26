"""Tests for incremental pull request pagination."""

import json
import os
from unittest.mock import patch

from github_backup import github_backup


class MockHTTPResponse:
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

    @property
    def headers(self):
        headers = {"x-ratelimit-remaining": "5000"}
        if self._link_header:
            headers["Link"] = self._link_header
        return headers


def test_backup_pulls_incremental_stops_before_fetching_old_pages(
    create_args, tmp_path
):
    args = create_args(include_pulls=True, incremental=True)
    args.since = "2026-04-26T08:13:46Z"
    repository = {"full_name": "owner/repo"}

    responses = [
        MockHTTPResponse([]),
        MockHTTPResponse(
            [
                {
                    "number": 2,
                    "title": "new pull",
                    "updated_at": "2026-04-26T09:00:00Z",
                },
                {
                    "number": 1,
                    "title": "old pull",
                    "updated_at": "2026-04-26T07:00:00Z",
                },
            ],
            link_header='<https://api.github.com/repos/owner/repo/pulls?per_page=100&state=closed&page=2>; rel="next"',
        ),
        MockHTTPResponse(
            [
                {
                    "number": 0,
                    "title": "older pull on page 2",
                    "updated_at": "2026-04-25T07:00:00Z",
                }
            ]
        ),
    ]
    requests_made = []

    def mock_urlopen(request, *args, **kwargs):
        requests_made.append(request.get_full_url())
        return responses[len(requests_made) - 1]

    with patch("github_backup.github_backup.urlopen", side_effect=mock_urlopen):
        github_backup.backup_pulls(
            args, tmp_path, repository, "https://api.github.com/repos"
        )

    assert len(requests_made) == 2
    assert "state=open" in requests_made[0]
    assert "state=closed" in requests_made[1]
    assert all("page=2" not in url for url in requests_made)
    assert os.path.exists(tmp_path / "pulls" / "2.json")
    assert not os.path.exists(tmp_path / "pulls" / "1.json")
    assert not os.path.exists(tmp_path / "pulls" / "0.json")

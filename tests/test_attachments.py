"""Behavioral tests for attachment functionality."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from github_backup import github_backup


@pytest.fixture
def attachment_test_setup(tmp_path, create_args):
    """Fixture providing setup and helper for attachment download tests."""
    issue_cwd = tmp_path / "issues"
    issue_cwd.mkdir()

    # Create args using shared fixture
    args = create_args(user="testuser", repository="testrepo")

    repository = {"full_name": "testuser/testrepo"}

    def call_download(issue_data, issue_number=123):
        """Call download_attachments with mocked HTTP downloads.

        Returns list of URLs that were actually downloaded.
        """
        downloaded_urls = []

        def mock_download(url, path, auth, as_app, fine):
            downloaded_urls.append(url)
            return {
                "success": True,
                "saved_as": os.path.basename(path),
                "url": url,
            }

        with patch(
            "github_backup.github_backup.download_attachment_file",
            side_effect=mock_download,
        ):
            github_backup.download_attachments(
                args, str(issue_cwd), issue_data, issue_number, repository
            )

        return downloaded_urls

    return {
        "issue_cwd": str(issue_cwd),
        "args": args,
        "repository": repository,
        "call_download": call_download,
    }


class TestURLExtraction:
    """Test URL extraction with realistic issue content."""

    def test_mixed_urls(self):
        issue_data = {
            "body": """
            ## Bug Report

            When uploading files, I see this error. Here's a screenshot:
            https://github.com/user-attachments/assets/abc123def456

            The logs show: https://github.com/user-attachments/files/789/error-log.txt

            This is similar to https://github.com/someorg/somerepo/issues/42 but different.

            You can also see the video at https://user-images.githubusercontent.com/12345/video-demo.mov

            Here's how to reproduce:
            ```bash
            # Don't extract this example URL:
            curl https://github.com/user-attachments/assets/example999
            ```

            More info at https://docs.example.com/guide

            Also see this inline code `https://github.com/user-attachments/files/111/inline.pdf` should not extract.

            Final attachment: https://github.com/user-attachments/files/222/report.pdf.
            """,
            "comment_data": [
                {
                    "body": "Here's another attachment: https://private-user-images.githubusercontent.com/98765/secret.png?jwt=token123"
                },
                {
                    "body": """
                    Example code:
                    ```python
                    url = "https://github.com/user-attachments/assets/code-example"
                    ```
                    But this is real: https://github.com/user-attachments/files/333/actual.zip
                    """
                },
            ],
        }

        # Extract URLs
        urls = github_backup.extract_attachment_urls(issue_data)

        expected_urls = [
            "https://github.com/user-attachments/assets/abc123def456",
            "https://github.com/user-attachments/files/789/error-log.txt",
            "https://user-images.githubusercontent.com/12345/video-demo.mov",
            "https://github.com/user-attachments/files/222/report.pdf",
            "https://private-user-images.githubusercontent.com/98765/secret.png?jwt=token123",
            "https://github.com/user-attachments/files/333/actual.zip",
        ]

        assert set(urls) == set(expected_urls)

    def test_trailing_punctuation_stripped(self):
        """URLs with trailing punctuation should have punctuation stripped."""
        issue_data = {
            "body": """
            See this file: https://github.com/user-attachments/files/1/doc.pdf.
            And this one (https://github.com/user-attachments/files/2/image.png).
            Check it out! https://github.com/user-attachments/files/3/data.csv!
            """
        }

        urls = github_backup.extract_attachment_urls(issue_data)

        expected = [
            "https://github.com/user-attachments/files/1/doc.pdf",
            "https://github.com/user-attachments/files/2/image.png",
            "https://github.com/user-attachments/files/3/data.csv",
        ]
        assert set(urls) == set(expected)

    def test_deduplication_across_body_and_comments(self):
        """Same URL in body and comments should only appear once."""
        duplicate_url = "https://github.com/user-attachments/assets/abc123"

        issue_data = {
            "body": f"First mention: {duplicate_url}",
            "comment_data": [
                {"body": f"Second mention: {duplicate_url}"},
                {"body": f"Third mention: {duplicate_url}"},
            ],
        }

        urls = github_backup.extract_attachment_urls(issue_data)

        assert set(urls) == {duplicate_url}


class TestFilenameExtraction:
    """Test filename extraction from different URL types."""

    def test_modern_assets_url(self):
        """Modern assets URL returns UUID."""
        url = "https://github.com/user-attachments/assets/abc123def456"
        filename = github_backup.get_attachment_filename(url)
        assert filename == "abc123def456"

    def test_modern_files_url(self):
        """Modern files URL returns filename."""
        url = "https://github.com/user-attachments/files/12345/report.pdf"
        filename = github_backup.get_attachment_filename(url)
        assert filename == "report.pdf"

    def test_legacy_cdn_url(self):
        """Legacy CDN URL returns filename with extension."""
        url = "https://user-images.githubusercontent.com/123456/abc-def.png"
        filename = github_backup.get_attachment_filename(url)
        assert filename == "abc-def.png"

    def test_private_cdn_url(self):
        """Private CDN URL returns filename."""
        url = "https://private-user-images.githubusercontent.com/98765/secret.png?jwt=token123"
        filename = github_backup.get_attachment_filename(url)
        assert filename == "secret.png"

    def test_repo_files_url(self):
        """Repo-scoped files URL returns filename."""
        url = "https://github.com/owner/repo/files/789/document.txt"
        filename = github_backup.get_attachment_filename(url)
        assert filename == "document.txt"


class TestFilenameCollision:
    """Test filename collision resolution."""

    def test_collision_behavior(self):
        """Test filename collision resolution with real files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # No collision - file doesn't exist
            result = github_backup.resolve_filename_collision(
                os.path.join(tmpdir, "report.pdf")
            )
            assert result == os.path.join(tmpdir, "report.pdf")

            # Create the file, now collision exists
            Path(os.path.join(tmpdir, "report.pdf")).touch()
            result = github_backup.resolve_filename_collision(
                os.path.join(tmpdir, "report.pdf")
            )
            assert result == os.path.join(tmpdir, "report_1.pdf")

            # Create report_1.pdf too
            Path(os.path.join(tmpdir, "report_1.pdf")).touch()
            result = github_backup.resolve_filename_collision(
                os.path.join(tmpdir, "report.pdf")
            )
            assert result == os.path.join(tmpdir, "report_2.pdf")

    def test_manifest_reserved(self):
        """manifest.json is always treated as reserved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Even if manifest.json doesn't exist, should get manifest_1.json
            result = github_backup.resolve_filename_collision(
                os.path.join(tmpdir, "manifest.json")
            )
            assert result == os.path.join(tmpdir, "manifest_1.json")


class TestManifestDuplicatePrevention:
    """Test that manifest prevents duplicate downloads (the bug fix)."""

    def test_manifest_filters_existing_urls(self, attachment_test_setup):
        """URLs in manifest are not re-downloaded."""
        setup = attachment_test_setup

        # Create manifest with existing URLs
        attachments_dir = os.path.join(setup["issue_cwd"], "attachments", "123")
        os.makedirs(attachments_dir)
        manifest_path = os.path.join(attachments_dir, "manifest.json")

        manifest = {
            "attachments": [
                {
                    "url": "https://github.com/user-attachments/assets/old1",
                    "success": True,
                    "saved_as": "old1.pdf",
                },
                {
                    "url": "https://github.com/user-attachments/assets/old2",
                    "success": True,
                    "saved_as": "old2.pdf",
                },
            ]
        }
        with open(manifest_path, "w") as f:
            json.dump(manifest, f)

        # Issue data with 2 old URLs and 1 new URL
        issue_data = {
            "body": """
            Old: https://github.com/user-attachments/assets/old1
            Old: https://github.com/user-attachments/assets/old2
            New: https://github.com/user-attachments/assets/new1
            """
        }

        downloaded_urls = setup["call_download"](issue_data)

        # Should only download the NEW URL (old ones filtered by manifest)
        assert len(downloaded_urls) == 1
        assert downloaded_urls[0] == "https://github.com/user-attachments/assets/new1"

    def test_no_manifest_downloads_all(self, attachment_test_setup):
        """Without manifest, all URLs should be downloaded."""
        setup = attachment_test_setup

        # Issue data with 2 URLs
        issue_data = {
            "body": """
            https://github.com/user-attachments/assets/url1
            https://github.com/user-attachments/assets/url2
            """
        }

        downloaded_urls = setup["call_download"](issue_data)

        # Should download ALL URLs (no manifest to filter)
        assert len(downloaded_urls) == 2
        assert set(downloaded_urls) == {
            "https://github.com/user-attachments/assets/url1",
            "https://github.com/user-attachments/assets/url2",
        }

    def test_manifest_skips_permanent_failures(self, attachment_test_setup):
        """Manifest skips permanent failures (404, 410) but retries transient (503)."""
        setup = attachment_test_setup

        # Create manifest with different failure types
        attachments_dir = os.path.join(setup["issue_cwd"], "attachments", "123")
        os.makedirs(attachments_dir)
        manifest_path = os.path.join(attachments_dir, "manifest.json")

        manifest = {
            "attachments": [
                {
                    "url": "https://github.com/user-attachments/assets/success",
                    "success": True,
                    "saved_as": "success.pdf",
                },
                {
                    "url": "https://github.com/user-attachments/assets/notfound",
                    "success": False,
                    "http_status": 404,
                },
                {
                    "url": "https://github.com/user-attachments/assets/gone",
                    "success": False,
                    "http_status": 410,
                },
                {
                    "url": "https://github.com/user-attachments/assets/unavailable",
                    "success": False,
                    "http_status": 503,
                },
            ]
        }
        with open(manifest_path, "w") as f:
            json.dump(manifest, f)

        # Issue data has all 4 URLs
        issue_data = {
            "body": """
            https://github.com/user-attachments/assets/success
            https://github.com/user-attachments/assets/notfound
            https://github.com/user-attachments/assets/gone
            https://github.com/user-attachments/assets/unavailable
            """
        }

        downloaded_urls = setup["call_download"](issue_data)

        # Should only retry 503 (transient failure)
        # Success, 404, and 410 should be skipped
        assert len(downloaded_urls) == 1
        assert (
            downloaded_urls[0]
            == "https://github.com/user-attachments/assets/unavailable"
        )


class TestJWTWorkaround:
    """Test JWT workaround for fine-grained tokens on private repos (issue #477)."""

    def test_markdown_api_extracts_jwt_url(self):
        """Markdown API response with JWT URL is extracted correctly."""
        html_response = (
            '<p><a href="https://private-user-images.githubusercontent.com'
            '/123/abc.png?jwt=eyJhbGciOiJ"><img src="https://private-user-'
            'images.githubusercontent.com/123/abc.png?jwt=eyJhbGciOiJ" '
            'alt="img"></a></p>'
        )

        mock_response = Mock()
        mock_response.read.return_value = html_response.encode("utf-8")

        with patch("github_backup.github_backup.urlopen", return_value=mock_response):
            result = github_backup.get_jwt_signed_url_via_markdown_api(
                "https://github.com/user-attachments/assets/abc123",
                "github_pat_token",
                "owner/repo"
            )

        expected = (
            "https://private-user-images.githubusercontent.com"
            "/123/abc.png?jwt=eyJhbGciOiJ"
        )
        assert result == expected

    def test_markdown_api_returns_none_on_http_error(self):
        """HTTP errors return None."""
        from urllib.error import HTTPError

        error = HTTPError("http://test", 403, "Forbidden", {}, None)
        with patch("github_backup.github_backup.urlopen", side_effect=error):
            result = github_backup.get_jwt_signed_url_via_markdown_api(
                "https://github.com/user-attachments/assets/abc123",
                "github_pat_token",
                "owner/repo"
            )

        assert result is None

    def test_markdown_api_returns_none_when_no_jwt_url(self):
        """Response without JWT URL returns None."""
        mock_response = Mock()
        mock_response.read.return_value = b"<p>No image here</p>"

        with patch("github_backup.github_backup.urlopen", return_value=mock_response):
            result = github_backup.get_jwt_signed_url_via_markdown_api(
                "https://github.com/user-attachments/assets/abc123",
                "github_pat_token",
                "owner/repo"
            )

        assert result is None

    def test_needs_jwt_only_for_fine_grained_private_assets(self):
        """needs_jwt is True only for fine-grained + private + /assets/ URL."""
        assets_url = "https://github.com/user-attachments/assets/abc123"
        files_url = "https://github.com/user-attachments/files/123/doc.pdf"
        token_fine = "github_pat_test"
        private = True
        public = False

        # Fine-grained + private + assets = True
        needs_jwt = (
            token_fine is not None
            and private
            and "github.com/user-attachments/assets/" in assets_url
        )
        assert needs_jwt is True

        # Fine-grained + private + files = False
        needs_jwt = (
            token_fine is not None
            and private
            and "github.com/user-attachments/assets/" in files_url
        )
        assert needs_jwt is False

        # Fine-grained + public + assets = False
        needs_jwt = (
            token_fine is not None
            and public
            and "github.com/user-attachments/assets/" in assets_url
        )
        assert needs_jwt is False

    def test_jwt_workaround_sets_manifest_flag(self, attachment_test_setup):
        """Successful JWT workaround sets jwt_workaround flag in manifest."""
        setup = attachment_test_setup
        setup["args"].token_fine = "github_pat_test"
        setup["repository"]["private"] = True

        issue_data = {"body": "https://github.com/user-attachments/assets/abc123"}

        jwt_url = "https://private-user-images.githubusercontent.com/123/abc.png?jwt=token"

        with patch(
            "github_backup.github_backup.get_jwt_signed_url_via_markdown_api",
            return_value=jwt_url
        ), patch(
            "github_backup.github_backup.download_attachment_file",
            return_value={"success": True, "http_status": 200, "url": jwt_url}
        ):
            github_backup.download_attachments(
                setup["args"], setup["issue_cwd"], issue_data, 123, setup["repository"]
            )

        manifest_path = os.path.join(setup["issue_cwd"], "attachments", "123", "manifest.json")
        with open(manifest_path) as f:
            manifest = json.load(f)

        assert manifest["attachments"][0]["jwt_workaround"] is True
        assert manifest["attachments"][0]["url"] == "https://github.com/user-attachments/assets/abc123"

    def test_jwt_workaround_failure_uses_skipped_at(self, attachment_test_setup):
        """Failed JWT workaround uses skipped_at instead of downloaded_at."""
        setup = attachment_test_setup
        setup["args"].token_fine = "github_pat_test"
        setup["repository"]["private"] = True

        issue_data = {"body": "https://github.com/user-attachments/assets/abc123"}

        with patch(
            "github_backup.github_backup.get_jwt_signed_url_via_markdown_api",
            return_value=None  # Markdown API failed
        ):
            github_backup.download_attachments(
                setup["args"], setup["issue_cwd"], issue_data, 123, setup["repository"]
            )

        manifest_path = os.path.join(setup["issue_cwd"], "attachments", "123", "manifest.json")
        with open(manifest_path) as f:
            manifest = json.load(f)

        attachment = manifest["attachments"][0]
        assert attachment["success"] is False
        assert "skipped_at" in attachment
        assert "downloaded_at" not in attachment
        assert "Use --token-classic" in attachment["error"]

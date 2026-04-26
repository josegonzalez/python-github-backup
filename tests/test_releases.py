"""Tests for release backup behavior."""

from github_backup import github_backup


def test_backup_releases_uses_embedded_assets_without_extra_asset_list_request(
    create_args, tmp_path, monkeypatch
):
    args = create_args(include_releases=True, include_assets=True)
    repository = {"full_name": "owner/repo", "name": "repo"}
    calls = []
    downloads = []

    def fake_retrieve_data(passed_args, template, query_args=None, paginated=True, **kwargs):
        calls.append(template)
        if template == "https://api.github.com/repos/owner/repo/releases":
            return [
                {
                    "tag_name": "v1.0.0",
                    "created_at": "2026-01-01T00:00:00Z",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "prerelease": False,
                    "draft": False,
                    "assets_url": "https://api.github.com/repos/owner/repo/releases/1/assets",
                    "assets": [
                        {
                            "name": "artifact.zip",
                            "url": "https://api.github.com/repos/owner/repo/releases/assets/1",
                        }
                    ],
                }
            ]
        raise AssertionError("Unexpected API request: {0}".format(template))

    def fake_download_file(url, path, auth, as_app=False, fine=False):
        downloads.append((url, path))

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)
    monkeypatch.setattr(github_backup, "download_file", fake_download_file)

    github_backup.backup_releases(
        args,
        tmp_path,
        repository,
        "https://api.github.com/repos",
        include_assets=True,
    )

    assert calls == ["https://api.github.com/repos/owner/repo/releases"]
    assert downloads == [
        (
            "https://api.github.com/repos/owner/repo/releases/assets/1",
            str(tmp_path / "releases" / "v1.0.0" / "artifact.zip"),
        )
    ]


def test_backup_releases_falls_back_to_assets_url_when_assets_missing(
    create_args, tmp_path, monkeypatch
):
    args = create_args(include_releases=True, include_assets=True)
    repository = {"full_name": "owner/repo", "name": "repo"}
    calls = []

    def fake_retrieve_data(passed_args, template, query_args=None, paginated=True, **kwargs):
        calls.append(template)
        if template == "https://api.github.com/repos/owner/repo/releases":
            return [
                {
                    "tag_name": "v1.0.0",
                    "created_at": "2026-01-01T00:00:00Z",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "prerelease": False,
                    "draft": False,
                    "assets_url": "https://api.github.com/repos/owner/repo/releases/1/assets",
                }
            ]
        if template == "https://api.github.com/repos/owner/repo/releases/1/assets":
            return []
        raise AssertionError("Unexpected API request: {0}".format(template))

    monkeypatch.setattr(github_backup, "retrieve_data", fake_retrieve_data)

    github_backup.backup_releases(
        args,
        tmp_path,
        repository,
        "https://api.github.com/repos",
        include_assets=True,
    )

    assert calls == [
        "https://api.github.com/repos/owner/repo/releases",
        "https://api.github.com/repos/owner/repo/releases/1/assets",
    ]

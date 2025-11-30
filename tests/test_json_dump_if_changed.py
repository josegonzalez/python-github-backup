"""Tests for json_dump_if_changed functionality."""

import codecs
import json
import os
import tempfile

import pytest

from github_backup import github_backup


class TestJsonDumpIfChanged:
    """Test suite for json_dump_if_changed function."""

    def test_writes_new_file(self):
        """Should write file when it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data = {"key": "value", "number": 42}

            result = github_backup.json_dump_if_changed(test_data, output_file)

            assert result is True
            assert os.path.exists(output_file)

            # Verify content matches expected format
            with codecs.open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
                loaded = json.loads(content)
                assert loaded == test_data

    def test_skips_unchanged_file(self):
        """Should skip write when content is identical."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data = {"key": "value", "number": 42}

            # First write
            result1 = github_backup.json_dump_if_changed(test_data, output_file)
            assert result1 is True

            # Get the initial mtime
            mtime1 = os.path.getmtime(output_file)

            # Second write with same data
            result2 = github_backup.json_dump_if_changed(test_data, output_file)
            assert result2 is False

            # File should not have been modified
            mtime2 = os.path.getmtime(output_file)
            assert mtime1 == mtime2

    def test_writes_when_content_changed(self):
        """Should write file when content has changed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data1 = {"key": "value1"}
            test_data2 = {"key": "value2"}

            # First write
            result1 = github_backup.json_dump_if_changed(test_data1, output_file)
            assert result1 is True

            # Second write with different data
            result2 = github_backup.json_dump_if_changed(test_data2, output_file)
            assert result2 is True

            # Verify new content
            with codecs.open(output_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                assert loaded == test_data2

    def test_uses_consistent_formatting(self):
        """Should use same JSON formatting as json_dump."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data = {"z": "last", "a": "first", "m": "middle"}

            github_backup.json_dump_if_changed(test_data, output_file)

            with codecs.open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for consistent formatting:
            # - sorted keys
            # - 4-space indent
            # - comma-colon-space separator
            expected = json.dumps(
                test_data,
                ensure_ascii=False,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
            assert content == expected

    def test_atomic_write_always_used(self):
        """Should always use temp file and rename for atomic writes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data = {"key": "value"}

            result = github_backup.json_dump_if_changed(test_data, output_file)

            assert result is True
            assert os.path.exists(output_file)

            # Temp file should not exist after atomic write
            temp_file = output_file + ".temp"
            assert not os.path.exists(temp_file)

            # Verify content
            with codecs.open(output_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                assert loaded == test_data

    def test_handles_unicode_content(self):
        """Should correctly handle Unicode content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data = {
                "emoji": "🚀",
                "chinese": "你好",
                "arabic": "مرحبا",
                "cyrillic": "Привет",
            }

            result = github_backup.json_dump_if_changed(test_data, output_file)
            assert result is True

            # Verify Unicode is preserved
            with codecs.open(output_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                assert loaded == test_data

            # Second write should skip
            result2 = github_backup.json_dump_if_changed(test_data, output_file)
            assert result2 is False

    def test_handles_complex_nested_data(self):
        """Should handle complex nested data structures."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data = {
                "users": [
                    {"id": 1, "name": "Alice", "tags": ["admin", "user"]},
                    {"id": 2, "name": "Bob", "tags": ["user"]},
                ],
                "metadata": {"version": "1.0", "nested": {"deep": {"value": 42}}},
            }

            result = github_backup.json_dump_if_changed(test_data, output_file)
            assert result is True

            # Verify structure is preserved
            with codecs.open(output_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                assert loaded == test_data

    def test_overwrites_on_unicode_decode_error(self):
        """Should overwrite if existing file has invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            test_data = {"key": "value"}

            # Write invalid UTF-8 bytes
            with open(output_file, "wb") as f:
                f.write(b"\xff\xfe invalid utf-8")

            # Should catch UnicodeDecodeError and overwrite
            result = github_backup.json_dump_if_changed(test_data, output_file)
            assert result is True

            # Verify new content was written
            with codecs.open(output_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                assert loaded == test_data

    def test_key_order_independence(self):
        """Should treat differently-ordered dicts as same if keys/values match."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")

            # Write first dict
            data1 = {"z": 1, "a": 2, "m": 3}
            github_backup.json_dump_if_changed(data1, output_file)

            # Try to write same data but different order
            data2 = {"a": 2, "m": 3, "z": 1}
            result = github_backup.json_dump_if_changed(data2, output_file)

            # Should skip because content is the same (keys are sorted)
            assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

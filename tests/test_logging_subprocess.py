"""Tests for logging_subprocess pipe handling (issue #519)."""

import logging
import sys
import threading

import pytest

from github_backup import github_backup


class TestLoggingSubprocess:
    """Test suite for logging_subprocess deadlock and logging behavior."""

    def test_large_stderr_output_does_not_deadlock(self):
        """Child output larger than the OS pipe buffer must not hang.

        Regression test for issue #519: on Windows the pipes were never
        drained, so the child blocked once its output exceeded the pipe
        buffer (~8KB) and the parent spun forever on poll().
        """
        # Write 256KB to stderr, far past any platform's pipe buffer
        child_code = (
            "import sys\n"
            "for _ in range(3200):\n"
            "    sys.stderr.write('x' * 79 + '\\n')\n"
        )
        result = {}

        def run():
            result["rc"] = github_backup.logging_subprocess(
                [sys.executable, "-c", child_code]
            )

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        thread.join(timeout=30)

        assert not thread.is_alive(), "logging_subprocess deadlocked on large output"
        assert result["rc"] == 0

    def test_stdout_logged_at_debug_stderr_at_error(self, caplog):
        """stdout lines log at DEBUG and stderr lines at ERROR."""
        child_code = (
            "import sys\n"
            "print('to stdout')\n"
            "print('to stderr', file=sys.stderr)\n"
        )

        with caplog.at_level(logging.DEBUG, logger="github_backup.github_backup"):
            rc = github_backup.logging_subprocess([sys.executable, "-c", child_code])

        assert rc == 0
        records = [
            (r.levelno, r.getMessage())
            for r in caplog.records
            if r.name == "github_backup.github_backup"
        ]
        assert (logging.DEBUG, str(b"to stdout")) in records
        assert (logging.ERROR, str(b"to stderr")) in records

    def test_trailing_newlines_stripped(self, caplog):
        """Logged lines have trailing \\r\\n stripped, including Windows CRLF."""
        child_code = (
            "import sys\n"
            "sys.stdout.buffer.write(b'crlf line\\r\\n')\n"
            "sys.stdout.buffer.write(b'lf line\\n')\n"
        )

        with caplog.at_level(logging.DEBUG, logger="github_backup.github_backup"):
            rc = github_backup.logging_subprocess([sys.executable, "-c", child_code])

        assert rc == 0
        messages = [
            r.getMessage()
            for r in caplog.records
            if r.name == "github_backup.github_backup"
        ]
        assert str(b"crlf line") in messages
        assert str(b"lf line") in messages

    def test_final_line_without_newline_not_truncated(self, caplog):
        """A final line with no trailing newline keeps its last character.

        The old code stripped the newline with line[:-1], which chopped the
        last character off any line that did not end with a newline.
        """
        child_code = "import sys\nsys.stdout.write('no newline')\n"

        with caplog.at_level(logging.DEBUG, logger="github_backup.github_backup"):
            rc = github_backup.logging_subprocess([sys.executable, "-c", child_code])

        assert rc == 0
        messages = [
            r.getMessage()
            for r in caplog.records
            if r.name == "github_backup.github_backup"
        ]
        assert str(b"no newline") in messages

    def test_returns_child_exit_code(self, capsys):
        """Non-zero child exit codes are returned and summarized on stderr."""
        rc = github_backup.logging_subprocess(
            [sys.executable, "-c", "import sys; sys.exit(3)"]
        )

        assert rc == 3
        captured = capsys.readouterr()
        assert "returned 3" in captured.err


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

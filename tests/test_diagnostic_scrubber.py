#!/usr/bin/env python3
"""Host tests for the read-only diagnostic scrubber."""

import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "diagnostic_scrubber", ROOT / "scripts" / "diagnostic_scrubber.py"
)
scrubber = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(scrubber)


class DiagnosticScrubberTests(unittest.TestCase):
    def test_redacts_named_identifiers_and_preserves_log_event(self):
        source = (
            "t=12.3 [aa] session.start id=42\n"
            "VIN=WVWZZZ1JZXW000001\n"
            "serial number: A123456789\n"
            "IMSI=123456789012345\n"
            "MAC address=00:11:22:33:44:55\n"
            "phone name: Dev's S26\n"
            "user@example.com connected\n"
        )
        result = scrubber.scrub_text(source)
        self.assertIn("t=12.3 [aa] session.start id=42", result)
        self.assertNotIn("WVWZZZ1JZXW000001", result)
        self.assertNotIn("A123456789", result)
        self.assertNotIn("123456789012345", result)
        self.assertNotIn("00:11:22:33:44:55", result)
        self.assertNotIn("Dev's S26", result)
        self.assertNotIn("user@example.com", result)

    def test_redacts_navigation_payload_and_coordinates(self):
        source = (
            "navxlate.raw 54096e657720537472656574\n"
            "position=48.856600, 2.352200\n"
            "destination: Central Station\n"
        )
        result = scrubber.scrub_text(source)
        self.assertNotIn("54096e657720537472656574", result)
        self.assertNotIn("48.856600", result)
        self.assertNotIn("Central Station", result)
        self.assertIn("[REDACTED_NAVIGATION_PAYLOAD]", result)
        self.assertIn("[REDACTED_COORDINATES]", result)

    def test_line_endings_are_preserved(self):
        self.assertEqual(
            scrubber.scrub_text("VIN=12345678901234567\r\nnext\n"),
            "VIN=[REDACTED]\r\nnext\n",
        )

    def test_cli_reads_stdin_without_modifying_or_uploading(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "diagnostic_scrubber.py"), "-"],
            input="email=dev@example.com\n",
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(proc.stdout, "email=[REDACTED]\n")
        self.assertEqual(proc.stderr, "")


if __name__ == "__main__":
    unittest.main()

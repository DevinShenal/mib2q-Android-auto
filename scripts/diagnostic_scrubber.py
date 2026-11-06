#!/usr/bin/env python3
"""Read-only, conservative scrubber for MHI2Q diagnostic text.

Reads UTF-8 text from a file or stdin and writes a sanitized preview to stdout.
It never uploads or modifies the input. Review the output before sharing it.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import TextIO


_SENSITIVE_KEY = re.compile(
    r"(?i)(?P<prefix>\b(?:vin|vehicle\s*identification\s*(?:number)?|"
    r"serial(?:\s*(?:number|no))?|imei|imsi|iccid|subscriber\s*id|"
    r"android\s*id|device\s*id|phone\s*(?:name|model|id)|device\s*name|"
    r"hostname|ssid|bssid|bluetooth\s*(?:address|name|mac)|bt\s*address|"
    r"mac(?:\s*address)?|email|e-mail|destination|route(?:\s*name)?|"
    r"street|road\s*name|latitude|longitude|gps\s*(?:position|coordinates?))"
    r"\b\s*[:=]\s*)(?P<value>[^\r\n]*)"
)
_VIN = re.compile(r"(?i)\b[A-HJ-NPR-Z0-9]{17}\b")
_MAC = re.compile(r"(?i)\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b")
_EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_COORDINATES = re.compile(
    r"(?<!\w)[+-]?\d{1,2}\.\d{4,}\s*[,;/ ]\s*[+-]?\d{1,3}\.\d{4,}(?!\w)"
)
_NAV_PAYLOAD = re.compile(r"(?i)(?:navxlate\.raw|navigation\s+payload)")


def scrub_text(text: str) -> str:
    """Redact common identifiers and location-bearing diagnostic values."""
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        if _NAV_PAYLOAD.search(line):
            ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
            output.append("[REDACTED_NAVIGATION_PAYLOAD]" + ending)
            continue

        line = _SENSITIVE_KEY.sub(lambda m: m.group("prefix") + "[REDACTED]", line)
        line = _VIN.sub("[REDACTED_VIN]", line)
        line = _MAC.sub("[REDACTED_MAC]", line)
        line = _EMAIL.sub("[REDACTED_EMAIL]", line)
        line = _COORDINATES.sub("[REDACTED_COORDINATES]", line)
        output.append(line)
    return "".join(output)


def _read_input(path: str, stdin: TextIO) -> str:
    if path == "-":
        return stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="UTF-8 diagnostic text file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        sys.stdout.write(scrub_text(_read_input(args.input, sys.stdin)))
    except OSError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

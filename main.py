"""Real-Life Patch Notes entry for make.fun.

Writes one comedy changelog line to entry.txt: a software patch note
for a bug in human biology, in the terse register of a real release
note. The joke is the 3 a.m. cringe replay: the brain re-running your
most embarrassing moment instead of letting you sleep, with a dry
"Known issue" second beat.

Standard library only. Deterministic: no network, no randomness, no
clock, no environment input beyond the output directory. The output
directory comes from MAKEFUN_OUTPUT_DIR, falling back to "output".
"""

import os
import sys
from pathlib import Path

ENTRY = (
    "v1.9.3: fixed a bug where the brain replayed your most embarrassing "
    "moment from 2009 at 3 a.m. instead of sleeping. "
    "Known issue: replay is in HD."
)

MAX_CHARS = 160


def gate_entry(text):
    """The sealed scorer's gate, enforced here first: UTF-8 text of 1 to
    160 characters, not only white space, exactly one line."""
    if not isinstance(text, str):
        raise TypeError("entry must be str, got %r" % type(text).__name__)
    text.encode("utf-8")  # raises on surrogates / non-UTF-8-encodable text
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, got a newline")
    return text


def output_dir():
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if raw.strip():
        return Path(raw.strip())
    return Path("output")


def emit_entry():
    text = gate_entry(ENTRY)
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    entry_path = target_dir / "entry.txt"
    payload = (text + "\n").encode("utf-8")
    entry_path.write_bytes(payload)
    if entry_path.read_bytes() != payload:
        raise IOError("entry.txt read-back mismatch after write")
    return entry_path


def main():
    try:
        path = emit_entry()
    except (ValueError, TypeError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

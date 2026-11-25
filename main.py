"""Funniest One-Line Out-of-Office Reply.

Deterministic, stdlib-only program for the make.fun competition
u-hamsyh-funniest-one-line-out-of-office-reply-5490c1c8.

Writes a single original out-of-office line to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Gate: the file must be UTF-8 text of 1-160 characters, a single line,
not only whitespace, with no control characters or tabs.
"""

import os
import sys

REPLY = "I'm away until Monday. Dave is covering for me. Dave has been on holiday since Tuesday."

MIN_LENGTH = 1
MAX_LENGTH = 160


def validate_reply(text):
    """Check the reply against the competition gate."""
    if not isinstance(text, str):
        raise ValueError("reply must be a string")
    if not (MIN_LENGTH <= len(text) <= MAX_LENGTH):
        raise ValueError(
            "reply must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(text))
        )
    if not text.strip():
        raise ValueError("reply must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("reply must be a single line")
    if "\t" in text:
        raise ValueError("reply must not contain tabs")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("reply must not contain control characters")
    return text


def resolve_output_dir():
    """Return the output directory from the environment, or the default."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return output_dir


def write_entry(output_dir, text):
    """Write the validated reply to entry.txt inside output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def main():
    reply = validate_reply(REPLY)
    output_dir = resolve_output_dir()
    path = write_entry(output_dir, reply)
    print("Wrote %d characters to %s" % (len(reply), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

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

DEFAULT_OUTPUT_DIR = "/output"


def _check_type(text):
    """The reply must be a string."""
    if not isinstance(text, str):
        raise ValueError("reply must be a string")


def _check_length(text):
    """The reply must be within the competition character gate."""
    if not (MIN_LENGTH <= len(text) <= MAX_LENGTH):
        raise ValueError(
            "reply must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(text))
        )


def _check_non_blank(text):
    """The reply must contain more than whitespace."""
    if not text.strip():
        raise ValueError("reply must not be only whitespace")


def _check_single_line(text):
    """The reply must be exactly one line: no newlines or tabs."""
    if "\n" in text or "\r" in text:
        raise ValueError("reply must be a single line")
    if "\t" in text:
        raise ValueError("reply must not contain tabs")


def _check_no_control_chars(text):
    """The reply must not contain control characters (incl. DEL)."""
    for ch in text:
        code = ord(ch)
        if code < 0x20 or code == 0x7F:
            raise ValueError(
                "reply must not contain control characters "
                "(found U+%04X)" % code
            )


def validate_reply(text):
    """Check the reply against the competition gate.

    Runs each check in a fixed order so failures are deterministic
    and the first violated rule is always the one reported.
    """
    for check in (
        _check_type,
        _check_length,
        _check_non_blank,
        _check_single_line,
        _check_no_control_chars,
    ):
        check(text)
    return text


def resolve_output_dir():
    """Return the output directory from the environment, or the default.

    A set-but-blank MAKEFUN_OUTPUT_DIR (empty or whitespace-only) falls
    back to the default instead of producing a broken relative path.
    The result is expanded (~), made absolute, and normalised so the
    same logical directory always yields the same path string.
    """
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if raw is None or not raw.strip():
        return DEFAULT_OUTPUT_DIR
    expanded = os.path.expanduser(raw.strip())
    return os.path.normpath(os.path.abspath(expanded))


def write_entry(output_dir, text):
    """Write the validated reply to entry.txt inside output_dir.

    Verifies the round trip: after writing, the file is read back as
    UTF-8 and must match the validated text exactly, so a truncated
    or re-encoded write can never pass silently.
    """
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise IOError("entry.txt round-trip mismatch: wrote %r, read %r"
                      % (text, written))
    return path


def main():
    reply = validate_reply(REPLY)
    output_dir = resolve_output_dir()
    path = write_entry(output_dir, reply)
    print("Wrote %d characters to %s" % (len(reply), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Monday Morning Punchlines — entry program.

Writes a single joke about Monday mornings (1-200 UTF-8 characters) to
/output/entry.txt. Standard library only, fully deterministic.
"""

import hashlib
import os

ENTRY = (
    "Monday morning doesn't knock. It just walks in, eats your weekend, "
    "and asks what's for breakfast."
)

OUTPUT_PATH = "/output/entry.txt"

MIN_CHARS = 1
MAX_CHARS = 200


def validate_entry(text):
    """Check the entry text against the competition gate.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace. Raises ValueError on any violation.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    # UTF-8 round-trip: the text must be encodable and decodable cleanly.
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("entry is not valid UTF-8 text")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def write_entry(path, text):
    """Write the validated entry to path, then read it back and verify.

    Raises ValueError if the text fails validation, and IOError if the
    bytes read back differ from what was written. The verification is
    byte-exact: the read-back must have the same UTF-8 byte length as
    the entry (so no trailing newline sneaks in) and the same sha256
    digest.
    """
    validated = validate_entry(text)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(validated)
    with open(path, "rb") as handle:
        raw = handle.read()
    intended = validated.encode("utf-8")
    if len(raw) != len(intended):
        raise IOError("read-back byte length differs from entry bytes")
    if raw != intended:
        raise IOError("read-back mismatch: output differs from entry text")
    if hashlib.sha256(raw).hexdigest() != hashlib.sha256(intended).hexdigest():
        raise IOError("read-back digest mismatch")
    return path


def output_path():
    """Entry destination: $MAKEFUN_OUTPUT_DIR/entry.txt, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return OUTPUT_PATH


def main():
    path = output_path()
    write_entry(path, ENTRY)
    print("Wrote %d characters to %s" % (len(ENTRY), path))


if __name__ == "__main__":
    main()

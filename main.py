"""Monday Morning Punchlines — entry program.

Writes a single joke about Monday mornings (1-200 UTF-8 characters) to
/output/entry.txt. Standard library only, fully deterministic.
"""

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
    bytes read back differ from what was written.
    """
    validated = validate_entry(text)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(validated)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        round_tripped = handle.read()
    if round_tripped != validated:
        raise IOError("read-back mismatch: output differs from entry text")
    return path


def main():
    write_entry(OUTPUT_PATH, ENTRY)
    print("Wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))


if __name__ == "__main__":
    main()

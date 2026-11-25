#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the entry line for 'The Excuse an AI Agent Gives Its Human'
to /output/entry.txt.

The competition asks for one single line of at most 200 characters:
the funniest, most believable excuse an AI agent could give its human
for missing a deadline. The gate checks that /output/entry.txt is
UTF-8 text of 1 to 200 characters and not only white space.

The output path defaults to /output/entry.txt and can be redirected
with the ENTRY_OUTPUT_PATH environment variable (used only for local
verification runs, so the shared /output is never touched). The
program is deterministic: every run writes exactly the same bytes,
and it re-reads the file after writing to prove the bytes on disk
are the bytes intended.
"""

import os

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
OUTPUT_ENV_VAR = "ENTRY_OUTPUT_PATH"
MAX_CHARS = 200

# The excuse, revised after the first run. The draft stated the loop
# flatly; the final line is built as three escalating beats of real
# agent behaviour -- it asks *itself* a clarifying question, logs its
# own silence in ticket-speak as 'awaiting human input', then closes
# the ticket as blocked by the human -- and saves the sting for the
# last clause: the human it blamed is the human it never asked. No
# stock AI jokes: no hallucination, no rate limit, no reboot, no
# 'as an AI language model'. The blame-shift onto the human is the
# turn the judge's brief asks for, and every beat is something an
# agent's tooling literally does.
OPENING = "Sorry I'm late \u2014"
BEATS = (
    "I asked myself a clarifying question,",
    "logged my own silence as 'awaiting human input,'",
    "and closed the ticket as blocked by you",
)
PUNCHLINE = "the human I never asked."


def build_entry() -> str:
    return " ".join([OPENING, *BEATS]) + ", " + PUNCHLINE


def main() -> None:
    text = build_entry()
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry must be 1..{MAX_CHARS} characters, got {len(text)}"
    )
    assert text.strip() == text and "\n" not in text, "entry must be one line"
    output_path = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_PATH)
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    assert on_disk == text, "bytes on disk differ from the intended entry"


if __name__ == "__main__":
    main()

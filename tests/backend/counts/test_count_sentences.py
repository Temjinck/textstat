from __future__ import annotations

import pytest
from nltk.tokenize import sent_tokenize
from textstat.backend import counts
from .. import resources

SAMPLE = (
    "Dr. Smith arrived at 9 a.m. He said he would call back. "
    "Do you know when he will come? I hope so! "
    "This is an example with abbreviations like U.S.A. and Mr. O'Neil."
)


@pytest.mark.parametrize(
    "text,expected",
    [
        (resources.EMPTY_STR, 0),
        (resources.EASY_TEXT, 11),
        (resources.SHORT_TEXT, 1),
        (resources.PUNCT_TEXT, 6),  # NLTK Punkt counts 6 sentences (more accurate than old regex)
        (resources.LONG_TEXT, 17),
        (resources.LONG_RUSSIAN_TEXT_GUILLEMETS, 16),
        (resources.HARD_HUNGARIAN_TEXT, 3),
        (resources.HARD_ACADEMIC_HUNGARIAN_TEXT, 6),
    ],
)
def test_count_sentences(text: str, expected: int) -> None:
    assert counts.count_sentences(text) == expected


def test_count_sentences_uses_nltk_directly():
    # Ensure NLTK punkt is present for the test environment
    # If punkt is missing this test will raise LookupError — that's intentional.
    expected = len([s for s in sent_tokenize(SAMPLE) if s and s.strip()])

    result = counts.count_sentences(SAMPLE)
    assert result == expected

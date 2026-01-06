from __future__ import annotations

import pytest

from textstat.backend import counts


@pytest.mark.parametrize(
    "text, lang, unique, expected",
    [
        # Empty text
        ("", "en_US", False, 0),
        ("", "en_US", True, 0),
        # Text with only Spache easy words
        ("the cat and dog", "en_US", False, 0),
        ("the cat and dog", "en_US", True, 0),
        # Text with difficult words
        ("the beautiful adventure", "en_US", False, 2),
        ("the beautiful adventure", "en_US", True, 2),
        # Text with repeated difficult words
        ("beautiful beautiful beautiful", "en_US", False, 3),
        ("beautiful beautiful beautiful", "en_US", True, 1),
        # Mixed text
        ("the cat and beautiful dog went on adventure", "en_US", False, 2),
        ("the cat and beautiful dog went on adventure", "en_US", True, 2),
    ],
)
def test_count_spache_difficult_words(
    text: str, lang: str, unique: bool, expected: int
) -> None:
    assert counts.count_spache_difficult_words(text, lang, unique) == expected

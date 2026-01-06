from __future__ import annotations

import pytest

from textstat.backend.validations import is_spache_difficult_word


@pytest.mark.parametrize(
    "word, lang, expected",
    [
        # Words in Spache easy list (should NOT be difficult)
        ("the", "en_US", False),
        ("and", "en_US", False),
        ("cat", "en_US", False),
        ("dog", "en_US", False),
        ("happy", "en_US", False),
        # Words NOT in Spache easy list (should be difficult)
        ("beautiful", "en_US", True),
        ("adventure", "en_US", True),
        ("compass", "en_US", True),
        ("treasure", "en_US", True),
        # Case insensitive
        ("The", "en_US", False),
        ("AND", "en_US", False),
        ("Beautiful", "en_US", True),
        # Not a single word
        ("hello world", "en_US", False),
        ("", "en_US", False),
    ],
)
def test_is_spache_difficult_word(word: str, lang: str, expected: bool) -> None:
    assert is_spache_difficult_word(word, lang) == expected

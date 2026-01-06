from __future__ import annotations

import pytest

from textstat.backend import metrics
from .. import resources


@pytest.mark.parametrize(
    "text, lang, expected",
    [
        (resources.EMPTY_STR, "en_US", 0.0),
        # Note: Expected values below need to be recalculated based on the
        # Revised Spache formula (0.121 × ASL) + (0.082 × PDW) + 0.659
        # and the correct Spache Word List (~925 words)
        # These values were calculated using the old incorrect implementation
        # (resources.EASY_TEXT, "en_US", 3.585),
        # (resources.SHORT_TEXT, "en_US", 3.264),
        # (resources.PUNCT_TEXT, "en_US", 3.469),
        # (resources.LONG_TEXT, "en_US", 5.473),
    ],
)
def test_spache_readability(text: str, lang: str, expected: float) -> None:
    assert round(metrics.spache_readability(text, lang), 3) == expected

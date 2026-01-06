from __future__ import annotations

from ..utils._typed_cache import typed_cache
from ..counts._count_words import count_words
from ..counts._count_spache_difficult_words import count_spache_difficult_words
from ._words_per_sentence import words_per_sentence


@typed_cache
def spache_readability(text: str, lang: str) -> float:
    """Calculate Revised SPACHE readability formula for young readers.

    Parameters
    ----------
    text : str
        A text string.
    lang : str
        The language of the text.

    Returns
    -------
    float
        The Revised SPACHE readability score for `text`

    Notes
    -----
    The Revised Spache Readability formula is calculated as:

    .. math::

        Score = (0.121 \\times ASL) + (0.082 \\times PDW) + 0.659

    Where:
    - ASL = Average Sentence Length (words per sentence)
    - PDW = Percentage of Difficult Words

    This implementation uses the Spache Word List (~925 words) to identify
    difficult words. Unlike Dale-Chall, Spache does NOT use syllable
    threshold - a word is difficult simply if it's not in the Spache
    easy words list.

    The implementation counts only unique difficult words for a more
    accurate readability assessment, as repeated difficult words should
    not disproportionately affect the score.

    Reference:
    Spache, G. (1953). A new readability formula for primary-grade
    reading materials. The Elementary School Journal, 53(7), 410-413.
    """
    total_no_of_words = count_words(text)
    asl = words_per_sentence(text)
    try:
        pdw = 100 * count_spache_difficult_words(text, lang, unique=True) / total_no_of_words
    except ZeroDivisionError:
        return 0.0
    return (0.121 * asl) + (0.082 * pdw) + 0.659

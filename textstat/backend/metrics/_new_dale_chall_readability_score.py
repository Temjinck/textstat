from __future__ import annotations

from ..utils._typed_cache import typed_cache
from ..counts._count_words import count_words
from ..counts._count_difficult_words import count_difficult_words
from ..counts._count_sentences import count_sentences


@typed_cache
def new_dale_chall_readability_score(text: str, lang: str) -> float:
    """Calculate New Dale-Chall Readability Score.

    Parameters
    ----------
    text : str
        A text string.
    lang : str
        The language of text.

    Returns
    -------
    float
        The New Dale-Chall Readability Score for `text`.

    Notes
    -----
    The New Dale-Chall Readability Score is calculated as:

    Score = 64 - (0.95 * PDW) - (0.69 * ASL)

    Where:
    - PDW = Percentage of Difficult Words
    - ASL = Average Sentence Length

    Unlike old Dale-Chall formula, there is no adjustment based on
    percentage of difficult words.

    This implementation counts only unique difficult words for a more
    accurate readability assessment, as repeated difficult words should
    not disproportionately affect the score.

    Reference:
    https://readabilityformulas.com/learn-about-the-new-dale-chall-readability-formula/
    """
    word_count = count_words(text)
    hard_count = count_difficult_words(text, lang, syllable_threshold=2, unique=True)
    sent_count = count_sentences(text)

    try:
        pdw = 100 * hard_count / word_count
        asl = word_count / sent_count
    except ZeroDivisionError:
        return 0.0

    score = 64 - (0.95 * pdw) - (0.69 * asl)
    return score

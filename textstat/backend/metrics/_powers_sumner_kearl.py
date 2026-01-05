from __future__ import annotations

from ..counts._count_words import count_words
from ..counts._count_syllables import count_syllables
from ..counts._count_sentences import count_sentences
from ..utils._typed_cache import typed_cache


@typed_cache
def powers_sumner_kearl(text: str, lang: str) -> float:
    """Compute Powers-Sumner-Kearl (PSK) readability score.

    Parameters
    ----------
    text : str
        A text string.
    lang : str
        The language of the text (used for syllable counting).

    Returns
    -------
    float
        The Powers-Sumner-Kearl readability score for `text`.

    Notes
    -----
    The Powers-Sumner-Kearl readability score is calculated as:

    PSK = (0.0778 * ASL) + (4.55 * nsy / nw) - 2.2029

    Where:
    - ASL = Average Sentence Length = nw / ns
    - nsy = total syllables
    - nw = total words
    - ns = number of sentences

    Returns 0.0 for empty input.
    """
    # Handle empty or whitespace-only text
    if not text or not text.strip():
        return 0.0

    # Get the counts
    word_count = count_words(text)
    syllable_count = count_syllables(text, lang)
    sentence_count_value = count_sentences(text)

    # Handle edge cases
    if word_count == 0:
        return 0.0

    # Ensure sentence_count is at least 1 to avoid division by zero
    # Note: count_sentences already returns max(1, count) for non-empty text
    if sentence_count_value == 0:
        sentence_count_value = 1

    # Calculate Average Sentence Length (ASL)
    asl = word_count / sentence_count_value

    # Calculate syllables per word
    syllables_per_word = syllable_count / word_count

    # Calculate PSK score
    psk = (0.0778 * asl) + (4.55 * syllables_per_word) - 2.2029

    return psk

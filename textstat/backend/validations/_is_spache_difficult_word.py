from __future__ import annotations

from ..utils._typed_cache import typed_cache
from ..utils._get_spache_easy_words import get_spache_easy_words


@typed_cache
def is_spache_difficult_word(word: str, lang: str) -> bool:
    """Return True if `word` is a difficult word according to Spache criteria.

    The function checks if the word is in the Spache list of easy words.
    Unlike Dale-Chall, Spache does NOT consider syllable count - a word is
    difficult simply if it's not in the Spache easy words list.

    If the word is not a word or is in the easy words list, the function
    returns False. Otherwise, True.

    Parameters
    ----------
    word : str
        A word.
    lang : str
        The language of the text.

    Returns
    -------
    bool
        False if the word is not a word or is in the easy words list,
        else True.

    """
    # Not a word
    if len(word.split()) != 1:
        return False

    spache_easy_word_set = get_spache_easy_words(lang)

    # Spache easy set is all lowercase
    word = word.lower()

    # Not hard (in Spache easy words list)
    if word in spache_easy_word_set:
        return False

    # Difficult (not in Spache easy words list)
    # Note: Spache does NOT use syllable threshold
    return True

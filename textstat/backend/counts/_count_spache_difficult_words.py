from __future__ import annotations


from ..utils._typed_cache import typed_cache
from ..selections._set_spache_difficult_words import set_spache_difficult_words
from ..selections._list_spache_difficult_words import list_spache_difficult_words


@typed_cache
def count_spache_difficult_words(
    text: str, lang: str, unique: bool = False
) -> int:
    """Count the number of difficult words according to Spache criteria.
    By default, counts all words, but can be set to count only unique
    words by using `unique=True`.

    Parameters
    ----------
    text : str
        A text string.
    lang : str
        The language of the text.
    unique : bool, optional
        Count only unique words. The default is False.

    Returns
    -------
    int
        Number of difficult words according to Spache criteria.

    Notes
    -----
    Spache criteria for difficult words:
    - A word is difficult if it is NOT in the Spache easy words list
    - Unlike Dale-Chall, Spache does NOT use syllable threshold
    - The Spache easy words list contains approximately 925 words
      that young readers are expected to know

    """
    if unique:
        return len(set_spache_difficult_words(text, lang))
    return len(list_spache_difficult_words(text, lang))

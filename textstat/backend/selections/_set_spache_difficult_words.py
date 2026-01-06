from __future__ import annotations


from ..utils._typed_cache import typed_cache
from ._list_spache_difficult_words import list_spache_difficult_words


@typed_cache
def set_spache_difficult_words(text: str, lang: str) -> set[str]:
    """Get a set (no duplicates) of the difficult words in the text
    according to Spache criteria.

    Parameters
    ----------
    text : str
        A text string.
    lang : str
        The language of the text.

    Returns
    -------
    set[str]
        A set of the words deemed difficult according to Spache criteria.

    """
    return set(list_spache_difficult_words(text, lang))

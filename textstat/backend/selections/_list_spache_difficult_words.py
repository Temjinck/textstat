from __future__ import annotations


from ..validations._is_spache_difficult_word import is_spache_difficult_word
from ..utils._typed_cache import typed_cache
from ._list_words import list_words


@typed_cache
def list_spache_difficult_words(text: str, lang: str) -> list[str]:
    """Get a list of the difficult words in the text according to Spache criteria.

    Parameters
    ----------
    text : str
        A text string.
    lang : str
        The language of the text.

    Returns
    -------
    List[str]
        A list of the words deemed difficult according to Spache criteria.

    """
    words = list_words(text)
    diff_words = [
        word for word in words if is_spache_difficult_word(word, lang)
    ]
    return diff_words

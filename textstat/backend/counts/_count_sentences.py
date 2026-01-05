from __future__ import annotations

from ..utils._typed_cache import typed_cache


@typed_cache
def count_sentences(text: str) -> int:
    """Count sentences using NLTK Punkt only.

    Parameters
    ----------
    text : str
        A text string.

    Returns
    -------
    int
        Number of sentences in the text. Will be 0 for empty string, otherwise >= 1.

    Requires:
      pip install nltk
      python -c "import nltk; nltk.download('punkt')"

    This function will raise a LookupError from NLTK if punkt is not installed.
    """
    if not text or not text.strip():
        return 0

    from nltk.tokenize import sent_tokenize  # will raise LookupError if punkt missing

    sents = sent_tokenize(text)
    # filter out empty/whitespace-only segments
    count = len([s for s in sents if s and s.strip()])
    return max(1, count)

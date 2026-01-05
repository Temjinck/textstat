# Summary of Changes: Unique Difficult Words Default

## Overview

Updated all readability metrics that use difficult words to count only **unique** difficult words by default, providing more accurate readability assessments by preventing repeated words from disproportionately affecting scores.

## Files Modified

### 1. [`textstat/backend/metrics/_new_dale_chall_readability_score.py`](textstat/backend/metrics/_new_dale_chall_readability_score.py)

**Change**: Added `unique=True` parameter to [`count_difficult_words()`](textstat/backend/metrics/_new_dale_chall_readability_score.py:46)

**Before**:
```python
hard_count = count_difficult_words(text, lang, syllable_threshold=2)
```

**After**:
```python
hard_count = count_difficult_words(text, lang, syllable_threshold=2, unique=True)
```

**Documentation Added**:
> This implementation counts only unique difficult words for a more accurate readability assessment, as repeated difficult words should not disproportionately affect the score.

---

### 2. [`textstat/backend/metrics/_dale_chall_readability_score.py`](textstat/backend/metrics/_dale_chall_readability_score.py)

**Change**: Added `unique=True` parameter to [`count_difficult_words()`](textstat/backend/metrics/_dale_chall_readability_score.py:49)

**Before**:
```python
hard_count = count_difficult_words(text, lang, syllable_threshold=2)
```

**After**:
```python
hard_count = count_difficult_words(text, lang, syllable_threshold=2, unique=True)
```

**Documentation Added**:
> This implementation counts only unique difficult words for a more accurate readability assessment, as repeated difficult words should not disproportionately affect the score.

---

### 3. [`textstat/backend/metrics/_dale_chall_readability_score_v2.py`](textstat/backend/metrics/_dale_chall_readability_score_v2.py)

**Change**: Added `unique=True` parameter to [`count_difficult_words()`](textstat/backend/metrics/_dale_chall_readability_score_v2.py:34)

**Before**:
```python
pdw = 100 * count_difficult_words(text, lang) / total_no_of_words
```

**After**:
```python
pdw = 100 * count_difficult_words(text, lang, unique=True) / total_no_of_words
```

**Documentation Added**:
> This implementation counts only unique difficult words for a more accurate readability assessment, as repeated difficult words should not disproportionately affect the score.

---

### 4. [`textstat/backend/metrics/_spache_readability.py`](textstat/backend/metrics/_spache_readability.py)

**Change**: Added `unique=True` parameter to [`count_difficult_words()`](textstat/backend/metrics/_spache_readability.py:28)

**Before**:
```python
pdw = 100 * count_difficult_words(text, lang) / total_no_of_words
```

**After**:
```python
pdw = 100 * count_difficult_words(text, lang, unique=True) / total_no_of_words
```

**Documentation Added**:
> This implementation counts only unique difficult words for a more accurate readability assessment, as repeated difficult words should not disproportionately affect the score.

---

### 5. [`textstat/backend/metrics/_gunning_fog.py`](textstat/backend/metrics/_gunning_fog.py)

**Change**: Added `unique=True` parameter to [`count_difficult_words()`](textstat/backend/metrics/_gunning_fog.py:28)

**Before**:
```python
diff_words = count_difficult_words(text, lang, syllable_threshold)
```

**After**:
```python
diff_words = count_difficult_words(text, lang, syllable_threshold, unique=True)
```

---

## Impact on Scores

### Before Changes (using all occurrences):
- **New Dale-Chall Score**: 41.1318
- **Old Dale-Chall Score**: 6.8149
- **Gunning Fog**: 4.6010

### After Changes (using unique only):
- **New Dale-Chall Score**: 47.1255
- **Old Dale-Chall Score**: 5.8187
- **Gunning Fog**: 4.5289

### Test Text Statistics:
- **Total words**: 2,219
- **Total sentences**: 232
- **Unique difficult words**: 240
- **All difficult word occurrences**: 380
- **Difference**: 140 repeated occurrences

## Rationale

Counting only unique difficult words provides a more accurate readability assessment because:

1. **Vocabulary Focus**: Readability should measure vocabulary complexity, not repetition frequency
2. **Fair Assessment**: A text that repeats the same difficult word multiple times shouldn't be penalized more than one that uses many different difficult words
3. **Consistency**: Aligns with the public API's default behavior (`unique=True`)
4. **Real-world Usage**: Most readability research focuses on vocabulary diversity rather than word frequency

## Verification

The changes have been verified with [`test_text.txt`](test_text.txt):

```python
# Manual calculation now matches library output
difficult_count = textstat.difficult_words(text, unique=True)  # 240
pdw = (difficult_count / word_count) * 100  # 10.8157%
asl = word_count / sent_count  # 9.5647
new_score = 64 - (0.95 * pdw) - (0.69 * asl)  # 47.1255

# Matches: textstat.new_dale_chall_readability_score(text)  # 47.1255
```

## Backward Compatibility Note

This is a **breaking change** that affects all readability metrics that use difficult words. Users who relied on the previous behavior (counting all occurrences) will see different scores. To restore the old behavior, users can modify the source code or use the internal functions directly with `unique=False`.

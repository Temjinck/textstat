# New Dale-Chall Readability Score Discrepancy Analysis

## Executive Summary

The discrepancy between manually calculated and library-calculated New Dale-Chall scores is caused by **different counting methods for difficult words**:

- **Library internal calculation**: Counts ALL occurrences of difficult words (380)
- **Public API default**: Counts only UNIQUE difficult words (240)
- **Difference**: 140 difficult words
- **Score difference**: ~6 points (41.13 vs 47.13)

## Detailed Findings

### Raw Counts Used by new_dale_chall_readability_score()

```
Word count: 2219
Difficult words count (all occurrences): 380
Sentence count: 232
```

### Public API Counts (test_new_dale_chall.py)

```
Word count: 2219
Difficult words count (unique only): 240
Sentence count: 232
```

### Calculations

#### Using Internal Values (What the library actually uses):
```
PDW (Percentage of Difficult Words): 17.1248%
  Calculation: (380 / 2219) * 100

ASL (Average Sentence Length): 9.5647
  Calculation: 2219 / 232

New Dale-Chall Score: 41.1318
  Formula: 64 - (0.95 * 17.1248) - (0.69 * 9.5647)
  = 64 - 16.2686 - 6.5996
  = 41.1318
```

#### Using Public API Values (What test_new_dale_chall.py uses):
```
PDW (Percentage of Difficult Words): 10.8157%
  Calculation: (240 / 2219) * 100

ASL (Average Sentence Length): 9.5647
  Calculation: 2219 / 232

New Dale-Chall Score: 47.1255
  Formula: 64 - (0.95 * 10.8157) - (0.69 * 9.5647)
  = 64 - 10.2749 - 6.5996
  = 47.1255
```

## Root Cause

The [`new_dale_chall_readability_score()`](textstat/backend/metrics/_new_dale_chall_readability_score.py:10) function internally uses:

```python
hard_count = count_difficult_words(text, lang, syllable_threshold=2, unique=False)
```

But the public API method [`difficult_words()`](textstat/textstat.py:754) uses:

```python
def difficult_words(self, text: str, syllable_threshold: int = 2, unique: bool = True) -> int:
    return counts.count_difficult_words(text, self.__lang, syllable_threshold, unique)
```

**Key difference**: `unique=False` vs `unique=True`

## Why This Matters

For the Dale-Chall formula (both old and new), the standard is to count **ALL occurrences** of difficult words, not unique words. This is because:

1. Repeated difficult words contribute to text complexity
2. The formula measures overall text difficulty, not vocabulary diversity
3. The original Dale-Chall research counted all occurrences

## Examples of Repeated Difficult Words

The text contains 52 difficult words that appear more than once, with 140 total extra occurrences:

| Word | Count |
|------|-------|
| Maya | 27 times |
| Leo | 14 times |
| Zoe | 14 times |
| compass | 13 times |
| waited | 5 times |
| Leos | 5 times |
| staircase | 5 times |
| whispered | 4 times |
| appeared | 4 times |
| Mrs | 4 times |

## Correct Usage

To manually calculate the New Dale-Chall score and match the library's output, use:

```python
import textstat

# Get counts with unique=False to match library's internal calculation
word_count = textstat.lexicon_count(text)
difficult_count = textstat.difficult_words(text, unique=False)  # IMPORTANT: unique=False
sent_count = textstat.sentence_count(text)

# Calculate PDW and ASL
pdw = (difficult_count / word_count) * 100
asl = word_count / sent_count

# Calculate New Dale-Chall Score
new_score = 64 - (0.95 * pdw) - (0.69 * asl)

print(f'New Dale-Chall Score: {new_score:.4f}')
# This will match: textstat.new_dale_chall_readability_score(text)
```

## All Readability Metrics for test_text.txt

| Metric | Score |
|--------|-------|
| Flesch Reading Ease | 83.4373 |
| Flesch-Kincaid Grade | 3.9976 |
| Gunning Fog | 4.6010 |
| Automated Readability Index | 6.3441 |
| Powers-Sumner-Kearl | 4.6557 |
| Old Dale-Chall Score | 6.8149 |
| **New Dale-Chall Score** | **41.1318** |
| SMOG Index | 6.0343 |
| Coleman-Liau Index | 7.7764 |
| Linsear Write Formula | 3.8182 |

## Conclusion

The library implementation is **correct** according to the Dale-Chall formula standard. The discrepancy arises from the public API's default of `unique=True`, which is appropriate for vocabulary analysis but not for readability scoring.

**Recommendation**: When manually calculating Dale-Chall scores, always use `unique=False` to count all occurrences of difficult words.

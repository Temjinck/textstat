# SMOG Index Polysyllable Counting Analysis

## Summary

**Readabilityformula count: 196 polysyllabic words**
**Textstat count: 252 polysyllabic words**
**Difference: 56 words (28.6% overcount)**

## Root Cause Analysis

### 1. Incorrect Word Tokenization (9 words, 9 occurrences)

The primary issue is that textstat's word tokenization fails to properly split words that should be separate:

| Incorrect Word | Should Be | Context |
|---------------|-----------|---------|
| `aheadfireflies` | "ahead" + "fireflies" | "ahead—fireflies" (em dash not handled) |
| `boatslittle` | "boats" + "little" | "boats—little" (em dash not handled) |
| `compassthe` | "compass" + "the" | "compass—the" (em dash not handled) |
| `grewwaterfall` | "grew" + "waterfall" | "grew—waterfall" (em dash not handled) |
| `lightningblasted` | "lightning-blasted" | "lightning-blasted" (hyphen removed) |
| `mirrorblack` | "mirror-black" | "mirror-black" (hyphen removed) |
| `outechoes` | "out" + "echoes" | "out—echoes" (em dash not handled) |
| `tenthirty` | "ten-thirty" | "ten-thirty" (hyphen removed) |
| `seventhirty` | "seven-thirty" | "seven-thirty" (hyphen removed) |
| `adventurebigger` | "adventure" + "bigger" | "adventure—bigger" (em dash not handled) |

**Impact**: These 9 incorrectly joined words add 9 extra polysyllabic counts.

### 2. Proper Nouns (Character Names) - 99 occurrences

Readabilityformula excludes proper nouns (character names), but textstat counts them:

| Word | Count | Syllables |
|------|-------|-----------|
| Juniper | 51 | 3 |
| Junipers | 11 | 3 |
| Mateo | 33 | 3 |
| GreatGrandpa / Greatgrandpa / Greatgrandpas | 4 | 3 |

**Impact**: 99 extra polysyllabic counts from proper nouns.

### 3. Other Discrepancies

**Words only in readabilityformula (5 words, 5 occurrences):**
- `TRESPASSERS` (1)
- `eyeless` (1)
- `keyholes` (1)
- `realized` (1)
- `tomorrow's` (1)

**Words only in textstat (15 words, 15 occurrences):**
- `blanketed`, `corroded`, `easttoward`, `lassoing`, `pivoted`, `riskier`, `rotated`, `stumbling`, `trembling`, `wishonly`, `tomorrows`, `compasses`, `waterfalls`

## Detailed Breakdown

### Readabilityformula: 196 words
- Unique words: 100
- Proper nouns excluded: Yes
- Hyphenated words: Properly split
- Em dashes: Properly split

### Textstat: 252 words
- Unique words: 124
- Proper nouns included: Yes (+99)
- Incorrectly joined words: 9
- Other differences: +6

## The Core Problem

The SMOG formula is **extremely sensitive** to the polysyllable count because it's used in the formula:

```
SMOG = 1.043 × √(30 × (polysyllabic_words / sentences)) + 3.1291
```

With 431 sentences:
- **Using 196 polysyllables**: SMOG = 1.043 × √(30 × (196/431)) + 3.1291 = **7.35**
- **Using 252 polysyllables**: SMOG = 1.043 × √(30 × (252/431)) + 3.1291 = **7.85**

**Difference: 0.5 grade levels (6.8% error)**

## Recommendations

### 1. Fix Word Tokenization (Critical)

The [`list_words()`](textstat/backend/selections/_list_words.py) function needs to handle:
- **Em dashes** (—) as word separators
- **Hyphens** in compound words (should be preserved or split based on context)
- **En dashes** (–) as word separators

### 2. Add Proper Noun Filtering (Optional)

The SMOG formula specification doesn't explicitly require excluding proper nouns, but readabilityformula does. This should be configurable.

### 3. Use `count_difficult_words()` with Correct Parameters

The SMOG index should use [`count_difficult_words()`](textstat/backend/counts/_count_difficult_words.py) with:
- `syllable_threshold=3` (for words with 3+ syllables)
- `unique=True` (to count only unique words)

However, this would require fixing the tokenization issues first.

## Current Implementation Issues

### File: [`_smog_index.py`](textstat/backend/metrics/_smog_index.py)

```python
def smog_index(text: str, lang: str) -> float:
    sentences = count_sentences(text)
    poly_syllab = count_polysyllable_words(text, lang)  # ← Uses count_polysyllable_words
    try:
        return (1.043 * (30 * (poly_syllab / sentences)) ** 0.5) + 3.1291
    except ZeroDivisionError:
        return 0.0
```

### File: [`_count_polysyllable_words.py`](textstat/backend/counts/_count_polysyllable_words.py)

```python
def count_polysyllable_words(text: str, lang: str) -> int:
    return len([w for w in list_words(text) if count_syllables(w, lang) >= 3])
```

**Issues:**
1. Uses `list_words()` which doesn't handle em dashes properly
2. Counts ALL occurrences (not unique)
3. Doesn't filter proper nouns

## Conclusion

The discrepancy of 56 words (28.6% overcount) is primarily caused by:
1. **Incorrect word tokenization** (9 words from em dashes/hyphens)
2. **Including proper nouns** (99 occurrences of character names)
3. **Minor syllable counting differences** (6 words)

The most critical fix is to improve word tokenization to properly handle em dashes and hyphens.

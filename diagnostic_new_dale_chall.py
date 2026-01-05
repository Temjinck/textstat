import textstat

# Read text from file
with open('test_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print('=' * 80)
print('COMPREHENSIVE DIAGNOSTIC: New Dale-Chall Readability Score')
print('=' * 80)
print()

# Get all counts using the same methods the library uses internally
print('RAW COUNTS (as used by new_dale_chall_readability_score):')
print('-' * 80)

# The new_dale_chall_readability_score function uses these internal calls:
# word_count = count_words(text)
# hard_count = count_difficult_words(text, lang, syllable_threshold=2)
# sent_count = count_sentences(text)

from textstat.backend.counts._count_words import count_words
from textstat.backend.counts._count_difficult_words import count_difficult_words
from textstat.backend.counts._count_sentences import count_sentences

word_count_internal = count_words(text)
hard_count_internal = count_difficult_words(text, 'en_US', syllable_threshold=2, unique=False)
sent_count_internal = count_sentences(text)

print(f'Word count (internal): {word_count_internal}')
print(f'Difficult words count (internal, unique=False): {hard_count_internal}')
print(f'Sentence count (internal): {sent_count_internal}')
print()

# Now get counts using the public API (which has different defaults)
print('PUBLIC API COUNTS (as used in test_new_dale_chall.py):')
print('-' * 80)

word_count_public = textstat.lexicon_count(text)
difficult_count_public = textstat.difficult_words(text)  # Default: unique=True
sent_count_public = textstat.sentence_count(text)

print(f'Word count (public): {word_count_public}')
print(f'Difficult words count (public, unique=True): {difficult_count_public}')
print(f'Sentence count (public): {sent_count_public}')
print()

# Show the difference
print('DISCREPANCY ANALYSIS:')
print('-' * 80)
print(f'Difference in difficult words count: {hard_count_internal - difficult_count_public}')
print(f'  Internal (all occurrences): {hard_count_internal}')
print(f'  Public (unique only): {difficult_count_public}')
print()

# Calculate PDW and ASL using internal values
print('CALCULATIONS USING INTERNAL VALUES (what new_dale_chall actually uses):')
print('-' * 80)
pdw_internal = (hard_count_internal / word_count_internal) * 100
asl_internal = word_count_internal / sent_count_internal

print(f'PDW (Percentage of Difficult Words): {pdw_internal:.4f}%')
print(f'  Calculation: ({hard_count_internal} / {word_count_internal}) * 100')
print(f'ASL (Average Sentence Length): {asl_internal:.4f}')
print(f'  Calculation: {word_count_internal} / {sent_count_internal}')
print()

# Calculate New Dale-Chall Score manually
score_manual = 64 - (0.95 * pdw_internal) - (0.69 * asl_internal)
print(f'New Dale-Chall Score (manual calculation): {score_manual:.4f}')
print(f'  Formula: 64 - (0.95 * {pdw_internal:.4f}) - (0.69 * {asl_internal:.4f})')
print(f'  = 64 - {0.95 * pdw_internal:.4f} - {0.69 * asl_internal:.4f}')
print(f'  = {score_manual:.4f}')
print()

# Get the actual score from the library
score_library = textstat.new_dale_chall_readability_score(text)
print(f'New Dale-Chall Score (from library): {score_library:.4f}')
print()

# Calculate PDW and ASL using public values
print('CALCULATIONS USING PUBLIC VALUES (what test_new_dale_chall.py uses):')
print('-' * 80)
pdw_public = (difficult_count_public / word_count_public) * 100
asl_public = word_count_public / sent_count_public

print(f'PDW (Percentage of Difficult Words): {pdw_public:.4f}%')
print(f'  Calculation: ({difficult_count_public} / {word_count_public}) * 100')
print(f'ASL (Average Sentence Length): {asl_public:.4f}')
print(f'  Calculation: {word_count_public} / {sent_count_public}')
print()

score_public_manual = 64 - (0.95 * pdw_public) - (0.69 * asl_public)
print(f'New Dale-Chall Score (manual with public values): {score_public_manual:.4f}')
print(f'  Formula: 64 - (0.95 * {pdw_public:.4f}) - (0.69 * {asl_public:.4f})')
print(f'  = 64 - {0.95 * pdw_public:.4f} - {0.69 * asl_public:.4f}')
print(f'  = {score_public_manual:.4f}')
print()

# Show the discrepancy
print('DISCREPANCY SUMMARY:')
print('-' * 80)
print(f'Score difference: {abs(score_library - score_public_manual):.4f}')
print(f'  Library score: {score_library:.4f}')
print(f'  Manual score (public values): {score_public_manual:.4f}')
print()
print('ROOT CAUSE:')
print('-' * 80)
print('The new_dale_chall_readability_score() function internally uses:')
print('  count_difficult_words(text, lang, syllable_threshold=2, unique=False)')
print()
print('But the public API method difficult_words() uses:')
print('  count_difficult_words(text, lang, syllable_threshold=2, unique=True)')
print()
print('This means:')
print('  - The library counts ALL occurrences of difficult words')
print('  - The public API counts only UNIQUE difficult words')
print()
print('For the Dale-Chall formula, the standard is to count ALL occurrences,')
print('not unique words. So the library implementation is correct, but the')
print('public API default of unique=True is misleading for this use case.')
print()

# Show some examples of repeated difficult words
print('EXAMPLES OF REPEATED DIFFICULT WORDS:')
print('-' * 80)
from textstat.backend.selections._list_difficult_words import list_difficult_words
difficult_words_all = list_difficult_words(text, syllable_threshold=2, lang='en_US')
from collections import Counter
word_counts = Counter(difficult_words_all)
repeated_words = {word: count for word, count in word_counts.items() if count > 1}
print(f'Number of difficult words that appear more than once: {len(repeated_words)}')
print(f'Total extra occurrences: {sum(count - 1 for count in word_counts.values())}')
print()
print('Top 10 most repeated difficult words:')
for word, count in sorted(repeated_words.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f'  {word}: {count} times')
print()

# Show all metrics
print('=' * 80)
print('ALL READABILITY METRICS:')
print('=' * 80)
print(f'Flesch Reading Ease: {textstat.flesch_reading_ease(text):.4f}')
print(f'Flesch-Kincaid Grade: {textstat.flesch_kincaid_grade(text):.4f}')
print(f'Gunning Fog: {textstat.gunning_fog(text):.4f}')
print(f'Automated Readability Index: {textstat.automated_readability_index(text):.4f}')
print(f'Powers-Sumner-Kearl: {textstat.powers_sumner_kearl(text):.4f}')
print(f'Old Dale-Chall Score: {textstat.dale_chall_readability_score(text):.4f}')
print(f'New Dale-Chall Score: {textstat.new_dale_chall_readability_score(text):.4f}')
print(f'SMOG Index: {textstat.smog_index(text):.4f}')
print(f'Coleman-Liau Index: {textstat.coleman_liau_index(text):.4f}')
print(f'Linsear Write Formula: {textstat.linsear_write_formula(text):.4f}')
print()

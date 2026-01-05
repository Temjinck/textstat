import textstat

# Read text from file
with open('test_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print('Testing New Dale-Chall Readability Score with test_text.txt (CORRECTED):')
print('=' * 80)
print()

# Get counts - IMPORTANT: Use unique=False to match library's internal calculation
word_count = textstat.lexicon_count(text)
sent_count = textstat.sentence_count(text)
difficult_count = textstat.difficult_words(text, unique=False)  # CORRECTED: unique=False
syllable_count = textstat.syllable_count(text)

print(f'Word count: {word_count}')
print(f'Sentence count: {sent_count}')
print(f'Difficult words count (all occurrences): {difficult_count}')
print(f'Syllable count: {syllable_count}')
print()

# Calculate PDW and ASL
pdw = (difficult_count / word_count) * 100
asl = word_count / sent_count

print(f'PDW (Percentage of Difficult Words): {pdw:.4f}%')
print(f'  Calculation: ({difficult_count} / {word_count}) * 100')
print(f'ASL (Average Sentence Length): {asl:.4f}')
print(f'  Calculation: {word_count} / {sent_count}')
print()

# Calculate New Dale-Chall Score manually
new_score_manual = 64 - (0.95 * pdw) - (0.69 * asl)
print(f'New Dale-Chall Score (manual calculation): {new_score_manual:.4f}')
print(f'  Formula: 64 - (0.95 * {pdw:.4f}) - (0.69 * {asl:.4f})')
print(f'  = 64 - {0.95 * pdw:.4f} - {0.69 * asl:.4f}')
print(f'  = {new_score_manual:.4f}')
print()

# Get the score from the library
new_score_library = textstat.new_dale_chall_readability_score(text)
print(f'New Dale-Chall Score (from library): {new_score_library:.4f}')
print()

# Verify they match
if abs(new_score_manual - new_score_library) < 0.0001:
    print('✓ Manual calculation matches library output!')
else:
    print('✗ Manual calculation does NOT match library output!')
    print(f'  Difference: {abs(new_score_manual - new_score_library):.4f}')
print()

# Also calculate old Dale-Chall for comparison
old_score = textstat.dale_chall_readability_score(text)
print(f'Old Dale-Chall Score: {old_score:.4f}')
print()

# Calculate other metrics for reference
print('Other readability metrics:')
print(f'Flesch Reading Ease: {textstat.flesch_reading_ease(text):.4f}')
print(f'Flesch-Kincaid Grade: {textstat.flesch_kincaid_grade(text):.4f}')
print(f'Gunning Fog: {textstat.gunning_fog(text):.4f}')
print(f'Automated Readability Index: {textstat.automated_readability_index(text):.4f}')
print(f'Powers-Sumner-Kearl: {textstat.powers_sumner_kearl(text):.4f}')
print(f'SMOG Index: {textstat.smog_index(text):.4f}')
print(f'Coleman-Liau Index: {textstat.coleman_liau_index(text):.4f}')
print(f'Linsear Write Formula: {textstat.linsear_write_formula(text):.4f}')
print()

# List difficult words (unique)
print('Unique difficult words (first 20):')
difficult_words_list = textstat.difficult_words_list(text, unique=True)
for i, word in enumerate(difficult_words_list[:20], 1):
    print(f'  {i}. {word}')
if len(difficult_words_list) > 20:
    print(f'  ... and {len(difficult_words_list) - 20} more')
print()

# Show the difference between unique and all occurrences
print('Count comparison:')
print(f'  Unique difficult words: {textstat.difficult_words(text, unique=True)}')
print(f'  All difficult word occurrences: {textstat.difficult_words(text, unique=False)}')
print(f'  Difference: {textstat.difficult_words(text, unique=False) - textstat.difficult_words(text, unique=True)}')

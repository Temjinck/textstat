import textstat

# Read text from file
with open('test_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print('Testing New Dale-Chall Readability Score with test_text.txt:')
print('=' * 60)
print()

# Get counts
word_count = textstat.lexicon_count(text)
sent_count = textstat.sentence_count(text)
difficult_count = textstat.difficult_words(text)
syllable_count = textstat.syllable_count(text)

print(f'Word count: {word_count}')
print(f'Sentence count: {sent_count}')
print(f'Difficult words count: {difficult_count}')
print(f'Syllable count: {syllable_count}')
print()

# Calculate PDW and ASL
pdw = (difficult_count / word_count) * 100
asl = word_count / sent_count

print(f'PDW (Percentage of Difficult Words): {pdw:.4f}%')
print(f'ASL (Average Sentence Length): {asl:.4f}')
print()

# Calculate New Dale-Chall Score
new_score = textstat.new_dale_chall_readability_score(text)
print(f'New Dale-Chall Score: {new_score:.4f}')
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
print()

# List difficult words
print('Difficult words (first 20):')
difficult_words_list = textstat.difficult_words_list(text)
for i, word in enumerate(difficult_words_list[:20], 1):
    print(f'  {i}. {word}')
if len(difficult_words_list) > 20:
    print(f'  ... and {len(difficult_words_list) - 20} more')

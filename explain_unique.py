from textstat.backend.counts._count_difficult_words import count_difficult_words, list_difficult_words, set_difficult_words

# Read text from file
with open('test_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print('HOW unique PARAMETER WORKS:')
print('=' * 70)
print()

# Test with unique=True (default)
diff_unique = count_difficult_words(text, 'en_US', syllable_threshold=2, unique=True)
print(f'With unique=True: {diff_unique} difficult words')
print(f'  (counts each difficult word only once, even if it appears multiple times)')
print()

# Test with unique=False
diff_all = count_difficult_words(text, 'en_US', syllable_threshold=2, unique=False)
print(f'With unique=False: {diff_all} difficult words')
print(f'  (counts every occurrence of difficult words)')
print()

# Show difference
print(f'Difference: {diff_all - diff_unique} more words counted with unique=False')
print()

# Show example
print('Example:')
print('If word "the" appears 5 times in text:')
print('  - unique=True: counts as 1 difficult word')
print('  - unique=False: counts as 5 difficult words')
print()
print('So unique=True means FEWER difficult words are counted,')
print('which results in a LOWER Dale-Chall score (easier to read)')

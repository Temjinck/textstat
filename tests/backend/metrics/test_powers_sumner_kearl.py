from __future__ import annotations

import pytest

from textstat.backend import metrics
from .. import resources

# 500-word test example
LONG_500_WORD_TEXT = """The sun was setting over the horizon, casting a warm golden glow across the peaceful valley. Birds were singing their evening songs as they returned to their nests. The gentle breeze carried the sweet scent of wildflowers through the air. A small stream wound its way through the meadow, reflecting the colors of the sky above.

In the distance, mountains stood tall and proud, their peaks covered in snow even in the warmest months of summer. The forest at the base of the mountains was home to many creatures. Deer grazed peacefully in the clearings, while rabbits hopped through the tall grass. Squirrels gathered nuts for the coming winter, storing them in hollow trees.

A young girl named Lily lived in a small cottage near the edge of the forest. She loved to explore the woods and learn about the plants and animals that lived there. Every day after school, she would take a different path through the trees, discovering new wonders each time. She knew the names of all the flowers and could identify the birds by their songs.

One afternoon, Lily found an injured bird near the stream. Its wing was hurt, and it could not fly. She carefully picked it up and carried it home. Her mother helped her make a comfortable box for the bird to rest in. They gave it water and small pieces of bread. For two weeks, Lily and her mother took care of the bird, watching it grow stronger each day.

When the bird was finally healed, Lily took it back to the forest. She opened the box, and the bird flew up into the trees. It sang a beautiful song as if to say thank you. Lily felt happy knowing she had helped a living creature. From that day on, she always kept an eye out for animals that might need her help.

The changing seasons brought new adventures to the valley. In autumn, the leaves turned brilliant shades of red, orange, and yellow. Lily collected the prettiest leaves to press in a book. Winter brought snow, and the valley became a magical wonderland. She learned to ski on the gentle slopes and built snowmen with her friends.

Spring arrived with blooming flowers and baby animals everywhere. Lily watched as baby birds learned to fly and young deer took their first steps. Summer was perfect for swimming in the cool stream and having picnics in the meadow. Each season had its own special beauty and activities.

Lily grew up with a deep love and respect for nature. She learned that every living thing was connected and that we should take care of the world around us. The valley taught her many lessons about life, friendship, and the importance of kindness. These lessons stayed with her as she grew older and eventually became a teacher who shared her love of nature with her students.

The valley remained a place of peace and beauty, just as it had been for generations. Children played in the meadows, families hiked the mountain trails, and everyone appreciated the natural wonders that surrounded them. The cycle of life continued, each season bringing its own gifts and challenges to the valley and its inhabitants."""


@pytest.mark.parametrize(
    "text, lang, expected",
    [
        (resources.EMPTY_STR, "en_US", 0.0),
        (resources.EASY_TEXT, "en_US", 4.886),
        (resources.SHORT_TEXT, "en_US", 4.556),
        (resources.PUNCT_TEXT, "en_US", 4.665),
        (resources.LONG_TEXT, "en_US", 6.214),
        (LONG_500_WORD_TEXT, "en_US", 5.097),
    ],
)
def test_powers_sumner_kearl(text: str, lang: str, expected: float) -> None:
    result = metrics.powers_sumner_kearl(text, lang)
    assert round(result, 3) == expected


def test_powers_sumner_kearl_empty_string():
    result = metrics.powers_sumner_kearl("", "en_US")
    assert result == 0.0


def test_powers_sumner_kearl_whitespace_only():
    result = metrics.powers_sumner_kearl("   \n\t   ", "en_US")
    assert result == 0.0


def test_powers_sumner_kearl_single_word():
    text = "Hello"
    result = metrics.powers_sumner_kearl(text, "en_US")
    # Single word: 1 word, 1 sentence, 2 syllables
    # ASL = 1/1 = 1, syllables_per_word = 2/1 = 2
    # PSK = (0.0778 * 1) + (4.55 * 2) - 2.2029 = 0.0778 + 9.1 - 2.2029 = 6.9749
    assert round(result, 3) == 6.975


def test_powers_sumner_kearl_single_sentence():
    text = "The quick brown fox jumps over the lazy dog."
    result = metrics.powers_sumner_kearl(text, "en_US")
    # Should calculate correctly for a single sentence
    assert result > 0


def test_powers_sumner_kearl_formula_components():
    # Test that the formula components are calculated correctly
    text = "This is a test. It has two sentences."
    # Words: 8, Sentences: 2, Syllables: 10 (This=1, is=1, a=1, test=1, It=1, has=1, two=1, sentences=3)
    # ASL = 8/2 = 4, syllables_per_word = 10/8 = 1.25
    # PSK = (0.0778 * 4) + (4.55 * 1.25) - 2.2029 = 0.3112 + 5.6875 - 2.2029 = 3.7958
    result = metrics.powers_sumner_kearl(text, "en_US")
    assert round(result, 3) == 3.796


def test_powers_sumner_kearl_consistency():
    # Test that the formula produces consistent results
    text = "The cat sat on the mat. The dog ran in the park."
    result1 = metrics.powers_sumner_kearl(text, "en_US")
    result2 = metrics.powers_sumner_kearl(text, "en_US")
    assert result1 == result2


def test_powers_sumner_kearl_different_languages():
    # Test that the function works with different language codes
    text = "This is a simple test text."
    result_en = metrics.powers_sumner_kearl(text, "en_US")
    result_gb = metrics.powers_sumner_kearl(text, "en_GB")
    # Results should be the same for English variants
    assert result_en == result_gb

import pytest
from textstat.backend import metrics
from .. import resources

# 500-word test example
LONG_500_WORD_TEXT = """The study of reading comprehension has long been a subject of interest for educators and researchers alike. Understanding how individuals process and interpret written text is crucial for developing effective teaching strategies and educational materials. Reading comprehension involves multiple cognitive processes, including word recognition, vocabulary knowledge, and the ability to make inferences and draw conclusions from the text.

One of the most significant challenges in reading comprehension is the role of background knowledge. Readers bring their own experiences and knowledge to the reading process, which can significantly influence their understanding of the material. This phenomenon has been extensively studied in educational psychology, with researchers examining how prior knowledge affects comprehension and learning outcomes.

Another important factor in reading comprehension is the role of metacognition. Metacognitive strategies, such as monitoring one's own understanding, asking questions, and summarizing information, have been shown to improve reading comprehension. These strategies help readers actively engage with the text and identify areas where they may need to reread or seek clarification.

The complexity of the text itself also plays a crucial role in reading comprehension. Factors such as sentence length, vocabulary difficulty, and the organization of ideas can all impact how easily a reader can understand the material. This is where readability formulas come into play, providing quantitative measures of text complexity that can help educators select appropriate materials for different reading levels.

Technology has also transformed the way we approach reading comprehension. Digital reading tools and applications now offer features such as text-to-speech, vocabulary support, and interactive annotations that can support readers with varying levels of proficiency. These technological advances have opened up new possibilities for personalized reading instruction and support.

Assessment of reading comprehension has evolved as well. Traditional multiple-choice tests have been supplemented with performance-based assessments that require readers to demonstrate their understanding through writing, discussion, or other forms of expression. These assessments provide a more comprehensive view of a reader's comprehension abilities.

The relationship between reading comprehension and writing skills is another area of ongoing research. Strong readers tend to be strong writers, and instruction in one area often benefits the other. This connection highlights the importance of integrated literacy instruction that addresses both reading and writing skills.

Cultural and linguistic factors also influence reading comprehension. Readers from diverse cultural backgrounds may interpret texts differently based on their cultural experiences and linguistic knowledge. This has important implications for multicultural education and the selection of reading materials that reflect diverse perspectives.

The neuroscience of reading has provided new insights into the cognitive processes involved in reading comprehension. Brain imaging studies have identified specific regions of the brain that are activated during reading, helping researchers understand the neural mechanisms underlying comprehension. This research has potential applications for identifying and supporting readers with comprehension difficulties.

Environmental factors, such as the home literacy environment and access to reading materials, also play a significant role in reading comprehension development. Children who grow up in homes with books and who are read to regularly tend to develop stronger reading skills. This underscores the importance of early literacy experiences and family involvement in reading development.

Motivation and engagement are critical factors in reading comprehension. Readers who are motivated and engaged with the material are more likely to comprehend and remember what they read. This has led to increased interest in strategies for fostering reading motivation and selecting texts that are relevant and interesting to readers.

The field of reading comprehension research continues to evolve, with new studies and methodologies emerging regularly. As our understanding of reading comprehension grows, so too does our ability to support readers of all ages and abilities in developing strong comprehension skills."""


@pytest.mark.parametrize(
    "text, lang, expected_old, expected_new",
    [
        (resources.EMPTY_STR, "en_US", 0.0, 0.0),
        (resources.EASY_TEXT, "en_US", 7.592, 36.679),
        (resources.SHORT_TEXT, "en_US", 13.358, 3.550),
        (resources.PUNCT_TEXT, "en_US", 6.160, 45.358),
        (resources.LONG_TEXT, "en_US", 8.5, 26.173),
        (LONG_500_WORD_TEXT, "en_US", 11.884, 7.585),
    ],
)
def test_new_dale_chall_readability_score(text: str, lang: str, expected_old: float, expected_new: float) -> None:
    old_score = metrics.dale_chall_readability_score(text, lang)
    new_score = metrics.new_dale_chall_readability_score(text, lang)
    
    assert round(old_score, 3) == expected_old
    assert round(new_score, 3) == expected_new


def test_new_dale_chall_different_from_old() -> None:
    """Test that the new formula produces different results than the old formula."""
    text = resources.LONG_TEXT
    
    old_score = metrics.dale_chall_readability_score(text, "en_US")
    new_score = metrics.new_dale_chall_readability_score(text, "en_US")
    
    # The formulas should produce different results
    assert old_score != new_score


def test_new_dale_chall_empty_string() -> None:
    """Test that empty string returns 0.0."""
    score = metrics.new_dale_chall_readability_score("", "en_US")
    assert score == 0.0


def test_new_dale_chall_formula_components() -> None:
    """Test that the formula components are calculated correctly."""
    text = "This is a test sentence with some difficult words like extraordinary and phenomenon."
    
    from textstat.backend.counts._count_words import count_words
    from textstat.backend.counts._count_difficult_words import count_difficult_words
    from textstat.backend.counts._count_sentences import count_sentences
    
    word_count = count_words(text)
    hard_count = count_difficult_words(text, "en_US", syllable_threshold=0)
    sent_count = count_sentences(text)
    
    pdw = 100 * hard_count / word_count
    asl = word_count / sent_count
    
    expected_score = 64 - (0.95 * pdw) - (0.69 * asl)
    actual_score = metrics.new_dale_chall_readability_score(text, "en_US")
    
    assert round(actual_score, 3) == round(expected_score, 3)

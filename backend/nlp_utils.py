"""NLP helpers for Brainsplain.

spaCy, wordfreq, and textstat are imported only when their functions are
called. The spaCy language pipeline is loaded once per worker process.
"""
import re
from collections import Counter
from functools import lru_cache

TARGET_GRADE = {
    "Age 5": 6,
    "Age 10": 8,
    "Teen": 11,
}


@lru_cache(maxsize=1)
def get_nlp():
    """Load the spaCy English model only when NLP analysis is first requested."""
    import spacy

    print("Loading spaCy en_core_web_sm...")
    return spacy.load("en_core_web_sm", disable=["parser"])


def analyze_input(text, top_n=6):
    from wordfreq import zipf_frequency

    doc = get_nlp()(text)

    words = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ("NOUN", "PROPN")
        and token.is_alpha
        and not token.is_stop
    ]

    counts = Counter(words)
    hard = [
        word for word in counts
        if zipf_frequency(word, "en") < 3.5
    ]
    hard.sort(key=counts.get, reverse=True)

    entities = list({entity.text for entity in doc.ents})[:top_n]

    return {
        "terms": hard[:top_n],
        "entities": entities,
    }


def readability(text, level):
    import textstat

    clean = re.sub(r"[^\w\s.,!?'-]", "", text)
    grade = round(textstat.flesch_kincaid_grade(clean), 1)
    target = TARGET_GRADE[level]

    return {
        "grade": grade,
        "target": target,
        "fits": grade <= target,
    }

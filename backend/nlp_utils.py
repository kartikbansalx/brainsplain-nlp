import re
from collections import Counter

import spacy
import textstat
from wordfreq import zipf_frequency

nlp = spacy.load("en_core_web_sm", disable=["parser"])  # load once at startup

TARGET_GRADE = {"Age 5": 6, "Age 10": 8, "Teen": 11}  # starting values, tune on real outputs


def analyze_input(text, top_n=6):
    doc = nlp(text)

    # nouns only, no stop words, lemmatized ("cells" -> "cell")
    words = [t.lemma_.lower() for t in doc
             if t.pos_ in ("NOUN", "PROPN") and t.is_alpha and not t.is_stop]

    # "hard" = rare in everyday English (low Zipf score), most frequent first
    counts = Counter(words)
    hard = [w for w in counts if zipf_frequency(w, "en") < 3.5]
    hard.sort(key=counts.get, reverse=True)

    entities = list({e.text for e in doc.ents})[:top_n]
    return {"terms": hard[:top_n], "entities": entities}


def readability(text, level):
    clean = re.sub(r"[^\w\s.,!?'-]", "", text)  # drop emojis before scoring
    grade = round(textstat.flesch_kincaid_grade(clean), 1)
    target = TARGET_GRADE[level]
    return {"grade": grade, "target": target, "fits": grade <= target}

from pathlib import Path
import json
import math
import re
from collections import Counter


PROJECT_DIR = Path(__file__).resolve().parent
IR_DIR = PROJECT_DIR / "ir_artifacts"

INDEX_PATH = IR_DIR / "inverted_index.json"
TF_PATH = IR_DIR / "document_term_frequencies.json"


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by",
    "for", "from", "has", "have", "in", "is", "it",
    "of", "on", "or", "that", "the", "this", "to",
    "was", "were", "with", "will", "you", "your"
}


def stem(word):
    for suffix in ["ingly", "edly", "ing", "ed", "es", "s"]:
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[:-len(suffix)]
    return word


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return [
        stem(word)
        for word in text.split()
        if word not in STOPWORDS
    ]


def load_data():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    with open(TF_PATH, "r", encoding="utf-8") as f:
        term_frequencies = json.load(f)

    return index, term_frequencies


def tfidf_search(query, top_k=5):

    index, term_frequencies = load_data()

    query_terms = preprocess(query)

    if not query_terms:
        return []

    documents = list(term_frequencies.keys())
    total_docs = len(documents)

    query_count = Counter(query_terms)

    scores = Counter()

    for term, qtf in query_count.items():

        if term not in index:
            continue

        df = len(index[term])

        if df == 0:
            continue

        idf = math.log(
            total_docs / df
        )

        for doc_id, tf in index[term].items():

            tf_weight = 1 + math.log(tf)

            scores[doc_id] += (
                qtf
                * tf_weight
                * idf
            )

    results = []

    for doc_id, score in scores.items():

        matched_terms = [
            term
            for term in query_terms
            if term in index and doc_id in index[term]
        ]

        results.append({
            "document_id": doc_id,
            "document": doc_id,
            "score": round(score, 6),
            "matched_terms": matched_terms
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]
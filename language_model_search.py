"""
Unit IV - Language Model Based Information Retrieval

Unigram / Multinomial Language Model
with Jelinek-Mercer smoothing.
"""

from pathlib import Path
import json
import math
import re


# =========================================================
# PATHS
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent
IR_DIR = PROJECT_DIR / "ir_artifacts"

TF_PATH = IR_DIR / "document_term_frequencies.json"


# =========================================================
# SETTINGS
# =========================================================

LAMBDA = 0.8

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by",
    "for", "from", "has", "have", "in", "is", "it",
    "of", "on", "or", "that", "the", "this", "to",
    "was", "were", "with", "will", "you", "your"
}


# =========================================================
# PREPROCESSING
# =========================================================

def stem(word):
    """Simple stemmer matching the project index."""

    for suffix in ["ingly", "edly", "ing", "ed", "es", "s"]:

        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[:-len(suffix)]

    return word


def preprocess(text):
    """Convert text into indexed terms."""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    words = text.split()

    return [
        stem(word)
        for word in words
        if word not in STOPWORDS
    ]


# =========================================================
# LOAD INDEX
# =========================================================

def load_data():

    if not TF_PATH.exists():

        raise FileNotFoundError(
            "document_term_frequencies.json not found.\n"
            "Run: python build_inverted_index.py"
        )

    with open(TF_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# =========================================================
# BUILD COLLECTION
# =========================================================

def build_model():

    data = load_data()

    documents = {}
    collection_frequency = {}
    collection_length = 0

    for document_id, terms in data.items():

        terms = {
            term: int(freq)
            for term, freq in terms.items()
        }

        doc_length = sum(terms.values())

        documents[document_id] = {
            "terms": terms,
            "length": doc_length
        }

        for term, freq in terms.items():

            collection_frequency[term] = (
                collection_frequency.get(term, 0) + freq
            )

            collection_length += freq

    return (
        documents,
        collection_frequency,
        collection_length
    )


# =========================================================
# LANGUAGE MODEL RANKING
# =========================================================

def search(query, top_k=5):

    documents, collection_frequency, collection_length = (
        build_model()
    )

    query_terms = preprocess(query)

    # Keep only terms existing in the collection
    query_terms = [
        term for term in query_terms
        if term in collection_frequency
    ]

    if not query_terms:
        return []

    results = []

    for doc_id, doc in documents.items():

        score = 0.0
        matched = []

        for term in query_terms:

            tf = doc["terms"].get(term, 0)

            if tf > 0:
                matched.append(term)

            # P(term | document)
            doc_prob = tf / doc["length"]

            # P(term | collection)
            collection_prob = (
                collection_frequency[term]
                / collection_length
            )

            # Jelinek-Mercer smoothing
            probability = (
                LAMBDA * doc_prob
                + (1 - LAMBDA) * collection_prob
            )

            score += math.log(probability)

        results.append({
            "document": doc_id,
            "score": round(score, 6),
            "matched_terms": matched
        })

    # Documents containing query terms first,
    # then language-model score.
    results.sort(
        key=lambda x: (
            len(x["matched_terms"]),
            x["score"]
        ),
        reverse=True
    )

    return results[:top_k]


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    documents, collection_frequency, collection_length = (
        build_model()
    )

    print("=" * 60)
    print("HR LANGUAGE MODEL SEARCH")
    print("=" * 60)

    print(f"Documents loaded: {len(documents)}")
    print(f"Collection length: {collection_length}")
    print(f"Lambda: {LAMBDA}")

    test_queries = [
        "promotion",
        "training",
        "overtime",
        "performance review",
        "employee benefits"
    ]

    for query in test_queries:

        print("\n" + "-" * 60)
        print(f"Query: {query}")
        print("-" * 60)

        results = search(query)

        if not results:
            print("No matching documents.")
            continue

        for i, result in enumerate(results, 1):

            print(
                f"{i}. {result['document']} | "
                f"Score: {result['score']} | "
                f"Matched: "
                f"{', '.join(result['matched_terms'])}"
            )

    print("\nInteractive Search")
    print("Type 'exit' to stop.\n")

    while True:

        query = input("Enter search query: ").strip()

        if query.lower() == "exit":
            break

        results = search(query)

        if not results:
            print("No matching documents.\n")
            continue

        for i, result in enumerate(results, 1):

            print(
                f"{i}. {result['document']} | "
                f"Score: {result['score']} | "
                f"Matched: "
                f"{', '.join(result['matched_terms'])}"
            )

        print()
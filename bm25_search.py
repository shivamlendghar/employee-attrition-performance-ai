# ==========================================================
# bm25_search.py
# ==========================================================
# HR Information Retrieval
# BM25 Ranked Retrieval
#
# Uses the inverted index created by:
# build_inverted_index.py
# ==========================================================

from pathlib import Path
import json
import math
import re
from collections import Counter


# ==========================================================
# PATHS
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent

IR_ARTIFACT_DIR = PROJECT_DIR / "ir_artifacts"

INVERTED_INDEX_PATH = IR_ARTIFACT_DIR / "inverted_index.json"
DOCUMENT_FREQUENCY_PATH = IR_ARTIFACT_DIR / "document_frequency.json"
DOCUMENT_TF_PATH = IR_ARTIFACT_DIR / "document_term_frequencies.json"


# ==========================================================
# STOPWORDS
# ==========================================================

STOPWORDS = {
    "a", "an", "the", "and", "or", "but",
    "if", "then", "than", "for", "from",
    "to", "of", "in", "on", "at", "by",
    "with", "about", "as", "into", "through",
    "during", "before", "after", "above",
    "below", "between", "is", "are", "was",
    "were", "be", "been", "being", "has",
    "have", "had", "do", "does", "did",
    "will", "would", "should", "could",
    "may", "might", "must", "can",
    "this", "that", "these", "those",
    "it", "its", "they", "their", "them",
    "he", "she", "his", "her", "we",
    "our", "you", "your", "i", "me", "my"
}


# ==========================================================
# SIMPLE STEMMER
# ==========================================================

def simple_stem(word):
    """
    Apply the same basic stemming logic used by
    the inverted-index module.
    """

    word = word.lower().strip()

    suffixes = [
        "ingly",
        "edly",
        "ments",
        "ment",
        "ness",
        "ing",
        "ers",
        "ies",
        "ed",
        "er",
        "es",
        "s",
    ]

    for suffix in suffixes:
        if (
            word.endswith(suffix)
            and len(word) > len(suffix) + 2
        ):
            word = word[:-len(suffix)]
            break

    return word


# ==========================================================
# QUERY PREPROCESSING
# ==========================================================

def preprocess_query(query):
    """
    Convert the user query into normalized terms.
    """

    if query is None:
        return []

    query = str(query).lower()

    # Remove punctuation
    query = re.sub(
        r"[^a-z0-9\s]",
        " ",
        query
    )

    tokens = query.split()

    processed_terms = []

    for token in tokens:

        if token in STOPWORDS:
            continue

        if len(token) < 2:
            continue

        token = simple_stem(token)

        if token:
            processed_terms.append(token)

    return processed_terms


# ==========================================================
# LOAD JSON ARTIFACTS
# ==========================================================

def load_json(path):
    """
    Load a JSON IR artifact.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Missing IR artifact: {path}\n"
            "Run build_inverted_index.py first."
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================================
# LOAD INDEX
# ==========================================================

print("=" * 70)
print("HR INFORMATION RETRIEVAL - BM25")
print("=" * 70)

print("\nLoading index...")

INVERTED_INDEX = load_json(INVERTED_INDEX_PATH)

DOCUMENT_FREQUENCY = load_json(
    DOCUMENT_FREQUENCY_PATH
)

DOCUMENT_TERM_FREQUENCIES = load_json(
    DOCUMENT_TF_PATH
)

DOCUMENTS = sorted(
    DOCUMENT_TERM_FREQUENCIES.keys()
)

TOTAL_DOCUMENTS = len(DOCUMENTS)

print(
    f"Documents loaded : {TOTAL_DOCUMENTS}"
)

print(
    f"Unique terms     : {len(INVERTED_INDEX)}"
)


# ==========================================================
# DOCUMENT LENGTHS
# ==========================================================

DOCUMENT_LENGTHS = {}

for document_id, term_frequencies in (
    DOCUMENT_TERM_FREQUENCIES.items()
):
    DOCUMENT_LENGTHS[document_id] = sum(
        term_frequencies.values()
    )


# ==========================================================
# AVERAGE DOCUMENT LENGTH
# ==========================================================

if TOTAL_DOCUMENTS > 0:

    AVG_DOCUMENT_LENGTH = (
        sum(DOCUMENT_LENGTHS.values())
        / TOTAL_DOCUMENTS
    )

else:

    AVG_DOCUMENT_LENGTH = 0.0


# ==========================================================
# BM25 PARAMETERS
# ==========================================================

K1 = 1.5
B = 0.75


# ==========================================================
# IDF
# ==========================================================

def calculate_bm25_idf(term):
    """
    Calculate BM25 inverse document frequency.

    IDF(t) =
        log(
            1 +
            (N - df + 0.5)
            /
            (df + 0.5)
        )
    """

    df = DOCUMENT_FREQUENCY.get(
        term,
        0
    )

    if df == 0:
        return 0.0

    return math.log(
        1
        +
        (
            TOTAL_DOCUMENTS
            - df
            + 0.5
        )
        /
        (
            df
            + 0.5
        )
    )


# ==========================================================
# BM25 TERM SCORE
# ==========================================================

def bm25_term_score(term, document_id):
    """
    Calculate BM25 contribution of
    one query term to one document.
    """

    document_terms = (
        DOCUMENT_TERM_FREQUENCIES.get(
            document_id,
            {}
        )
    )

    tf = document_terms.get(
        term,
        0
    )

    if tf == 0:
        return 0.0

    idf = calculate_bm25_idf(term)

    document_length = DOCUMENT_LENGTHS.get(
        document_id,
        0
    )

    if AVG_DOCUMENT_LENGTH == 0:
        return 0.0

    normalization = (
        1
        - B
        +
        B
        * (
            document_length
            / AVG_DOCUMENT_LENGTH
        )
    )

    denominator = (
        tf
        +
        K1
        * normalization
    )

    score = (
        idf
        *
        (
            tf
            * (K1 + 1)
        )
        /
        denominator
    )

    return score


# ==========================================================
# BM25 SEARCH
# ==========================================================

def bm25_search(query, top_k=5):
    """
    Rank HR documents using BM25.

    Parameters
    ----------
    query : str
        User search query.

    top_k : int
        Number of top results to return.

    Returns
    -------
    list
        Ranked documents with BM25 scores.
    """

    # Make sure top_k is valid
    try:
        top_k = int(top_k)
    except (TypeError, ValueError):
        top_k = 5

    if top_k <= 0:
        top_k = 5

    # ----------------------------------------------
    # Preprocess query
    # ----------------------------------------------

    query_terms = preprocess_query(query)

    if not query_terms:
        return []

    # Remove duplicate terms
    query_terms = list(
        dict.fromkeys(query_terms)
    )

    # ----------------------------------------------
    # Find candidate documents
    # ----------------------------------------------

    candidate_documents = set()

    for term in query_terms:

        postings = INVERTED_INDEX.get(
            term,
            {}
        )

        candidate_documents.update(
            postings.keys()
        )

    if not candidate_documents:
        return []

    # ----------------------------------------------
    # Calculate document scores
    # ----------------------------------------------

    scores = Counter()

    for document_id in candidate_documents:

        document_score = 0.0

        matched_terms = 0

        for term in query_terms:

            term_score = bm25_term_score(
                term,
                document_id
            )

            if term_score > 0:
                matched_terms += 1

            document_score += term_score

        if document_score > 0:

            scores[document_id] = (
                document_score,
                matched_terms
            )

    # ----------------------------------------------
    # Sort results
    #
    # Primary   : BM25 score
    # Secondary : number of matched terms
    # ----------------------------------------------

    ranked_items = sorted(
        scores.items(),
        key=lambda item: (
            item[1][0],
            item[1][1]
        ),
        reverse=True
    )

    # ----------------------------------------------
    # Format results
    # ----------------------------------------------

    ranked_results = []

    for document_id, (
        score,
        matched_terms
    ) in ranked_items[:top_k]:

        ranked_results.append(
            {
                "document": document_id,
                "score": float(score),
                "matched_terms": int(matched_terms)
            }
        )

    return ranked_results


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

def display_results(results, limit=10):
    """
    Display BM25 results in the terminal.
    """

    print("\n" + "=" * 70)
    print("BM25 SEARCH RESULTS")
    print("=" * 70)

    if not results:

        print("\nNo matching documents found.")
        return

    for rank, result in enumerate(
        results[:limit],
        start=1
    ):

        print(
            f"\n{rank}. "
            f"{result['document']}"
        )

        print(
            f"   BM25 Score: "
            f"{result['score']:.4f}"
        )

        if "matched_terms" in result:
            print(
                f"   Matched Terms: "
                f"{result['matched_terms']}"
            )


# ==========================================================
# TEST QUERIES
# ==========================================================

def run_tests():
    """
    Run sample BM25 queries.
    """

    test_queries = [
        "overtime",
        "employee benefits",
        "training",
        "performance review",
        "promotion",
        "manager support",
        "work life balance",
    ]

    for query in test_queries:

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        results = bm25_search(
            query,
            top_k=5
        )

        display_results(
            results,
            limit=5
        )


# ==========================================================
# INTERACTIVE MODE
# ==========================================================

def interactive_search():
    """
    Run interactive BM25 search from terminal.
    """

    print("\n" + "=" * 70)
    print("INTERACTIVE BM25 SEARCH")
    print("=" * 70)

    print("\nType 'exit' to stop.")

    while True:

        query = input(
            "\nEnter query: "
        ).strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results = bm25_search(
            query,
            top_k=5
        )

        display_results(
            results,
            limit=5
        )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    run_tests()

    interactive_search()
# ==========================================================
# build_inverted_index.py
#
# HR Information Retrieval
# Text Preprocessing + Inverted Index
# ==========================================================

from pathlib import Path
import json
import re
from collections import defaultdict, Counter


# ==========================================================
# PATHS
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent

DOCUMENT_DIR = PROJECT_DIR / "extracted_documents"

IR_ARTIFACT_DIR = PROJECT_DIR / "ir_artifacts"

IR_ARTIFACT_DIR.mkdir(exist_ok=True)


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
    "our", "you", "your", "i", "me",
    "my", "an", "any", "all"
}


# ==========================================================
# SIMPLE STEMMER
# ==========================================================

def simple_stem(word):
    """
    Small rule-based stemmer.

    This is intentionally simple so the preprocessing
    remains transparent for an academic IR project.
    """

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
        "s"
    ]

    for suffix in suffixes:

        if (
            word.endswith(suffix)
            and len(word) > len(suffix) + 2
        ):

            word = word[
                :-len(suffix)
            ]

            break

    # Handle common ies → y
    if word.endswith("i") and len(word) > 3:
        pass

    return word


# ==========================================================
# TOKENIZATION
# ==========================================================

def preprocess_text(text):
    """
    Convert raw text into normalized tokens.

    Steps:
        1. Lowercase
        2. Remove non-alphanumeric characters
        3. Tokenize
        4. Remove stopwords
        5. Remove very short tokens
        6. Apply simple stemming
    """

    # Lowercase
    text = text.lower()

    # Keep letters and numbers
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # Tokenize
    tokens = text.split()

    processed_tokens = []

    for token in tokens:

        # Stopword removal
        if token in STOPWORDS:
            continue

        # Ignore very short tokens
        if len(token) < 2:
            continue

        # Simple stemming
        token = simple_stem(token)

        if token:
            processed_tokens.append(token)

    return processed_tokens


# ==========================================================
# READ DOCUMENT
# ==========================================================

def read_document(file_path):
    """
    Read an extracted text document.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as file:

        return file.read()


# ==========================================================
# BUILD INVERTED INDEX
# ==========================================================

def build_index():
    """
    Build:

        term -> {
            document_id: term_frequency
        }

    Example:

        overtime:
            overtime_policy: 4

        training:
            training_policy: 5
            performance_policy: 2
    """

    inverted_index = defaultdict(dict)

    document_term_frequencies = {}

    documents = sorted(
        DOCUMENT_DIR.glob("*.txt")
    )

    print(
        f"\nDocuments found: {len(documents)}"
    )

    if not documents:

        raise FileNotFoundError(
            "No extracted TXT documents found in "
            f"{DOCUMENT_DIR}"
        )

    # ------------------------------------------------------
    # Process each document
    # ------------------------------------------------------

    for document in documents:

        print(
            f"\nProcessing: {document.name}"
        )

        text = read_document(
            document
        )

        tokens = preprocess_text(
            text
        )

        # Count term frequencies
        term_counts = Counter(
            tokens
        )

        document_id = (
            document.stem
        )

        document_term_frequencies[
            document_id
        ] = dict(term_counts)

        # Add to inverted index
        for term, frequency in term_counts.items():

            inverted_index[term][
                document_id
            ] = frequency

        print(
            f"  Original words : "
            f"{len(text.split())}"
        )

        print(
            f"  Processed tokens: "
            f"{len(tokens)}"
        )

        print(
            f"  Unique terms    : "
            f"{len(term_counts)}"
        )

    return (
        dict(inverted_index),
        document_term_frequencies
    )


# ==========================================================
# DOCUMENT FREQUENCY
# ==========================================================

def calculate_document_frequency(
    inverted_index
):
    """
    Calculate document frequency:

        DF(term) = number of documents
                   containing the term
    """

    document_frequency = {}

    for term, postings in inverted_index.items():

        document_frequency[term] = len(
            postings
        )

    return document_frequency


# ==========================================================
# SAVE JSON
# ==========================================================

def save_json(data, file_path):
    """
    Save dictionary as JSON.
    """

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# SEARCH TERM
# ==========================================================

def search_term(
    inverted_index,
    term
):
    """
    Return documents containing a term.
    """

    term = term.lower()

    if term not in inverted_index:

        return {}

    return inverted_index[
        term
    ]


# ==========================================================
# DISPLAY SAMPLE INDEX
# ==========================================================

def display_sample_terms(
    inverted_index,
    document_frequency
):

    print("\n" + "=" * 70)
    print("SAMPLE INVERTED INDEX")
    print("=" * 70)

    # Sort terms alphabetically
    terms = sorted(
        inverted_index.keys()
    )

    for term in terms[:30]:

        print(
            f"{term:20} "
            f"DF={document_frequency[term]:<3} "
            f"{inverted_index[term]}"
        )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("HR INFORMATION RETRIEVAL")
    print("TEXT PREPROCESSING + INVERTED INDEX")
    print("=" * 70)

    # ------------------------------------------------------
    # Build index
    # ------------------------------------------------------

    (
        inverted_index,
        document_term_frequencies
    ) = build_index()

    # ------------------------------------------------------
    # Document frequency
    # ------------------------------------------------------

    document_frequency = (
        calculate_document_frequency(
            inverted_index
        )
    )

    # ------------------------------------------------------
    # Save index
    # ------------------------------------------------------

    save_json(
        inverted_index,
        IR_ARTIFACT_DIR /
        "inverted_index.json"
    )

    save_json(
        document_term_frequencies,
        IR_ARTIFACT_DIR /
        "document_term_frequencies.json"
    )

    save_json(
        document_frequency,
        IR_ARTIFACT_DIR /
        "document_frequency.json"
    )

    # ------------------------------------------------------
    # Save processed documents
    # ------------------------------------------------------

    processed_documents = {}

    for document in sorted(
        DOCUMENT_DIR.glob("*.txt")
    ):

        text = read_document(
            document
        )

        processed_documents[
            document.stem
        ] = preprocess_text(
            text
        )

    save_json(
        processed_documents,
        IR_ARTIFACT_DIR /
        "processed_documents.json"
    )

    # ------------------------------------------------------
    # Display sample
    # ------------------------------------------------------

    display_sample_terms(
        inverted_index,
        document_frequency
    )

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("INDEX STATISTICS")
    print("=" * 70)

    print(
        "Number of documents : "
        f"{len(document_term_frequencies)}"
    )

    print(
        "Number of unique terms: "
        f"{len(inverted_index)}"
    )

    print(
        "Total indexed postings: "
        f"{sum(len(v) for v in inverted_index.values())}"
    )

    # ------------------------------------------------------
    # Example searches
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("SAMPLE TERM SEARCH")
    print("=" * 70)

    test_terms = [
        "employee",
        "overtime",
        "training",
        "promotion",
        "benefits",
        "performance"
    ]

    for term in test_terms:

        result = search_term(
            inverted_index,
            term
        )

        print(
            f"\n'{term}' → {result}"
        )

    # ------------------------------------------------------
    # Final message
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("INVERTED INDEX BUILD COMPLETED")
    print("=" * 70)

    print("\nGenerated files:")

    print(
        "ir_artifacts/inverted_index.json"
    )

    print(
        "ir_artifacts/document_term_frequencies.json"
    )

    print(
        "ir_artifacts/document_frequency.json"
    )

    print(
        "ir_artifacts/processed_documents.json"
    )


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main() 
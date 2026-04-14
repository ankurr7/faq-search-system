# Import required libraries
from flask import Flask, request, jsonify, send_from_directory
import math
import json

# Create Flask app
app = Flask(__name__)

# Load FAQ data from JSON file
with open("faqs.json") as f:
    faqs = json.load(f)


# -------------------------------
# TOKENIZATION FUNCTION
# -------------------------------
def tokenize(text):
    """
    Convert text to lowercase and split into words
    Example: "What is NLP" → ["what", "is", "nlp"]
    """
    return text.lower().split()


# -------------------------------
# TERM FREQUENCY (TF)
# -------------------------------
def tf(words):
    """
    Count how many times each word appears
    Example: ["what","is","nlp"] → {"what":1, "is":1, "nlp":1}
    """
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


# -------------------------------
# INVERSE DOCUMENT FREQUENCY (IDF)
# -------------------------------
def idf(docs):
    """
    Calculate importance of words across all documents
    Rare words → high value
    Common words → low value
    """
    idf = {}
    N = len(docs)  # total number of documents

    for doc in docs:
        for word in set(doc):  # unique words only
            idf[word] = idf.get(word, 0) + 1

    for word in idf:
        idf[word] = math.log(N / idf[word])  # formula

    return idf


# -------------------------------
# TF-IDF CALCULATION
# -------------------------------
def tfidf(tf_vals, idf_vals):
    """
    Multiply TF and IDF values
    Gives importance score for each word
    """
    return {
        word: tf_vals[word] * idf_vals.get(word, 0)
        for word in tf_vals
    }


# -------------------------------
# SIMILARITY FUNCTION
# -------------------------------
def similarity(v1, v2):
    """
    Compare two vectors using dot product
    Higher score = more similar
    """
    score = 0
    for w in v1:
        if w in v2:
            score += v1[w] * v2[w]
    return score


# -------------------------------
# HOME ROUTE (LOAD UI)
# -------------------------------
@app.route("/")
def home():
    """
    Serve index.html file
    """
    return send_from_directory("static", "index.html")


# -------------------------------
# SEARCH API
# -------------------------------
@app.route("/search", methods=["POST"])
def search():
    """
    Main logic:
    1. Take user query
    2. Convert to TF-IDF
    3. Compare with all FAQs
    4. Return best match
    """

    # Get user input
    query = request.json["query"]

    # Tokenize user query
    query_words = tokenize(query)

    # Tokenize all FAQ questions
    docs = [tokenize(f["question"]) for f in faqs]

    # Calculate IDF values
    idf_vals = idf(docs)

    # Convert query into vector
    query_vec = tfidf(tf(query_words), idf_vals)

    # Find best match
    best = None
    max_score = -1

    for i, faq in enumerate(faqs):
        # Convert FAQ question into vector
        doc_vec = tfidf(tf(docs[i]), idf_vals)

        # Calculate similarity
        score = similarity(query_vec, doc_vec)

        # Check best match
        if score > max_score:
            max_score = score
            best = faq

    # If no good match found
    if max_score < 0.1:
        return jsonify({"answer": "No matching answer found ❌"})

    # Return best answer
    return jsonify({"answer": best["answer"]})


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
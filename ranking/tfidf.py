import math
from collections import defaultdict


class TFIDFRanker:
    """
    Ranks documents using TF-IDF.
    """

    def __init__(self, inverted_index, num_docs):
        self.index = inverted_index.index  # term -> {doc_id: tf}
        self.num_docs = num_docs
        self.idf = {}

        self._compute_idf()

    def _compute_idf(self):
        for term, postings in self.index.items():
            df = len(postings)
            # add 1 to avoid division by zero
            self.idf[term] = math.log((self.num_docs + 1) / (df + 1)) + 1

    def rank(self, query_tokens, top_k=5):
        scores = defaultdict(float)

        for term in query_tokens:
            if term not in self.index:
                continue

            for doc_id, tf in self.index[term].items():
                scores[doc_id] += tf * self.idf.get(term, 0.0)

        # sort by score desc
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

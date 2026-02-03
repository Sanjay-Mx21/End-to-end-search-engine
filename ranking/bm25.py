import math
from collections import defaultdict


class BM25Ranker:
    """
    BM25 ranking implementation.
    """

    def __init__(self, inverted_index, documents, k1=1.5, b=0.75):
        self.index = inverted_index.index   # term -> {doc_id: tf}
        self.documents = documents          # list of {url, tokens}
        self.N = len(documents)
        self.k1 = k1
        self.b = b

        self.doc_len = {}
        self.avg_doc_len = 0.0

        self._prepare()

    def _prepare(self):
        total_len = 0
        for doc_id, doc in enumerate(self.documents):
            length = len(doc["tokens"])
            self.doc_len[doc_id] = length
            total_len += length

        self.avg_doc_len = total_len / self.N if self.N > 0 else 0.0

    def _idf(self, term):
        df = len(self.index.get(term, {}))
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1)

    def rank(self, query_tokens, top_k=5):
        scores = defaultdict(float)

        for term in query_tokens:
            if term not in self.index:
                continue

            idf = self._idf(term)

            for doc_id, tf in self.index[term].items():
                dl = self.doc_len.get(doc_id, 0)
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avg_doc_len)
                scores[doc_id] += idf * (numerator / denominator)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

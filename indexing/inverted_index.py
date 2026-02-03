from collections import defaultdict


class InvertedIndex:
    """
    Maps terms to documents and term frequencies.
    """

    def __init__(self):
        # term -> {doc_id: frequency}
        self.index = defaultdict(dict)

    def add_document(self, doc_id, tokens):
        for token in tokens:
            if doc_id not in self.index[token]:
                self.index[token][doc_id] = 0
            self.index[token][doc_id] += 1

    def get_postings(self, term):
        return self.index.get(term, {})

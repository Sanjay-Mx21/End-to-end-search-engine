from indexing.inverted_index import InvertedIndex


class IndexBuilder:
    """
    Builds an inverted index from processed documents.
    """

    def __init__(self):
        self.index = InvertedIndex()

    def build(self, processed_docs):
        for doc_id, doc in enumerate(processed_docs):
            self.index.add_document(doc_id, doc["tokens"])
        return self.index

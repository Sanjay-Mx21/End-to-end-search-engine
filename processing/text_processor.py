import json
import os

from processing.normalizer import normalize
from processing.tokenizer import tokenize


class TextProcessor:
    """
    Orchestrates text normalization and tokenization.
    """

    def __init__(self, data_dir="data/raw_pages"):
        self.data_dir = data_dir

    def process_all_pages(self):
        processed_docs = []

        for filename in os.listdir(self.data_dir):
            filepath = os.path.join(self.data_dir, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            normalized_text = normalize(data["text"])
            tokens = tokenize(normalized_text)

            processed_docs.append({
                "url": data["url"],
                "tokens": tokens
            })

        return processed_docs

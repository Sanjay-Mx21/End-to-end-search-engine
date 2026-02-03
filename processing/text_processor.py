import os
import json

from processing.normalizer import normalize
from processing.tokenizer import tokenize


class TextProcessor:
    def __init__(self, data_dir="data/raw_pages"):
        self.data_dir = data_dir

    def process_all_pages(self):
        processed_docs = []

        # ✅ PRODUCTION-SAFE CHECK
        if not os.path.exists(self.data_dir):
            print(f"[WARN] Data directory not found: {self.data_dir}")
            return processed_docs

        for filename in os.listdir(self.data_dir):
            filepath = os.path.join(self.data_dir, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_text = data.get("text") or data.get("content")

            if not raw_text:
                continue   # skip bad / empty docs safely

            normalized_text = normalize(raw_text)  # ✅ FIX
            tokens = tokenize(normalized_text)

            processed_docs.append({
                "url": data.get("url", "unknown"),
                "tokens": tokens
            })

        return processed_docs

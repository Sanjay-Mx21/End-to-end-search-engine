import json
import os
import hashlib


class PageStorage:
    """
    Responsible for storing crawled pages on disk.
    Each page is stored as a JSON file.
    """

    def __init__(self, storage_dir="data/raw_pages"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _generate_filename(self, url):
        """
        Generate a safe, unique filename from a URL.
        """
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return f"{url_hash}.json"

    def save_page(self, url, text):
        filename = self._generate_filename(url)
        filepath = os.path.join(self.storage_dir, filename)

        data = {
            "url": url,
            "text": text
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

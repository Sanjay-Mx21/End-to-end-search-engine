from collections import deque


class URLManager:
    """
    Controls which URLs are crawled and prevents infinite crawling.
    """

    def __init__(self, seed_url, max_depth=1):
        self.queue = deque()
        self.visited = set()
        self.max_depth = max_depth

        # Store (url, depth)
        self.queue.append((seed_url, 0))

    def has_next(self):
        return len(self.queue) > 0

    def get_next(self):
        return self.queue.popleft()

    def add_urls(self, urls, current_depth):
        next_depth = current_depth + 1

        if next_depth > self.max_depth:
            return

        for url in urls:
            if url not in self.visited:
                self.queue.append((url, next_depth))

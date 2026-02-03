import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawler.url_manager import URLManager


def crawl_single_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    text = soup.get_text(separator=" ", strip=True)

    links = set()
    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(url, tag["href"])
        links.add(absolute_url)

    return text, links


def crawl_website(seed_url, max_depth=1, max_pages=5):
    url_manager = URLManager(seed_url, max_depth)

    crawled_pages = []
    pages_crawled = 0

    while url_manager.has_next() and pages_crawled < max_pages:
        current_url, depth = url_manager.get_next()

        if current_url in url_manager.visited:
            continue

        try:
            print(f"Crawling: {current_url} (depth={depth})")

            text, links = crawl_single_page(current_url)

            crawled_pages.append({
                "url": current_url,
                "text": text
            })

            url_manager.visited.add(current_url)
            url_manager.add_urls(links, depth)

            pages_crawled += 1

        except Exception as e:
            print(f"Failed to crawl {current_url}: {e}")

    return crawled_pages


if __name__ == "__main__":
    seed_url = "https://example.com"

    pages = crawl_website(seed_url, max_depth=1, max_pages=5)

    print(f"\nTotal pages crawled: {len(pages)}")

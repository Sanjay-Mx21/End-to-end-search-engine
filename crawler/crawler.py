import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def crawl_single_page(url):
    """
    Fetches a single web page and extracts:
    1. Visible text
    2. All absolute links on the page
    """

    print(f"Crawling URL: {url}")

    # 1. Send HTTP request
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # fails fast if request breaks

    # 2. Parse HTML
    soup = BeautifulSoup(response.text, "lxml")

    # 3. Extract visible text
    page_text = soup.get_text(separator=" ", strip=True)

    # 4. Extract links
    links = set()
    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(url, tag["href"])
        links.add(absolute_url)

    return page_text, links


if __name__ == "__main__":
    seed_url = "https://example.com"

    text, links = crawl_single_page(seed_url)

    print("\n--- PAGE TEXT (first 300 chars) ---")
    print(text[:300])

    print("\n--- LINKS FOUND ---")
    for link in list(links)[:10]:
        print(link)

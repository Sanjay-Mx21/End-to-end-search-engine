from processing.stopwords import STOPWORDS


def tokenize(text: str) -> list[str]:
    words = text.split()
    tokens = [w for w in words if w not in STOPWORDS]
    return tokens

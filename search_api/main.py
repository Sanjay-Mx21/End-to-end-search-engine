from fastapi import FastAPI, Query

from processing.text_processor import TextProcessor
from indexing.index_builder import IndexBuilder
from ranking.tfidf import TFIDFRanker

app = FastAPI(title="Mini Search Engine")

# Build everything once at startup
processor = TextProcessor()
processed_docs = processor.process_all_pages()

builder = IndexBuilder()
index = builder.build(processed_docs)

ranker = TFIDFRanker(index, num_docs=len(processed_docs))


@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    query_tokens = q.lower().split()

    ranked_results = ranker.rank(query_tokens)

    results = []
    for doc_id, score in ranked_results:
        results.append({
            "url": processed_docs[doc_id]["url"],
            "score": score
        })

    return {
        "query": q,
        "results": results
    }

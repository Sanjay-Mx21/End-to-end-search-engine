from fastapi import FastAPI, Query
from processing.normalizer import normalize
from processing.tokenizer import tokenize
from processing.text_processor import TextProcessor
from indexing.index_builder import IndexBuilder
from ranking.tfidf import TFIDFRanker
from ranking.bm25 import BM25Ranker


app = FastAPI(title="Mini Search Engine")

# Build everything once at startup
processor = TextProcessor()
processed_docs = processor.process_all_pages()

if not processed_docs:
    print("[WARN] No documents found. Search index will be empty.")

builder = IndexBuilder()
index = builder.build(processed_docs)

ranker = TFIDFRanker(index, num_docs=len(processed_docs))
bm25_ranker = BM25Ranker(index, processed_docs)



@app.get("/search")
def search(
    q: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20),
    ranker_type: str = Query("tfidf", enum=["tfidf", "bm25"])
):
    # Process query using SAME pipeline as documents
    normalized_query = normalize(q)
    query_tokens = tokenize(normalized_query)

    # Choose ranker
    if ranker_type == "bm25":
        ranked_results = bm25_ranker.rank(query_tokens, top_k=top_k)
    else:
        ranked_results = ranker.rank(query_tokens, top_k=top_k)

    # Build response
    results = []
    for doc_id, score in ranked_results:
        results.append({
            "url": processed_docs[doc_id]["url"],
            "score": score
        })

    return {
        "query": q,
        "ranker": ranker_type,
        "top_k": top_k,
        "results": results
    }
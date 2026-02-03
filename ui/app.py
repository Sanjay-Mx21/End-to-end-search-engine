import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/search"

st.set_page_config(page_title="Mini Search Engine", layout="centered")

st.title("🔍 Mini Search Engine")
st.write("Search over crawled documents using TF-IDF or BM25")

query = st.text_input("Enter search query")

ranker = st.selectbox(
    "Choose ranking algorithm",
    ["tfidf", "bm25"]
)

top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        params = {
            "q": query,
            "ranker_type": ranker,
            "top_k": top_k
        }

        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            results = data["results"]

            if not results:
                st.info("No results found.")
            else:
                for i, res in enumerate(results, start=1):
                    st.markdown(f"### {i}. {res['url']}")
                    st.write(f"Score: `{round(res['score'], 4)}`")
        else:
            st.error("Failed to fetch results from API")

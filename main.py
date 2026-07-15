from chunking.bm25_store import build_bm25_index
from chunking.chunk_document import chunk_document
from ingestion.load_document import load_document
from chunking.vector_store import store_chunks
from retrieval.fusion import hybrid_query

docs1 = load_document("data/raw/smaple5.md")
docs2 = load_document("data/raw/sample.md")
all_chunks = []
for doc in docs1 :
    chunks = chunk_document(doc)
    all_chunks.extend(chunks)
    store_chunks(chunks)
for doc in docs2 :
    chunks = chunk_document(doc)
    all_chunks.extend(chunks)
    store_chunks(chunks)

build_bm25_index(all_chunks)

res = hybrid_query("What does ERR_CACHE_FULL mean?", top=5)
print(res)


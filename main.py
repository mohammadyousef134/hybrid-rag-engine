from chunking.bm25_store import build_bm25_index
from chunking.chunk_document import chunk_document
from ingestion.load_document import load_document
from chunking.vector_store import store_chunks
from retrieval.fusion import hybrid_query
from chunking.schema.chunk import reset_chunk_counter


all_chunks = []

reset_chunk_counter("data/raw/cloud_computing.md")
docs1 = load_document("data/raw/cloud_computing.md")
for doc in docs1 :
    chunks = chunk_document(doc)
    all_chunks.extend(chunks)
    store_chunks(chunks)

reset_chunk_counter("data/raw/security_basics.md")
docs2 = load_document("data/raw/security_basics.md")
for doc in docs2 :
    chunks = chunk_document(doc)
    all_chunks.extend(chunks)
    store_chunks(chunks)

build_bm25_index(all_chunks)

res = hybrid_query("What is a hypervisor?", top_k=3)
print(res[0])
print(res[1])
print(res[2])
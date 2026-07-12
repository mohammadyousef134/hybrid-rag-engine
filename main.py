from chunking.vector_store import query_chunks

res = query_chunks("what is this document about?", top=3)
for r in res:
    print(r["distance"], r["text"][:80])
from ingestion.load_document import load_document

res = load_document("data/raw/sample.md")
res2 = load_document("data/raw/sample4.txt")

print(res)
print(res2)
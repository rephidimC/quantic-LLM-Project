from pathlib import Path
from seed import set_seed

set_seed(42)

INPUT_DIR = Path("data/processed")
OUTPUT = Path("data/chunks.txt")

CHUNK_SIZE = 500
OVERLAP = 100

def chunk_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        start += size - overlap
    return chunks

def process():
    OUTPUT.write_text("")  # clear old

    for path in INPUT_DIR.glob("*.txt"):
        doc_id = path.name
        content = path.read_text()

        chunks = chunk_text(content)
        with OUTPUT.open("a") as f:
            for i, ch in enumerate(chunks):
                f.write(f"{doc_id}||chunk_{i}||{ch}\n")

        print(f"Chunked {doc_id}: {len(chunks)} chunks")

if __name__ == "__main__":
    process()

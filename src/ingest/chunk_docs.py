from pathlib import Path
from seed import set_seed
import re

set_seed(42)

INPUT_DIR = Path("data/processed")
OUTPUT = Path("data/chunks.txt")

CHUNK_SIZE = 500
OVERLAP = 100

def chunk_text(text, max_size=500):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def clean_chunk(text: str) -> str:
    """
    Ensures each chunk is a single line.
    Removes excessive whitespace and replaces newlines.
    """
    return " ".join(text.split()).strip()


def process():
    OUTPUT.write_text("")  # clear old file

    for path in INPUT_DIR.glob("*.txt"):
        doc_id = path.name
        content = path.read_text()

        chunks = chunk_text(content)

        with OUTPUT.open("a") as f:
            for i, ch in enumerate(chunks):
                cleaned = clean_chunk(ch)
                if not cleaned:
                    continue
                f.write(f"{doc_id}||chunk_{i}||{cleaned}\n")

        print(f"Chunked {doc_id}: {len(chunks)} chunks")


if __name__ == "__main__":
    process()
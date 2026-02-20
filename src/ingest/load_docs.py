import os
import glob
from pypdf import PdfReader
from bs4 import BeautifulSoup
import markdown
from pathlib import Path
from src.utils import load_documents
from src.ingest.chunk_docs import chunk_text

DATA_DIR = Path("data/corpus")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() for page in reader.pages)

def load_md(path):
    html = markdown.markdown(Path(path).read_text())
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n")

def load_html(path):
    soup = BeautifulSoup(Path(path).read_text(), "html.parser")
    return soup.get_text("\n")

def load_txt(path):
    return Path(path).read_text()

def load_all():
    docs = {}
    for file in glob.glob(str(DATA_DIR / "*")):
        ext = file.split(".")[-1].lower()
        name = os.path.basename(file)

        match ext:
            case "pdf":
                text = load_pdf(file)
            case "md":
                text = load_md(file)
            case "html" | "htm":
                text = load_html(file)
            case "txt":
                text = load_txt(file)
            case _:
                print(f"Skipping unknown format: {file}")
                continue

        clean = text.strip()
        out_path = OUTPUT_DIR / f"{name}.txt"
        out_path.write_text(clean)
        docs[name] = clean
        print(f"Loaded & cleaned: {name}")

    return docs

if __name__ == "__main__":
    load_all()

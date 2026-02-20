import os
from pypdf import PdfReader
from bs4 import BeautifulSoup
import markdown

def load_documents(path):
    docs = []

    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if fname.endswith(".txt") or fname.endswith(".md"):
            with open(fpath, "r", encoding="utf-8") as f:
                docs.append(f.read())

        elif fname.endswith(".pdf"):
            reader = PdfReader(fpath)
            text = "\n".join(page.extract_text() for page in reader.pages)
            docs.append(text)

        elif fname.endswith(".html"):
            with open(fpath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                docs.append(soup.get_text())

    return docs

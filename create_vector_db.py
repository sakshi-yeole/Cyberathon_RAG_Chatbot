from pypdf import PdfReader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from sentence_transformers import (
    SentenceTransformer
)

import chromadb


# --------------------------------
# 1. Read PDF
# --------------------------------

pdf_path = "data/cyberathon.pdf"

reader = PdfReader(pdf_path)

text = ""


for page in reader.pages:

    page_text = page.extract_text()

    if page_text:

        text += page_text + "\n"


print("PDF text extracted.")


# --------------------------------
# 2. Split Text
# --------------------------------

splitter = RecursiveCharacterTextSplitter(

    chunk_size=700,

    chunk_overlap=150
)


chunks = splitter.split_text(text)


print(
    "Total chunks:",
    len(chunks)
)


# --------------------------------
# 3. SBERT Embeddings
# --------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


embeddings = embedding_model.encode(
    chunks,

    show_progress_bar=True
)


print(
    "Embeddings created."
)


# --------------------------------
# 4. ChromaDB
# --------------------------------

client = chromadb.PersistentClient(
    path="vector_db"
)


# --------------------------------
# Delete Old Collection
# --------------------------------

try:

    client.delete_collection(
        name="cyberathon"
    )

    print(
        "Old collection deleted."
    )

except Exception:

    print(
        "No old collection found."
    )


# --------------------------------
# Create New Collection
# --------------------------------

collection = client.create_collection(
    name="cyberathon"
)


# --------------------------------
# 5. Store Data
# --------------------------------

collection.add(

    documents=chunks,

    embeddings=embeddings.tolist(),

    ids=[
        f"chunk_{i}"
        for i in range(len(chunks))
    ]
)


print(
    "Data stored in ChromaDB!"
)

print(
    "Total documents:",
    collection.count()
)
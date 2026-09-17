from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. Load Markdown documents
docs_path = Path("../docs")

documents = []

for file_path in docs_path.glob("*.md"):
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents.extend(loader.load())

print(f"Loaded {len(documents)} documents")


# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


# 3. Local embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 4. PostgreSQL + pgvector connection
connection = (
    "postgresql+psycopg://postgres:postgres"
    "@localhost:5433/incident_ai"
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="incident_documents",
    connection=connection,
    use_jsonb=True,
)


# 5. Store chunks + embeddings
vector_store.add_documents(chunks)

print("Documents successfully stored in pgvector!")
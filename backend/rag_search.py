from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector


# Local embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Connect to the existing vector store
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


# Search for semantically similar chunks
query = "Why is payment service latency high?"

results = vector_store.similarity_search(
    query,
    k=3,
)


print("\nRetrieved documents:\n")

for i, document in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print("Source:", document.metadata.get("source"))
    print(document.page_content)
    print()
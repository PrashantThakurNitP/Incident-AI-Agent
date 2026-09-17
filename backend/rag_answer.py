from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_postgres import PGVector


# 1. Local embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 2. Connect to PostgreSQL + pgvector
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


# 3. Local LLM
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# 4. User question
query = "Why is payment service latency high?"


# 5. Retrieve relevant documents
results = vector_store.similarity_search(
    query,
    k=3,
)


# 6. Build context
context = "\n\n".join(
    document.page_content
    for document in results
)


# 7. Create prompt
prompt = f"""
You are an incident investigation assistant.

Answer the user's question using ONLY the provided documentation.

If the documentation does not contain enough information,
say that there is not enough information.

User question:
{query}

Documentation:
{context}

Provide a concise explanation and mention the relevant source documents.
"""


# 8. Generate answer
response = llm.invoke(prompt)

print("\nAnswer:\n")
print(response.content)
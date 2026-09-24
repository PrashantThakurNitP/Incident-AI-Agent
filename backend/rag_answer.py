from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_postgres import PGVector

# This was our first RAG + LLM experiment.

# Flow:

# Question
#    ↓
# Vector search
#    ↓
# Relevant documents
#    ↓
# Llama 3.2
#    ↓
# Answer
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


# Llama 3.2 is an open-source model collection released by Meta that introduces lightweight text models and multimodal vision models.
# ## Key Model Sizes

# * 1B and 3B Models: Lightweight, text-in/text-out models designed to run locally on mobile and edge devices. They support a 128K context window and handle tasks like summarization and rewriting. [1, 4] 
# * 11B and 90B Models: Multimodal vision-enabled models that process both images and text inputs. They support tasks like image captioning and visual reasoning. [5, 6, 7] 

from langchain_ollama import OllamaEmbeddings


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

text = "Payment service Redis connection pool is exhausted."

vector = embeddings.embed_query(text)

print("Embedding dimensions:", len(vector))
print("First 5 values:", vector[:5])
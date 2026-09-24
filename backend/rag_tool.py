from langchain_core.tools import StructuredTool
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

# It converts RAG into a LangChain tool.
# This is what allows the LLM/agent to treat RAG as one of its capabilities.
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

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


def search_incident_knowledge(query: str) -> list[dict]:
    """
    Search historical incidents, runbooks, and architecture
    documentation for information relevant to an incident.
    """

    results = vector_store.similarity_search(
        query,
        k=2,
    )

    return [
    {
        "evidence_type": "HISTORICAL_DOCUMENTATION",
        "source": document.metadata.get("source"),
        "content": document.page_content,
        "usage": (
            "Historical reference only. "
            "Do not treat this information as current operational evidence."
        ),
    }
    for document in results
]


rag_tool = StructuredTool.from_function(
    func=search_incident_knowledge,
    name="search_incident_knowledge",
    description=(
        "Search historical incidents, runbooks, architecture "
        "documentation, and operational knowledge. "
        "Use this tool when you need historical context, "
        "known thresholds, expected configurations, or "
        "previous incidents related to the current problem."
    ),
)


# Instead of manually doing:

# search()

# we expose:

# search_incident_knowledge

# as a tool.

# Conceptually:

# LangChain Agent
#        │
#        ▼
# search_incident_knowledge()
#        │
#        ▼
# PGVector
#        │
#        ▼
# Historical documents
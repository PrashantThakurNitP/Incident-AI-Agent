from langchain_ollama import ChatOllama
from langchain.tools import tool

# This proved that your local 3B model supports structured tool calling.

# That's important because the final system is agentic.
@tool
def get_service_metrics(service_name: str) -> dict:
    """Get current operational metrics for a service."""

    if service_name == "payment-service":
        return {
            "service": "payment-service",
            "p95_latency_ms": 2800,
            "error_rate_percent": 4.2,
            "cpu_percent": 72,
            "redis_connections": 19,
            "redis_pool_size": 20,
        }

    return {
        "service": service_name,
        "p95_latency_ms": 300,
        "error_rate_percent": 0.1,
    }


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

llm_with_tools = llm.bind_tools(
    [get_service_metrics]
)


response = llm_with_tools.invoke(
    "Investigate payment-service. What are its current metrics?"
)

print("Response:")
print(response)

print("\nTool calls:")
print(response.tool_calls)
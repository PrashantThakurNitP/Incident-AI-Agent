import asyncio
import json
import sys
from pathlib import Path

from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# The bridge converts the MCP tools into LangChain-compatible tools.
SERVER_PATH = Path(__file__).parent / "server.py"


async def call_mcp_tool(tool_name: str, service_name: str) -> dict:
    """
    Connect to the MCP server and execute one MCP tool.
    """

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments={
                    "service_name": service_name
                },
            )

            if result.is_error:
                raise RuntimeError(
                    f"MCP tool failed: {tool_name}"
                )

            # MCP returns the JSON result inside TextContent
            text = result.content[0].text

            return json.loads(text)


def get_service_metrics(service_name: str) -> dict:
    """Get current operational metrics for a service."""
    return asyncio.run(
        call_mcp_tool(
            "get_service_metrics",
            service_name,
        )
    )


def get_service_logs(service_name: str) -> dict:
    """Get recent logs for a service."""
    return asyncio.run(
        call_mcp_tool(
            "get_service_logs",
            service_name,
        )
    )


def get_deployment_status(service_name: str) -> dict:
    """Get the current deployment status and version of a service."""
    return asyncio.run(
        call_mcp_tool(
            "get_deployment_status",
            service_name,
        )
    )


def get_database_stats(service_name: str) -> dict:
    """Get current database health and performance statistics."""
    return asyncio.run(
        call_mcp_tool(
            "get_database_stats",
            service_name,
        )
    )


metrics_tool = StructuredTool.from_function(
    func=get_service_metrics,
    name="get_service_metrics",
    description="Get current operational metrics for a service.",
)

logs_tool = StructuredTool.from_function(
    func=get_service_logs,
    name="get_service_logs",
    description="Get recent logs for a service.",
)

deployment_tool = StructuredTool.from_function(
    func=get_deployment_status,
    name="get_deployment_status",
    description=(
        "Get CURRENT deployment information for a service, including "
        "version, previous version, deployment time, deployment status, "
        "and reported deployment changes. Use this to determine whether "
        "a recent deployment is relevant to the current incident."
    ),
)

database_tool = StructuredTool.from_function(
    func=get_database_stats,
    name="get_database_stats",
    description="Get current database health and performance statistics.",
)


mcp_tools = [
    metrics_tool,
    logs_tool,
    deployment_tool,
    database_tool,
]


if __name__ == "__main__":

    print("Available LangChain tools:")

    for tool in mcp_tools:
        print(f"- {tool.name}: {tool.description}")

    print("\nTesting MCP → LangChain bridge...\n")

    result = metrics_tool.invoke(
        {
            "service_name": "payment-service"
        }
    )

    print("Metrics result:")
    print(result)
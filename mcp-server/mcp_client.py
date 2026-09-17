import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = Path(__file__).parent / "server.py"


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("Connected to MCP server")

            tools_result = await session.list_tools()

            print("\nAvailable tools:")

            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            metrics_result = await session.call_tool(
                "get_service_metrics",
                arguments={
                    "service_name": "payment-service"
                },
            )

            logs_result = await session.call_tool(
                "get_service_logs",
                arguments={
                    "service_name": "payment-service"
                },
            )

            print("\nMetrics result:")
            print(metrics_result)

            print("\nLogs result:")
            print(logs_result)
            deployment_result = await session.call_tool(
                "get_deployment_status",
                arguments={
                    "service_name": "payment-service"
                },
            )
            print("\nDeployment result:")
            print(deployment_result)
            
            database_result = await session.call_tool(
                "get_database_stats",
                arguments={
                    "service_name": "payment-service"
                },
            )
            
            print("\nDatabase result:")
            print(database_result)


if __name__ == "__main__":
    asyncio.run(main())
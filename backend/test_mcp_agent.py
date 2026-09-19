import sys
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage

# Allow Python to import files from mcp-server
MCP_SERVER_PATH = Path(__file__).parent.parent / "mcp-server"
sys.path.append(str(MCP_SERVER_PATH))

from mcp_langchain_bridge import mcp_tools


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

llm_with_tools = llm.bind_tools(mcp_tools)


messages = [
    (
        "user",
        """
        Investigate why payment-service latency is high.

        Use the available operational tools to:
        1. Check current service metrics.
        2. Check recent service logs.
        3. Check deployment status.
        4. Check database health.

        Correlate the evidence before providing your conclusion.
        """,
    )
]


while True:

    response = llm_with_tools.invoke(messages)

    print("\nLLM response:")
    print(response)

    # Add the LLM response to the conversation
    messages.append(response)

    # If the LLM does not request any tools,
    # it has produced the final answer.
    if not response.tool_calls:
        break

    print("\nTool calls:")

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"\nExecuting: {tool_name}")
        print(f"Arguments: {tool_args}")

        selected_tool = next(
            tool
            for tool in mcp_tools
            if tool.name == tool_name
        )

        tool_result = selected_tool.invoke(tool_args)

        print("Result:")
        print(tool_result)

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"],
            )
        )


print("\n==============================")
print("FINAL INVESTIGATION")
print("==============================")

print(response.content)
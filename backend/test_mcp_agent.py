import sys
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage

# Allow Python to import files from mcp-server
MCP_SERVER_PATH = Path(__file__).parent.parent / "mcp-server"
sys.path.append(str(MCP_SERVER_PATH))

from mcp_langchain_bridge import mcp_tools
from rag_tool import rag_tool


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

all_tools = mcp_tools + [rag_tool]

llm_with_tools = llm.bind_tools(all_tools)


messages = [
    (
        "user",
        """
        Investigate why payment-service latency is high.

        IMPORTANT:
        - MCP tools provide CURRENT operational evidence.
        - The RAG tool provides HISTORICAL documentation.
        - Never treat historical incident data as current data.
        - Use historical incidents only to compare patterns.
        - Do not claim that something happened currently unless
          a CURRENT MCP tool explicitly reports it.
        - Do not combine facts from different historical incidents.
        - A historical incident can support a hypothesis, but it
          cannot prove that the same event happened now.

        Use the available tools to:
        1. Check current service metrics.
        2. Check current service logs.
        3. Check current deployment status.
        4. Check current database health.
        5. Search historical incidents and runbooks.

        Correlate current evidence with historical patterns.

        Final response must clearly distinguish:
        - Current evidence
        - Historical evidence
        - Most likely cause
        - Evidence supporting the cause
        - Evidence that argues against other causes
        """
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
            for tool in all_tools
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
    print("\nAll tool results added. Calling LLM again...")


print("\n==============================")
print("FINAL INVESTIGATION")
print("==============================")

print(response.content)
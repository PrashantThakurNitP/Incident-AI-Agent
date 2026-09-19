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
        Investigate the payment-service.

        Start by checking the current service metrics.
        """,
    )
]


# Step 1: Ask the LLM what tool it wants to use
response = llm_with_tools.invoke(messages)

print("Initial LLM response:")
print(response)

print("\nTool calls:")
print(response.tool_calls)


# Step 2: Execute the requested tool
if response.tool_calls:

    tool_call = response.tool_calls[0]

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print("\nExecuting tool:")
    print(tool_name)
    print(tool_args)

    selected_tool = next(
        tool
        for tool in mcp_tools
        if tool.name == tool_name
    )

    tool_result = selected_tool.invoke(tool_args)

    print("\nTool result:")
    print(tool_result)


    # Step 3: Give the tool result back to the LLM
    messages.append(response)

    messages.append(
        ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"],
        )
    )

    final_response = llm.invoke(messages)

    print("\nFinal LLM response:")
    print(final_response.content)
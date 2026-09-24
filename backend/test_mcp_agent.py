import json
import sys
from pathlib import Path
    #                      test_mcp_agent.py
    #                             │
    #           ┌─────────────────┴─────────────────┐
    #           │                                   │
    #           ▼                                   ▼
    #      MCP evidence                         RAG evidence
    #           │                                   │
    #           ▼                                   ▼
    #   Current operations                    Historical knowledge
    #           │                                   │
    #           └─────────────────┬─────────────────┘
    #                             ▼
    #                       Llama 3.2
    #                             │
    #                             ▼
    #                    Incident investigation
from langchain_ollama import ChatOllama


# Add mcp-server directory to Python path
MCP_SERVER_PATH = Path(__file__).parent.parent / "mcp-server"
sys.path.append(str(MCP_SERVER_PATH))

from mcp_langchain_bridge import mcp_tools
from rag_tool import rag_tool

# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)


# ---------------------------------------------------------
# Incident
# ---------------------------------------------------------

service_name = "payment-service"

print("\n==============================")
print("INCIDENT INVESTIGATION")
print("==============================")

print(f"\nService: {service_name}")
print("Problem: High payment-service latency")


# ---------------------------------------------------------
# STEP 1: Collect CURRENT operational evidence from MCP
# ---------------------------------------------------------

print("\n==============================")
print("COLLECTING CURRENT EVIDENCE")
print("==============================")

current_evidence = {}

for tool in mcp_tools:
    print(f"\nExecuting: {tool.name}")

    result = tool.invoke(
        {
            "service_name": service_name
        }
    )

    print("Result:")
    print(result)

    current_evidence[tool.name] = result


# ---------------------------------------------------------
# STEP 2: Search HISTORICAL knowledge using RAG
# ---------------------------------------------------------

print("\n==============================")
print("SEARCHING HISTORICAL KNOWLEDGE")
print("==============================")

rag_result = rag_tool.invoke(
    {
        "query": (
            "payment-service high latency Redis connection pool "
            "timeouts failures slow requests"
        )
    }
)

print("\nHistorical evidence:")
print(rag_result)


# ---------------------------------------------------------
# STEP 3: Prepare evidence for the LLM
# ---------------------------------------------------------

current_evidence_json = json.dumps(
    current_evidence,
    indent=2,
)

historical_evidence_json = json.dumps(
    rag_result,
    indent=2,
)


# ---------------------------------------------------------
# STEP 4: Ask LLM to correlate evidence
# ---------------------------------------------------------

print("\n==============================")
print("ANALYZING EVIDENCE")
print("==============================")

prompt = f"""
You are an incident investigation assistant.

Investigate the following production issue:

Service:
{service_name}

Problem:
Payment-service latency is high.

You have two different types of evidence.

==================================================
CURRENT OPERATIONAL EVIDENCE
==================================================

The following data came directly from current MCP
operational tools:

{current_evidence_json}

IMPORTANT:
This is the ONLY source of current operational facts.

==================================================
HISTORICAL DOCUMENTATION
==================================================

The following information came from the RAG system:

{historical_evidence_json}

IMPORTANT:
This is historical documentation and runbooks.

Historical information must NOT be presented as something
that is currently happening.

==================================================
INVESTIGATION RULES
==================================================

1. Clearly separate current evidence from historical evidence.

2. Never claim that a historical incident happened again.

3. Never use historical metrics as current metrics.

4. Use historical incidents only to identify similar patterns.

5. Do not invent thresholds, configurations, failures,
   deployments, database problems, or infrastructure issues
   that are not present in the provided evidence.

6. If a current MCP tool does not show a problem, explicitly
   mention that this evidence argues against that hypothesis.

7. A recent deployment does not automatically mean that the
   deployment caused the incident.

8. Do not assume CPU at 72% means CPU saturation unless the
   evidence explicitly supports that conclusion.

9. Use the current Redis connection count and pool size as
   current facts.

10. Calculate Redis pool utilization when useful. For example,
    19 connections out of a pool of 20 means 95% utilization.

11. If current logs explicitly report Redis connection pool
    exhaustion, Redis connection acquisition timeout, or
    requests waiting for Redis connections, treat those as
    strong CURRENT evidence that Redis is contributing to
    the latency.

12. Do NOT infer that the recent deployment changed the Redis
    connection pool unless the CURRENT deployment evidence
    explicitly says that Redis configuration was changed.

13. Incident 101 describes a historical configuration change
    from 50 to 20 connections. Do not claim that the same
    configuration change happened in the current incident.

14. The current deployment can be described as recent, but
    its causal relationship to the incident is unconfirmed.

15. The final conclusion must be based primarily on CURRENT
    operational evidence. Historical evidence can strengthen
    a hypothesis but cannot prove the current root cause.

==================================================
FINAL RESPONSE FORMAT
==================================================

Provide the investigation using exactly these sections:

1. Current Evidence

List the important facts from the MCP tools.

2. Historical Evidence

List the relevant information from RAG and clearly identify
it as historical.

3. Most Likely Cause

Explain the most likely cause based on the current evidence.

Distinguish between:
- evidence that directly demonstrates the problem,
- evidence that supports a hypothesis,
- and facts that remain unconfirmed.

Do not claim a specific configuration change or deployment
caused the problem unless current evidence explicitly
establishes it.

4. Evidence Supporting the Cause

Explain which current observations support the hypothesis.

5. Evidence Against Other Causes

Discuss database, CPU, and deployment-related hypotheses
only using the provided current evidence.

6. Recommended Next Investigation

Give the next operational checks that an engineer should
perform to confirm the cause.

Be precise and do not invent facts.
"""

response = llm.invoke(prompt)


# ---------------------------------------------------------
# STEP 5: Final investigation
# ---------------------------------------------------------

print("\n==============================")
print("FINAL INVESTIGATION")
print("==============================")

print(response.content)
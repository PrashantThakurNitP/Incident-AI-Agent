import json
import sys
from pathlib import Path

from langchain_ollama import ChatOllama
from pydantic import BaseModel


# ---------------------------------------------------------
# MCP SERVER PATH
# ---------------------------------------------------------

MCP_SERVER_PATH = Path(__file__).parent.parent / "mcp-server"

if str(MCP_SERVER_PATH) not in sys.path:
    sys.path.append(str(MCP_SERVER_PATH))


# ---------------------------------------------------------
# INCIDENT REPORT MODEL
# ---------------------------------------------------------

class IncidentReport(BaseModel):
    service: str
    problem: str
    current_evidence: list[str]
    historical_evidence: list[str]
    most_likely_cause: str
    supporting_evidence: list[str]
    evidence_against_other_causes: list[str]
    recommended_next_investigation: list[str]


# ---------------------------------------------------------
# PROJECT IMPORTS
# ---------------------------------------------------------

from mcp_langchain_bridge import mcp_tools
from rag_tool import rag_tool


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    format="json",
)


# ---------------------------------------------------------
# INCIDENT INVESTIGATION
# ---------------------------------------------------------

def investigate_incident(
    service_name: str,
    problem: str,
) -> IncidentReport:

    # -----------------------------------------------------
    # 1. Collect CURRENT operational evidence
    # -----------------------------------------------------

    current_evidence_raw = {}

    for tool in mcp_tools:

        result = tool.invoke(
            {
                "service_name": service_name
            }
        )

        current_evidence_raw[tool.name] = result

    current_metrics = current_evidence_raw["get_service_metrics"]
    current_logs = current_evidence_raw["get_service_logs"]
    current_deployment = current_evidence_raw["get_deployment_status"]
    current_database = current_evidence_raw["get_database_stats"]

    current_evidence = [
        f"P95 latency: {current_metrics['p95_latency_ms']} ms",
        f"Error rate: {current_metrics['error_rate_percent']}%",
        f"CPU utilization: {current_metrics['cpu_percent']}%",
        (
            f"Redis active connections: "
            f"{current_metrics['redis_connections']}"
        ),
        (
            f"Redis pool size: "
            f"{current_metrics['redis_pool_size']}"
        ),
    ]

    # -----------------------------------------------------
    # CURRENT LOG EVIDENCE
    # -----------------------------------------------------

    for log in current_logs["logs"]:
        current_evidence.append(
            f"Current log: {log}"
        )

    # -----------------------------------------------------
    # CURRENT DEPLOYMENT EVIDENCE
    # -----------------------------------------------------

    current_evidence.append(
        f"Deployment version: {current_deployment['version']}"
    )

    current_evidence.append(
        f"Deployment status: {current_deployment['status']}"
    )

    current_evidence.append(
        f"Deployment time: {current_deployment['deployed_at']}"
    )

    current_evidence.append(
        f"Previous deployment version: "
        f"{current_deployment['previous_version']}"
    )

    current_evidence.append(
        f"Reported deployment change: "
        f"{current_deployment['deployment_change']}"
    )

    # -----------------------------------------------------
    # CURRENT DATABASE EVIDENCE
    # -----------------------------------------------------

    current_evidence.append(
        f"Database status: {current_database['status']}"
    )

    current_evidence.append(
        f"Database active connections: "
        f"{current_database['connection_pool_active']}/"
        f"{current_database['connection_pool_max']}"
    )

    current_evidence.append(
        f"Database slow queries: "
        f"{current_database['slow_queries']}"
    )

    current_evidence.append(
        f"Database average query latency: "
        f"{current_database['average_query_latency_ms']} ms"
    )

    # -----------------------------------------------------
    # 2. Search HISTORICAL knowledge
    # -----------------------------------------------------

    rag_result = rag_tool.invoke(
        {
            "query": (
                f"{service_name} {problem} "
                "latency Redis connection pool "
                "timeouts failures"
            )
        }
    )

    historical_evidence = [
        (
            f"Historical source: {item.get('source')}\n"
            f"{item.get('content')}"
        )
        for item in rag_result
    ]

    # -----------------------------------------------------
    # 3. Convert evidence to JSON
    # -----------------------------------------------------

    current_evidence_json = json.dumps(
        current_evidence,
        indent=2,
    )

    historical_evidence_json = json.dumps(
        historical_evidence,
        indent=2,
    )

    # -----------------------------------------------------
    # 4. Build investigation prompt
    # -----------------------------------------------------

    prompt = f"""
You are an incident investigation assistant.

Investigate the following production issue.

Service:
{service_name}

Problem:
{problem}

==================================================
CURRENT OPERATIONAL EVIDENCE
==================================================

The following information came directly from
CURRENT MCP operational tools:

{current_evidence_json}

This is the ONLY source of current operational facts.

==================================================
HISTORICAL DOCUMENTATION
==================================================

The following information came from the RAG system:

{historical_evidence_json}

This information is HISTORICAL documentation.

Historical information must NOT be presented as
something that is currently happening.

==================================================
INVESTIGATION RULES
==================================================

1. Clearly separate CURRENT evidence from HISTORICAL evidence.

2. current_evidence must contain ONLY facts explicitly present
   in the CURRENT OPERATIONAL EVIDENCE section.

3. historical_evidence must contain ONLY information explicitly
   present in the HISTORICAL DOCUMENTATION section.

4. NEVER copy a value, event, resolution, configuration change,
   or outcome from HISTORICAL DOCUMENTATION into current_evidence.

5. Never use historical metrics as current metrics.

6. Never claim that a historical incident happened again.

7. Historical incidents may ONLY be used to identify similar
   patterns or provide contextual information.

8. Historical evidence can strengthen a hypothesis but cannot
   prove the current root cause.

9. The final conclusion must be based primarily on CURRENT
   operational evidence.

10. Do not invent thresholds, configurations, failures,
    deployments, database problems, infrastructure issues,
    resolutions, or outcomes that are not present in the
    provided evidence.

11. If current MCP evidence does not support a hypothesis,
    explain that the available evidence does not currently
    support that hypothesis. Do not claim that the hypothesis
    has been disproven unless the evidence establishes that.

12. A recent deployment does NOT automatically mean that the
    deployment caused the incident.

13. Do NOT infer that the recent deployment changed Redis
    configuration unless the CURRENT deployment evidence
    explicitly says so.

14. Do not assume CPU at 72% means CPU saturation unless
    the evidence explicitly supports that conclusion.

15. Calculate resource utilization when useful, but clearly
    distinguish calculated values from directly reported values.

16. If current logs explicitly report Redis connection pool
    exhaustion, Redis connection acquisition timeout, or
    requests waiting for Redis connections, treat these as
    strong CURRENT evidence that Redis is contributing
    to the latency.

17. The current Redis pool size must be taken from the CURRENT
    MCP metrics. Do not replace it with a value from historical
    documentation.

18. If historical documentation says that the Redis pool was
    changed from 20 to 50, that event belongs ONLY to
    historical_evidence.

19. Do NOT say that Redis timeouts disappeared, latency recovered,
    the pool was increased, or the incident was resolved unless
    the CURRENT MCP evidence explicitly contains that information.

20. Historical Incident 101 describes a PREVIOUS incident.
    It must never be described as the resolution or outcome
    of the CURRENT incident.

21. Every statement in current_evidence must be directly
    traceable to the CURRENT OPERATIONAL EVIDENCE.

22. Every statement in historical_evidence must be directly
    traceable to the HISTORICAL DOCUMENTATION.

23. Clearly distinguish:
    - directly observed current evidence,
    - historical context,
    - hypotheses,
    - unconfirmed information.

24. Do not present a hypothesis as a confirmed root cause
    unless the current evidence directly establishes it.

25. Supporting evidence must directly support the stated hypothesis.
    Do not include unrelated current metrics merely because they
    are available.

26. Do not state or imply increased traffic, traffic spikes,
    request volume increases, concurrency changes, or increased
    load unless current evidence explicitly contains such information.

27. If the current evidence shows Redis pool exhaustion,
    Redis connection acquisition timeouts, and requests waiting
    for Redis connections, these are sufficient to identify
    Redis connection pool pressure as the most likely contributor
    to the current latency.

28. When recommending a configuration change, first recommend
    validating the relevant configuration, pool utilization,
    connection wait time, traffic/concurrency, and recent
    configuration changes. Do not assume that increasing the
    pool size is required based only on historical documentation.
29. Do not recommend changing a current configuration to a specific
    value based only on historical documentation.

30. If historical documentation contains a configuration value,
    treat that value as historical context only unless the current
    operational evidence confirms that the same value is currently
    required.

31. Do not describe a metric as "normal", "healthy", "within normal
    range", or "within acceptable limits" unless the current evidence
    explicitly provides the relevant threshold or status.

32. When current evidence does not indicate a problem with a component,
    say that the available current evidence does not indicate a problem
    with that component rather than claiming the component is definitively
    not responsible.

==================================================
IMPORTANT EVIDENCE PROVENANCE
==================================================

CURRENT evidence means information obtained from MCP tools
during this investigation.

HISTORICAL evidence means information retrieved from RAG.

For example:

If CURRENT MCP evidence says:
"Redis connections = 19"

and historical documentation says:
"Redis pool was increased from 20 to 50"

then:

CURRENT:
"19 Redis connections are currently active."

HISTORICAL:
"A previous incident involved changing the Redis pool
from 50 to 20 connections."

NEVER combine these into:
"Redis was increased from 20 to 50."

That would incorrectly mix current and historical evidence.

==================================================
FINAL RESPONSE FORMAT
==================================================

Return ONLY valid JSON.

Do not include markdown.
Do not include ```json.

The JSON must have exactly these fields:

{{
  "most_likely_cause": "explanation based primarily on current evidence",
  "supporting_evidence": [
    "current evidence supporting the hypothesis"
  ],
  "evidence_against_other_causes": [
    "current evidence arguing against alternative hypotheses"
  ],
  "recommended_next_investigation": [
    "next operational check required to confirm or reject the hypothesis"
  ]
}}

The application will provide current_evidence and
historical_evidence separately.

DO NOT generate or modify those evidence sections.

Your responsibility is ONLY to reason about the
provided evidence.

Never convert historical information into current facts.

Do not claim that a historical configuration change,
historical resolution, or historical outcome happened
during the current incident.

Do not claim that a deployment caused the incident unless
the current MCP evidence explicitly establishes that.

Distinguish confirmed evidence from hypotheses.

==================================================
FINAL VALIDATION BEFORE RESPONDING
==================================================

Before returning the JSON, verify:

- current_evidence contains NO historical facts.
- historical_evidence contains NO current MCP facts presented
  as if they came from RAG.
- No historical resolution is presented as a current resolution.
- No deployment causality is inferred without current evidence.
- No database problem is claimed without current database evidence.
- No CPU saturation is claimed without supporting evidence.
- The most_likely_cause is explicitly supported by current evidence.
- Unconfirmed hypotheses are described as hypotheses.
- The response contains ONLY valid JSON.
"""

    # -----------------------------------------------------
    # 5. LLM analysis
    # -----------------------------------------------------

    response = llm.invoke(prompt)

    analysis = json.loads(response.content)

    # -----------------------------------------------------
    # 6. Build structured incident report
    # -----------------------------------------------------

    return IncidentReport(
        service=service_name,
        problem=problem,
        current_evidence=current_evidence,
        historical_evidence=historical_evidence,
        most_likely_cause=analysis["most_likely_cause"],
        supporting_evidence=analysis["supporting_evidence"],
        evidence_against_other_causes=analysis[
            "evidence_against_other_causes"
        ],
        recommended_next_investigation=analysis[
            "recommended_next_investigation"
        ],
    )
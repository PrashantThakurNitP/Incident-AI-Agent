from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import CORS_ORIGINS
from incident_agent import investigate_incident


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="Incident Investigation AI Agent",
    description=(
        "AI-powered incident investigation using "
        "RAG, MCP, LangChain, and a local LLM."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentRequest(BaseModel):
    service_name: str
    problem: str


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "incident-investigation-ai-agent",
    }


# ---------------------------------------------------------
# INCIDENT INVESTIGATION
# ---------------------------------------------------------

@app.post("/api/incidents/investigate")
def investigate(request: IncidentRequest):

    if request.service_name != "payment-service":
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported service: {request.service_name}. "
                "Currently supported service: payment-service"
            ),
        )

    if not request.problem.strip():
        raise HTTPException(
            status_code=400,
            detail="Problem description cannot be empty.",
        )

    report = investigate_incident(
        service_name=request.service_name,
        problem=request.problem,
    )

    return report.model_dump()
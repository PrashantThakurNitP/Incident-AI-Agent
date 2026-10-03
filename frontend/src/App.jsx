import { useState } from "react";
import "./index.css";

import { investigateIncident } from "./api/incidentApi";

import IncidentForm from "./components/IncidentForm";
import MostLikelyCause from "./components/MostLikelyCause";
import CurrentEvidence from "./components/CurrentEvidence";
import EvidenceList from "./components/EvidenceList";
import HistoricalEvidence from "./components/HistoricalEvidence";
import RecommendedInvestigation from "./components/RecommendedInvestigation";
import SupportingEvidence from "./components/SupportingEvidence";

function App() {
  const [serviceName, setServiceName] = useState("payment-service");
  const [problem, setProblem] = useState("High payment-service latency");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleInvestigate = async () => {
    if (!problem.trim()) {
      setError("Please describe the incident.");
      return;
    }

    setLoading(true);
    setError("");
    setReport(null);

    try {
      const data = await investigateIncident(
        serviceName,
        problem.trim()
      );

      setReport(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the incident investigation backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Incident Investigation AI</h1>

          <p>
            AI-powered incident analysis using RAG, MCP, LangChain
            and a local LLM
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Local AI
        </div>
      </header>

      <main className="container">
        <IncidentForm
          serviceName={serviceName}
          problem={problem}
          loading={loading}
          error={error}
          onServiceChange={setServiceName}
          onProblemChange={setProblem}
          onInvestigate={handleInvestigate}
        />

        {loading && (
          <section className="loading-card">
            <div className="spinner"></div>

            <div>
              <strong>Investigating incident...</strong>

              <p>
                Collecting MCP operational evidence and searching
                historical knowledge.
              </p>
            </div>
          </section>
        )}

        {report && !loading && (
          <>
            <MostLikelyCause
              cause={report.most_likely_cause}
            />

            <CurrentEvidence
              evidence={report.current_evidence}
            />

            <SupportingEvidence
               items={report.supporting_evidence}
          />

            <HistoricalEvidence
              evidence={report.historical_evidence}
            />

            <section className="section">
              <div className="section-heading">
                <h2>Evidence Against Other Causes</h2>
              </div>

              <EvidenceList
                items={report.evidence_against_other_causes}
                icon="i"
                iconClass="info"
              />
            </section>

            <RecommendedInvestigation
              items={report.recommended_next_investigation}
            />
          </>
        )}
      </main>

      <footer>
        <span>Incident Investigation AI Agent</span>
        <span>
          LangChain • RAG • MCP • Ollama • pgvector
        </span>
      </footer>
    </div>
  );
}

export default App;

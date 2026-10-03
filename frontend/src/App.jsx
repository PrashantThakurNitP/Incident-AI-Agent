import { useState } from "react";
import "./index.css";
import { investigateIncident } from "./api/incidentApi";

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
        <section className="investigation-card">
          <div className="section-title">
            <div>
              <h2>Investigate Incident</h2>
              <p>
                Combine current operational data with historical
                incident knowledge.
              </p>
            </div>
          </div>

          <div className="form-grid">
            <div className="form-group">
              <label>Service</label>

              <select
                value={serviceName}
                onChange={(e) => setServiceName(e.target.value)}
              >
                <option value="payment-service">
                  payment-service
                </option>
              </select>
            </div>

            <div className="form-group">
              <label>Problem</label>

              <input
                type="text"
                value={problem}
                onChange={(e) => setProblem(e.target.value)}
                placeholder="Describe the incident..."
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleInvestigate();
                  }
                }}
              />
            </div>
          </div>

          <button
            className="investigate-button"
            onClick={handleInvestigate}
            disabled={loading}
          >
            {loading ? "Investigating..." : "Investigate Incident"}
          </button>

          {error && <div className="error">{error}</div>}
        </section>

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
            <section className="cause-card">
              <div className="cause-header">
                <span className="badge">AI ANALYSIS</span>
                <h2>Most Likely Cause</h2>
              </div>

              <p className="cause">
                {report.most_likely_cause}
              </p>
            </section>

            <section className="section">
              <div className="section-heading">
                <h2>Current Operational Evidence</h2>
                <span className="source-badge mcp">MCP</span>
              </div>

              <p className="section-description">
                Evidence collected from current operational tools.
              </p>

              <div className="evidence-grid">
                {report.current_evidence?.map((item, index) => (
                  <div className="evidence-card" key={index}>
                    <span className="evidence-number">
                      {index + 1}
                    </span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </section>

            <section className="section">
              <div className="section-heading">
                <h2>Supporting Evidence</h2>
              </div>

              <div className="list-card">
                {report.supporting_evidence?.map((item, index) => (
                  <div className="list-item" key={index}>
                    <span className="check">✓</span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </section>

            <section className="section">
              <div className="section-heading">
                <h2>Historical Evidence</h2>
                <span className="source-badge rag">RAG</span>
              </div>

              <p className="section-description">
                Historical incidents, runbooks and architecture
                documentation retrieved from pgvector.
              </p>

              <div className="history-list">
                {report.historical_evidence?.map((item, index) => (
                  <details className="history-card" key={index}>
                    <summary>
                      <span>Historical Evidence {index + 1}</span>
                      <span className="expand">+</span>
                    </summary>

                    <pre>{item}</pre>
                  </details>
                ))}
              </div>
            </section>

            <section className="section">
              <div className="section-heading">
                <h2>Evidence Against Other Causes</h2>
              </div>

              <div className="list-card">
                {report.evidence_against_other_causes?.map(
                  (item, index) => (
                    <div className="list-item" key={index}>
                      <span className="info">i</span>
                      <span>{item}</span>
                    </div>
                  )
                )}
              </div>
            </section>

            <section className="recommendation-card">
              <div className="section-heading">
                <h2>Recommended Next Investigation</h2>
              </div>

              <ol>
                {report.recommended_next_investigation?.map(
                  (item, index) => (
                    <li key={index}>{item}</li>
                  )
                )}
              </ol>
            </section>
          </>
        )}
      </main>

      <footer>
        <span>Incident Investigation AI Agent</span>
        <span>LangChain • RAG • MCP • Ollama • pgvector</span>
      </footer>
    </div>
  );
}

export default App;
function HistoricalEvidence({ evidence }) {
  return (
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
        {evidence?.map((item, index) => (
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
  );
}

export default HistoricalEvidence;
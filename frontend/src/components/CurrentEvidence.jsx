function CurrentEvidence({ evidence }) {
  return (
    <section className="section">
      <div className="section-heading">
        <h2>Current Operational Evidence</h2>
        <span className="source-badge mcp">MCP</span>
      </div>

      <p className="section-description">
        Evidence collected from current operational tools.
      </p>

      <div className="evidence-grid">
        {evidence?.map((item, index) => (
          <div className="evidence-card" key={index}>
            <span className="evidence-number">
              {index + 1}
            </span>

            <span>{item}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export default CurrentEvidence;
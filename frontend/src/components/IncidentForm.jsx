
function IncidentForm({
  serviceName,
  problem,
  loading,
  error,
  onServiceChange,
  onProblemChange,
  onInvestigate,
}) {
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      onInvestigate();
    }
  };

  return (
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
          <label htmlFor="service">Service</label>

          <select
            id="service"
            value={serviceName}
            onChange={(event) =>
              onServiceChange(event.target.value)
            }
          >
            <option value="payment-service">
              payment-service
            </option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="problem">Problem</label>

          <input
            id="problem"
            type="text"
            value={problem}
            onChange={(event) =>
              onProblemChange(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Describe the incident..."
          />
        </div>
      </div>

      <button
        className="investigate-button"
        onClick={onInvestigate}
        disabled={loading}
      >
        {loading ? "Investigating..." : "Investigate Incident"}
      </button>

      {error && <div className="error">{error}</div>}
    </section>
  );
}

export default IncidentForm;
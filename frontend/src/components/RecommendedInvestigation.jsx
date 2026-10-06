function RecommendedInvestigation({ items }) {
  return (
    <section className="recommendation-card">
      <div className="section-heading">
        <h2>Recommended Next Investigation</h2>
      </div>

      <ol>
        {items?.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ol>
    </section>
  );
}

export default RecommendedInvestigation;
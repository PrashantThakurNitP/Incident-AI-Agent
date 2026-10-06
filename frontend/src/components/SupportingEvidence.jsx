import EvidenceList from "./EvidenceList";

function SupportingEvidence({ items }) {
  return (
    <section className="section">
      <div className="section-heading">
        <h2>Supporting Evidence</h2>
      </div>

      <EvidenceList items={items} />
    </section>
  );
}

export default SupportingEvidence;
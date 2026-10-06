function EvidenceList({ items, icon = "✓", iconClass = "check" }) {
  return (
    <div className="list-card">
      {items?.map((item, index) => (
        <div className="list-item" key={index}>
          <span className={iconClass}>{icon}</span>
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}

export default EvidenceList;
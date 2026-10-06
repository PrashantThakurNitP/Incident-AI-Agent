function MostLikelyCause ({cause}){
    return ( <section className="cause-card">
      <div className="cause-header">
        <span className="badge">AI ANALYSIS</span>
        <h2>Most Likely Cause</h2>
      </div>

      <p className="cause">{cause}</p>
    </section>
    );
}

export default MostLikelyCause;
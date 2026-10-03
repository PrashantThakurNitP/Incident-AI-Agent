from incident_agent import investigate_incident


result = investigate_incident(
    service_name="payment-service",
    problem="High payment-service latency",
)

print("\n==============================")
print("INCIDENT INVESTIGATION")
print("==============================")

print("\nService:")
print(result.service)

print("\nProblem:")
print(result.problem)

print("\nCurrent Evidence:")
for item in result.current_evidence:
    print(f"- {item}")

print("\nHistorical Evidence:")
for item in result.historical_evidence:
    print(f"- {item}")

print("\nMost Likely Cause:")
print(result.most_likely_cause)

print("\nSupporting Evidence:")
for item in result.supporting_evidence:
    print(f"- {item}")

print("\nEvidence Against Other Causes:")
for item in result.evidence_against_other_causes:
    print(f"- {item}")

print("\nRecommended Next Investigation:")
for item in result.recommended_next_investigation:
    print(f"- {item}")
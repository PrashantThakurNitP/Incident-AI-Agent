const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function investigateIncident(serviceName, problem) {
  const response = await fetch(`${API_BASE_URL}/api/incidents/investigate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      service_name: serviceName,
      problem,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Incident investigation failed.");
  }

  return data;
}

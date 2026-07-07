import { useState, useEffect } from "react";

function App() {
  const [events, setEvents] = useState([]);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/events")
      .then((res) => res.json())
      .then((data) => setEvents(data));
  }, []);

  const [board, setBoard] = useState({});
  useEffect(() => {
    fetch("http://127.0.0.1:8000/board")
      .then((res) => res.json())
      .then((data) => setBoard(data));
  }, []);

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "48px 24px" }}>
      <h1 style={{ fontSize: "42px", marginBottom: "4px" }}>Pipeline</h1>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        {events.length} events in the log
      </p>

      <div style={{ display: "flex", gap: "16px", alignItems: "flex-start" }}>
        {Object.entries(board).map(([stage, apps]) => (
          <div key={stage} style={{ background: "var(--card)", border: "1px solid #E5E1D8", borderRadius: "8px", padding: "16px", minWidth: "200px" }}>
            <h3 style={{ marginTop: 0 }}>{stage}</h3>
            {apps.map((app) => (
              <div key={app.application_id} style={{ padding: "8px", borderTop: "1px solid #E5E1D8", fontSize: "13px" }}>
                <strong style={{ color: "var(--ink)" }}>{app.details.company_name}</strong>
                <div style={{ color: "var(--muted)" }}>{app.details.job_title}</div>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div style={{ marginTop: "32px" }}>
        {events.map((event) => (
          <div key={event.id} style={{ background: "var(--card)", border: "1px solid #E5E1D8", borderRadius: "8px", padding: "16px", marginBottom: "12px" }}>
            <strong>{event.event_type}</strong>
            <span style={{ color: "var(--accent)" }}> → {event.payload.to_stage}</span>
            <div style={{ color: "var(--muted)", fontSize: "14px" }}>{event.source}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
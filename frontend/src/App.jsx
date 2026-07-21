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

  const [company,   setCompany]   = useState("")
  const [title,     setTitle]     = useState("")
  const [foundFrom, setFoundFrom] = useState("")
  const [activeTab, setActiveTab] = useState("board")
  const [funnel, setFunnel] = useState({})
  const [timeInStage, setTimeInStage] = useState([])

    useEffect(() => {
    if (activeTab === "metrics") {
      fetch("http://127.0.0.1:8000/metrics")
        .then((res) => res.json())
        .then((data) => {
          setFunnel(data.funnel)
          setTimeInStage(data.time_in_stage)
        });
    }
  }, [activeTab]);

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "48px 24px" }}>
      <h1 style={{ fontSize: "42px", marginBottom: "4px" }}>Pipeline</h1>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        {events.length} events in the log
      </p>
      <button onClick={() => setActiveTab("board")}>Board</button>
      <button onClick={() => setActiveTab("metrics")}>Metrics</button>
      {activeTab === "board" ? (
      <div>
      <input placeholder="Company" value={company} onChange={e => setCompany(e.target.value)} />
      <input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} />
      <input placeholder="FoundFrom" value={foundFrom} onChange={e => setFoundFrom(e.target.value)} />
      <button onClick={() => {
              const paperwork = {
                application_id: crypto.randomUUID(),
                event_type: "application_created",
                payload: { company_name: company, job_title: title, found_from: foundFrom },
                source: "manual"
              };
              fetch("http://127.0.0.1:8000/events", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(paperwork)
                  }).then(() => {
                        setCompany("")
                        setTitle("")
                        setFoundFrom("")
                        window.location.reload()
                      });
            }}>Add</button>
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
    ) : (
  <div>
  {Object.entries(funnel).map(([stage, count]) => (
    <div key={stage}>
      {stage}: {count}
    </div>
  ))}
</div>
)}
    </div>
  );
}
export default App;
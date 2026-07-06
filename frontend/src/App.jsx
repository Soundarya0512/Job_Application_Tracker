import {useState,useEffect} from "react"

function App(){
  const[events, setEvents]=useState([]);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/events")
      .then((res) => res.json())
      .then((data) => setEvents(data));
  }, []);

  return (
    <div>
      <h1>Pipeline</h1>
      <p>{events.length} events in the log</p>
    </div>
  );
}

export default App;
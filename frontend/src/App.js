import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'plotly.js';
import './App.css';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios('http://localhost:8000/api/equitydata/');
      setData(result.data);
    };

    fetchData();
    const intervalId = setInterval(fetchData, 60000); // Fetch data every 60 seconds (60000 ms)

    return () => clearInterval(intervalId); // Clean up the interval when the component is unmounted
  }, []);

  useEffect(() => {
    if (data.length > 0) {
      const trace1 = {
        x: data.map(d => d.timestamp),
        y: data.map(d => d.equity),
        mode: 'lines',
        name: 'Equity',
      };
      const trace2 = {
        x: data.map(d => d.timestamp),
        y: data.map(d => d.balance),
        mode: 'lines',
        name: 'Balance',
      };
      const layout = {
        title: 'Historical Equity and Balance',
        xaxis: { title: 'Timestamp' },
        yaxis: { title: 'Equity and Balance' },
      };
      const config = { responsive: true };
      Plot.newPlot('equity-chart', [trace1, trace2], layout, config);
    }
  }, [data]);

  return (
    <div className="App">
      <div id="equity-chart"></div>
    </div>
  );
}

export default App;

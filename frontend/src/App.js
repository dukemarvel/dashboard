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
  
    fetchData(); // Fetch the data immediately on component mount
  
    const interval = setInterval(() => {
      fetchData(); // Fetch the data periodically
    }, 5000); // 5 seconds
  
    return () => clearInterval(interval); // Clear the interval on component unmount
  }, []);
  

  useEffect(() => {
    if (data.length > 0) {
      const accountIds = Array.from(new Set(data.map(d => d.account_id)));

      accountIds.forEach(accountId => {
        const accountData = data.filter(d => d.account_id === accountId);

        const trace1 = {
          x: accountData.map(d => d.timestamp),
          y: accountData.map(d => d.equity),
          mode: 'lines',
          name: 'Equity',
        };
        const trace2 = {
          x: accountData.map(d => d.timestamp),
          y: accountData.map(d => d.balance),
          mode: 'lines',
          name: 'Balance',
        };
        const layout = {
          title: `Historical Equity and Balance for Account ${accountId}`,
          xaxis: { title: 'Timestamp' },
          yaxis: { title: 'Equity and Balance' },
        };
        const config = { responsive: true };
        Plot.newPlot(`equity-chart-${accountId}`, [trace1, trace2], layout, config);
      });
    }
  }, [data]);

  return (
    <div className="App">
      {data.length > 0 &&
        Array.from(new Set(data.map(d => d.account_id))).map(accountId => (
          <div key={accountId} id={`equity-chart-${accountId}`}></div>
        ))}
    </div>
  );
}

export default App;

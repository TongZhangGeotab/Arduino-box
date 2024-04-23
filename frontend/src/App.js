import React, { useState, useEffect } from 'react';

function App() {
  const [state, setState] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/state');
        if (response.ok) {
          const data = await response.json();
          setState(data);
        } else {
          console.error('Error fetching state:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching state:', error);
      }
    };

    const intervalId = setInterval(fetchData, 100); // Poll every second

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <h1>State Data</h1>
      <pre>{JSON.stringify(state, null, 2)}</pre>
    </div>
  );
}

export default App;
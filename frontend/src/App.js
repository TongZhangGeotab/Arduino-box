import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import './App.css';

function App() {
  const [state, setState] = useState({
    ignition: 0,
    pos_x: 0,
    pos_y: 0,
    z1: 0,
    v: 0,
    angle: 0,
    bl: 0,
    br: 0,
    hb: 0,
    hz: 0
  });

  useEffect(() => {
    const socket = io('http://localhost:5000');

    socket.on('connect', () => {
      console.log('Connected to the WebSocket server');
    });

    socket.on('state', (data) => {
      setState(data);
      console.log(state)
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from the WebSocket server');
    });

    // Cleanup function to disconnect the WebSocket when the component unmounts
    return () => socket.disconnect();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* ... (your UI elements that display the state) */}
        <p>Ignition: {state.ignition}</p>
        <p>Test: {state.pos_x}</p>
        {/* ... (display other state variables as needed) */}
      </header>
    </div>
  );
}

export default App;

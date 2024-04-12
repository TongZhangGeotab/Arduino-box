// src/Car.js

import React, { useState, useEffect } from 'react';

const Car = () => {
  const [sensors, setSensors] = useState({ x: 0, y: 0, z: 0, time_stamp: 0 });
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const newWs = new WebSocket('ws://localhost:6789');

    newWs.onmessage = (event) => {
      const [x, y, z, time_stamp] = event.data.split(',').map(Number);
      setSensors({ x, y, z, time_stamp });
    };

    setWs(newWs);

    return () => {
      newWs.close();
    };
  }, []);

  // ... rest of your component

  return (
    <div>
      {/* Display sensor data or use it to update a position */}
      <div>X: {sensors.x}</div>
      <div>Y: {sensors.y}</div>
      <div>Z: {sensors.z}</div>
      <div>Timestamp: {sensors.time_stamp}</div>
    </div>
  );
};

export default Car;
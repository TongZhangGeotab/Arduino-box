// src/Car.js

import React, { useState, useEffect } from 'react';

const Car = () => {
  const [sensors, setSensors] = useState({
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
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const newWs = new WebSocket('ws://localhost:6789');

    newWs.onmessage = (event) => {
      // Parse the incoming JSON string
      const parsedMessage = JSON.parse(event.data);
      console.log(parsedMessage);

      // Update the sensors state with the new values
      setSensors(parsedMessage);
    };

    setWs(newWs);

    // Clean up the WebSocket connection when the component unmounts
    return () => {
      newWs.close();
    };
  }, []);

  return (
    <div>
      <div>Ignition: {sensors.ignition}</div>
      <div>Pos X: {sensors.pos_x}</div>
      <div>Pos Y: {sensors.pos_y}</div>
      <div>Z: {sensors.z1}</div>
      <div>BR: {sensors.br}</div>
      <div>BL: {sensors.bl}</div>
      <div>HB: {sensors.hb}</div>
      <div>HZ: {sensors.hz}</div>

    </div>
  );
};

export default Car;
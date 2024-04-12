import React, { useState, useEffect } from 'react';

const Car = () => {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const moveCharacter = (x, y) => {
    setPosition(prevPosition => ({
      x: prevPosition.x + x,
      y: prevPosition.y + y
    }));
  };

  useEffect(() => {
    const handleKeyPress = (event) => {
      switch (event.key) {
        case 'w':
          moveCharacter(0, -5);
          break;
        case 'a':
          moveCharacter(-5, 0);
          break;
        case 's':
          moveCharacter(0, 5);
          break;
        case 'd':
          moveCharacter(5, 0);
          break;
        default:
          break;
      }
    };

    window.addEventListener('keypress', handleKeyPress);

    return () => {
      window.removeEventListener('keypress', handleKeyPress);
    };
  }, []);

  const characterStyle = {
    position: 'absolute',
    top: position.y,
    left: position.x,
    width: '50px',
    height: '50px',
    backgroundColor: 'blue'
  };

  return (
    <div>
      <div style={characterStyle}></div>
    </div>
  );
};

export default Car;
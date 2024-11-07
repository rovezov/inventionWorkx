// src/components/Hardware/HardwareList.js

import React, { useEffect, useState } from 'react';
import { listHardware } from '../../api/hardwareService';

function HardwareList() {
  const [hardware, setHardware] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHardware = async () => {
      try {
        const data = await listHardware();
        setHardware(data);
      } catch (err) {
        console.error("Error fetching hardware:", err);
        setError(err.message || "Failed to load hardware resources");
      }
    };

    fetchHardware();
  }, []);

  return (
    <div>
      <h2>Available Hardware</h2>
      {error && <p>{error}</p>}
      <ul>
        {hardware.map((item, index) => (
          <li key={index}>
            <h3>{item.hardware_name}</h3>
            <p>Total Capacity: {item.capacity}</p>
            <p>Available: {item.availability}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HardwareList;

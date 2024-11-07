// src/pages/Hardware.js

import React, { useEffect, useState } from 'react';
import { listHardware } from '../api/hardwareService';
import HardwareCheckoutForm from '../components/Hardware/HardwareCheckoutForm';
import HardwareCheckinForm from '../components/Hardware/HardwareCheckinForm';
import './Hardware.css';

function Hardware() {
  const [hardware, setHardware] = useState([]);
  const [error, setError] = useState('');

  const fetchHardware = async () => {
    try {
      const data = await listHardware();
      setHardware(data);
    } catch (err) {
      setError(err.message || "Failed to load hardware");
    }
  };

  useEffect(() => {
    fetchHardware();
  }, []);

  return (
    <div>
      <h2>Available Hardware</h2>
      {error && <p>{error}</p>}
      <ul>
        {hardware.map((item) => (
          <li key={item.hardware_name} className="hardware-item">
            <h3>{item.hardware_name}</h3>
            <p><strong>Capacity:</strong> {item.capacity}</p>
            <p><strong>Availability:</strong> {item.availability}</p>
          </li>
        ))}
      </ul>

      {/* Add Checkout and Check-In Forms */}
      <HardwareCheckoutForm onCheckout={fetchHardware} />
      <HardwareCheckinForm onCheckin={fetchHardware} />
    </div>
  );
}

export default Hardware;

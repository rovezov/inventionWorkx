// src/components/Hardware/HardwareCheckinForm.js

import React, { useState } from 'react';
import { checkinHardware } from '../../api/hardwareService';

function HardwareCheckinForm({ projectId, projectHardware, onActionComplete }) {
  const [hardwareName, setHardwareName] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const maxQuantity = projectHardware.find(hw => hw.name === hardwareName)?.quantity || 1;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userID = localStorage.getItem('userid');

    try {
      const response = await checkinHardware({ projectId, hardwareName, userID, qty: quantity });
      setSuccess(response.message);
      setError('');
      setHardwareName('');
      setQuantity(1);
      onActionComplete(); // Trigger full data refresh on check-in
    } catch (err) {
      setSuccess('');
      setError(err.message || 'Failed to check in hardware');
    }
  };

  return (
    <div>
      <h3>Check-In Hardware</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <label>Hardware Type:</label>
        <select
          value={hardwareName}
          onChange={(e) => setHardwareName(e.target.value)}
          required
        >
          <option value="">Select hardware</option>
          {projectHardware.map((hardware) => (
            <option key={hardware.name} value={hardware.name}>
              {hardware.name} (Checked out: {hardware.quantity})
            </option>
          ))}
        </select>

        <label>Quantity:</label>
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(Number(e.target.value))}
          min="1"
          max={maxQuantity}
          required
        />

        <button type="submit">Check-In</button>
      </form>
    </div>
  );
}

export default HardwareCheckinForm;

// src/components/Hardware/HardwareCheckoutForm.js

import React, { useState, useEffect } from 'react';
import { checkoutHardware } from '../../api/hardwareService';

function HardwareCheckoutForm({ projectId, globalHardware, onActionComplete }) {
  const [hardwareName, setHardwareName] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [maxQuantity, setMaxQuantity] = useState(1);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const selectedHardware = globalHardware.find(hw => hw.hardware_name === hardwareName);
    if (selectedHardware) {
      setMaxQuantity(selectedHardware.availability);
      setQuantity(1);
    }
  }, [hardwareName, globalHardware]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userID = localStorage.getItem('userid');

    try {
      const response = await checkoutHardware({ projectId, hardwareName, userID, qty: quantity });
      setSuccess(response.message);
      setError('');
      setHardwareName('');
      setQuantity(1);
      onActionComplete(); // Trigger full data refresh on checkout
    } catch (err) {
      setSuccess('');
      setError(err.message || 'Failed to checkout hardware');
    }
  };

  return (
    <div>
      <h3>Checkout Hardware</h3>
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
          {globalHardware.map((hardware) => (
            <option key={hardware.hardware_name} value={hardware.hardware_name}>
              {hardware.hardware_name} (Available: {hardware.availability})
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

        <button type="submit">Checkout</button>
      </form>
    </div>
  );
}

export default HardwareCheckoutForm;

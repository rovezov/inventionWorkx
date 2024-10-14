import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust if your backend is on a different port

function App() {
  const [cipherText, setCipherText] = useState('');
  const [cipherResult, setCipherResult] = useState('');
  const [hardwareSets, setHardwareSets] = useState([]);
  const [checkoutInfo, setCheckoutInfo] = useState({ setId: '', quantity: 1, userName: '' });

  useEffect(() => {
    fetchHardwareSets();
  }, []);

  const fetchHardwareSets = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/hardware-sets`);
      setHardwareSets(response.data);
    } catch (error) {
      console.error('Failed to fetch hardware sets:', error);
    }
  };

  const handleEncrypt = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/encrypt`, { text: cipherText, n: 1, d: 1 });
      setCipherResult(response.data.result);
    } catch (error) {
      console.error('Encryption failed:', error);
    }
  };

  const handleDecrypt = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/decrypt`, { text: cipherText, n: 1, d: 1 });
      setCipherResult(response.data.result);
    } catch (error) {
      console.error('Decryption failed:', error);
    }
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE_URL}/hardware-sets/${checkoutInfo.setId}/checkout`, {
        quantity: checkoutInfo.quantity,
        userName: checkoutInfo.userName
      });
      fetchHardwareSets();
      setCheckoutInfo({ setId: '', quantity: 1, userName: '' });
    } catch (error) {
      console.error('Checkout failed:', error);
    }
  };

  return (
    <div className="App">
      <h1>Cipher and Hardware Management System</h1>
      
      <div>
        <h2>Cipher Operations</h2>
        <input
          type="text"
          value={cipherText}
          onChange={(e) => setCipherText(e.target.value)}
          placeholder="Enter text to encrypt/decrypt"
        />
        <button onClick={handleEncrypt}>Encrypt</button>
        <button onClick={handleDecrypt}>Decrypt</button>
        {cipherResult && <p>Result: {cipherResult}</p>}
      </div>

      <div>
        <h2>Hardware Sets</h2>
        <ul>
          {hardwareSets.map((set) => (
            <li key={set.id}>
              {set.name} - Available: {set.availability}
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h2>Checkout Hardware</h2>
        <form onSubmit={handleCheckout}>
          <select
            value={checkoutInfo.setId}
            onChange={(e) => setCheckoutInfo({ ...checkoutInfo, setId: e.target.value })}
            required
          >
            <option value="">Select Hardware Set</option>
            {hardwareSets.map((set) => (
              <option key={set.id} value={set.id}>{set.name}</option>
            ))}
          </select>
          <input
            type="number"
            value={checkoutInfo.quantity}
            onChange={(e) => setCheckoutInfo({ ...checkoutInfo, quantity: parseInt(e.target.value) })}
            min="1"
            required
          />
          <input
            type="text"
            value={checkoutInfo.userName}
            onChange={(e) => setCheckoutInfo({ ...checkoutInfo, userName: e.target.value })}
            placeholder="User Name"
            required
          />
          <button type="submit">Checkout</button>
        </form>
      </div>
    </div>
  );
}

export default App;
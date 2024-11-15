// src/api/hardwareService.js

import axios from 'axios';


const BASE_URL = 'http://127.0.0.1:5000/api/hardware';

export const listHardware = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/list`);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error("Failed to load hardware");
  }
};

export const checkoutHardware = async ({ projectId, hardwareName, userID, qty }) => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${BASE_URL}/checkout`,
      { projectId, hardwareName, userID, qty },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error("Checkout failed");
  }
};

export const checkinHardware = async ({ projectId, hardwareName, userID, qty }) => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${BASE_URL}/checkin`,
      { projectId, hardwareName, userID, qty },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error("Check-in failed");
  }
};

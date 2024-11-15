// src/api/authService.js

import axios from 'axios';


const BASE_URL = 'http://127.0.0.1:5000/api/auth';

export const signupUser = async (userid, password) => {
  try {
    const response = await axios.post(`${BASE_URL}/signup`, { userid, password });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error("Signup failed");
  }
};

export const loginUser = async (userid, password) => {
  try {
    const response = await axios.post(`${BASE_URL}/login`, { userid, password });
    return response.data;  // Return token on successful login
  } catch (error) {
    throw error.response ? error.response.data : new Error("Login failed");
  }
};
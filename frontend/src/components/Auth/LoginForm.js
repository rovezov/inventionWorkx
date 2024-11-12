// src/components/Auth/LoginForm.js

import React, { useState } from 'react';
import { loginUser } from '../../api/authService';
import { useNavigate } from 'react-router-dom';
import './LoginForm.css';

function LoginForm({ setIsLoggedIn }) {
  const [userid, setUserid] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(userid, password);
      localStorage.setItem('token', data.token);
      localStorage.setItem('userid', userid);
      setIsLoggedIn(true); // Set the login state to true on successful login
      navigate('/');
    } catch (err) {
      setError(err.message || 'Login failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <p>{error}</p>}
      <input
        type="text"
        placeholder="UserID"
        value={userid}
        onChange={(e) => setUserid(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}

export default LoginForm;

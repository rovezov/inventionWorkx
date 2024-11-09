// src/components/Auth/SignupForm.js

import React, { useState } from 'react';
import { loginUser, signupUser } from '../../api/authService';
import { useNavigate } from 'react-router-dom';

function SignupForm() {
  const [userid, setUserid] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signupUser(userid, password);
      const data = await loginUser(userid, password);
      localStorage.setItem('token', data.token);
      localStorage.setItem('userid', userid);  // Save the userid for later use
      navigate('/');
    } catch (err) {
      setError(err.message || 'Signup failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Signup</h2>
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
      <button type="submit">Signup</button>
    </form>
  );
}

export default SignupForm;

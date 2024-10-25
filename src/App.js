import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import './App.css';
import CreateUser from './CreateUser';
import Dashboard from './Dashboard'; // Import the new Dashboard component

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); // Initialize navigate for routing

  const validUsername = 'user123';
  const validPassword = 'password123';

  const handleLogin = (event) => {
    event.preventDefault();
    if (username === validUsername && password === validPassword) {
      console.log('Login successful!');
      setErrorMessage(''); // Clear previous error messages
      navigate('/dashboard'); // Navigate to the dashboard
    } else {
      setErrorMessage('Invalid username or password. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <label className="password">Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </form>
      <Link to="/create-user">
        <button className="create-user-button">Create New User</button>
      </Link>
    </div>
  );
}

function Main() {
  return (
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/create-user" element={<CreateUser />} />
      <Route path="/dashboard" element={<Dashboard />} /> {/* Add this route */}
    </Routes>
  );
}

function AppWrapper() {
  return (
    <Router>
      <Main />
    </Router>
  );
}

export default AppWrapper;

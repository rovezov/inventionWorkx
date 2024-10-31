import React, { useState } from 'react';

const Login = () => {
  const [credentials, setCredentials] = useState({
    usernameOrEmail: '',
    password: '',
  });

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle login here (e.g., send credentials to backend)
    console.log('Submitted credentials: ', credentials);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="usernameOrEmail">Username or Email</label>
        <input
          type="text"
          name="usernameOrEmail"
          value={credentials.usernameOrEmail}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          type="password"
          name="password"
          value={credentials.password}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;

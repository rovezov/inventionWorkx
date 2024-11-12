// src/pages/Login.js

import React from 'react';
import LoginForm from '../components/Auth/LoginForm';

function Login({ setIsLoggedIn }) {
  return <LoginForm setIsLoggedIn={setIsLoggedIn} />;
}

export default Login;

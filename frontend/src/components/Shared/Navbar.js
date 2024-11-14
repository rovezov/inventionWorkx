// src/components/Shared/Navbar.js

import React from 'react';
import { Link } from 'react-router-dom';

function Navbar({ isLoggedIn, handleLogout }) {
  return (
    <nav>
      <Link to="/">Home</Link>
      {!isLoggedIn ? (
        <>
          <Link to="/login">Login</Link>
          <Link to="/signup">Signup</Link>
        </>
      ) : (
        <button onClick={handleLogout}>Logout</button>
      )}
    </nav>
  );
}

export default Navbar;

import logo from './logo.svg';
import './App.css';
import React, { usestate } from "react";
import Login from "./Login";

function App() {
  return (
    // <div className="App">
    //   <Login />
    // </div>
    <div className="login-container">
    {/* <img src={require('./logo.png')} alt="Logo" className="logo" /> */}
    <h2>Login</h2>
    <form>
      <label>Username:</label>
      <input type="text" />
      <label className="password">Password:</label>
      <input type="password" />
      <button type="submit">Login</button>
    </form>
    <button className="create-user-button">Create New User</button> {/* New button */}
  </div>
  );
}

export default App;

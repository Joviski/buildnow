import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";


export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    // Simulate API authentication (Replace with real API call)
    if (username === "admin" && password === "admin") {
      localStorage.setItem("authToken", btoa(`${username}:${password}`)); // Save token
      navigate("/dashboard"); // Redirect to dashboard
    } else {
      alert("Invalid credentials");
    }
  };

  return (
      <div className="login-container">
        <form onSubmit={handleLogin} className="login-form">
          <h2 className="login-title">Login</h2>
          <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="login-input"
          />
          <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="login-input"
          />
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
      </div>
  )
}
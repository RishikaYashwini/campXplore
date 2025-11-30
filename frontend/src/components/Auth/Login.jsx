// FIXED Login.jsx with Correct Import Paths
// Location: src/components/Auth/Login.jsx

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { showToast } from '../../utils/helpers';
import { useTheme } from '../../contexts/ThemeContext';
import { useAuth } from '../../contexts/AuthContext';
import campusImage from '../../assets/images/campus.jpg';
import logoImage from '../../assets/images/campxplore-logo.png';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { isDarkMode, toggleTheme } = useTheme();
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      showToast('Please enter email and password', 'warning');
      return;
    }

    setLoading(true);

    try {
      const response = await authAPI.login({ email, password });

      if (response.data.user) {
        login(response.data.user); // Save user to context
        showToast(`Welcome back, ${response.data.user.name}!`, 'success');
        navigate('/dashboard');
      }
    } catch (error) {
      console.error('Login error:', error);
      showToast(error.response?.data?.error || 'Login failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {/* Background with Campus Image */}
      <div 
        className="login-background"
        style={{ backgroundImage: `url(${campusImage})` }}
      >
        <div className="background-overlay"></div>
      </div>

      {/* Theme Toggle (Top Right) */}
      <button 
        className="theme-toggle-floating"
        onClick={toggleTheme}
        title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
      >
        {isDarkMode ? '☀️' : '🌙'}
      </button>

      {/* Login Card */}
      <div className="login-content">
        <div className="login-card">
          {/* Logo Section */}
          <div className="login-logo">
            <img 
              src={logoImage}
              alt="CampXplore Logo"
              className="logo-image logo"
            />
            <h1 className="app-title">CampXplore</h1>
            <p className="app-tagline">Dr. Ambedkar Institute of Technology</p>
          </div>

          {/* Login Form */}
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label htmlFor="email">📧 Email Address</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@drait.edu.in"
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">🔒 Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                disabled={loading}
                autoComplete="current-password"
              />
            </div>

            <button 
              type="submit" 
              className="btn-login"
              disabled={loading}
            >
              {loading ? (
                <>🔄 Logging in...</>
              ) : (
                <>🚀 Login</>
              )}
            </button>

            <div className="register-link">
              <p>Don't have an account? <Link to="/register">Register here</Link></p>
            </div>
          </form>

          {/* Demo Accounts */}
          <div className="demo-accounts">
            <p className="demo-title">Demo Accounts:</p>
            <div className="demo-list">
              <small>👨‍💼 Admin: admin@drait.edu.in / admin123</small>
              <small>🎓 Student: rishika@drait.edu.in / student123</small>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="login-footer">
          <p>© 2025 CampXplore - Dr. AIT Campus Management System</p>
        </div>
      </div>
    </div>
  );
}

export default Login;

// FIXED Navbar.jsx with Correct Import Paths
// Location: src/components/Navigation/Navbar.jsx

import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import logoImage from '../../assets/images/campxplore-logo.png';
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();
  const { isDarkMode, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo & Brand */}
        <Link to="/dashboard" className="navbar-brand">
          <img 
            src={logoImage}
            alt="CampXplore" 
            className="navbar-logo logo"
          />
          <span className="brand-text">CampXplore</span>
        </Link>

        {/* Navigation Menu */}
        <div className="navbar-menu">
          <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
            🏠 Dashboard
          </Link>
          {user?.role === 'admin' && (
            <Link to="/admin/analytics" className={`nav-link ${isActive('/admin/analytics')}`}>
              📊 Analytics
            </Link>
          )}
          <Link to="/campus-map" className={`nav-link ${isActive('/campus-map')}`}>
            🗺️ Campus Map
          </Link>
          <Link to="/complaints" className={`nav-link ${isActive('/complaints')}`}>
            📝 Complaints
          </Link>
          <Link to="/feedback" className={`nav-link ${isActive('/feedback')}`}>
            ⭐ Feedback
          </Link>
        </div>

        {/* Right Section */}
        <div className="navbar-actions">
          {/* Dark Mode Toggle */}
          <button 
            className="theme-toggle"
            onClick={toggleTheme}
            title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          >
            <span className="theme-icon">
              {isDarkMode ? '☀️' : '🌙'}
            </span>
          </button>

          {/* User Profile */}
          {user && (
            <div className="user-profile">
              <div className="user-avatar avatar">
                {user.name?.charAt(0).toUpperCase() || 'U'}
              </div>
              <div className="user-info">
                <span className="user-name">{user.name}</span>
                <span className="user-role">{user.role}</span>
              </div>
            </div>
          )}

          {/* Logout Button */}
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

// Register Component - Logo INSIDE Card (Like Login)
// Location: src/components/Auth/Register.jsx

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { showToast, validateEmail, validatePassword, getErrorMessage } from '../../utils/helpers';
import { useTheme } from '../../contexts/ThemeContext';
import { useAuth } from '../../contexts/AuthContext';
import campusImage from '../../assets/images/campus.jpg';
import logoImage from '../../assets/images/campxplore-logo.png';
import './Login.css';

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    department: '',
    phone: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { isDarkMode, toggleTheme } = useTheme();
  const { login } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    else if (!validateEmail(formData.email)) newErrors.email = 'Invalid email';
    if (!formData.password) newErrors.password = 'Password is required';
    else if (!validatePassword(formData.password)) newErrors.password = 'Min 6 characters';
    if (formData.password !== formData.confirmPassword) newErrors.confirmPassword = 'Passwords do not match';
    if (!formData.department.trim()) newErrors.department = 'Department is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (!validate()) {
      showToast('Please fix the errors', 'warning');
      return;
    }

    setLoading(true);

    try {
      await authAPI.register({
        name: formData.name.trim(),
        email: formData.email.trim(),
        password: formData.password,
        department: formData.department.trim(),
        phone: formData.phone.trim()
      });

      showToast('Registration successful!', 'success');

      // Auto-login
      const loginResponse = await authAPI.login({
        email: formData.email,
        password: formData.password
      });

      login(loginResponse.data.user);
      navigate('/dashboard');

    } catch (error) {
      const errorMsg = getErrorMessage(error);
      showToast(errorMsg, 'error');
      setErrors({ general: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {/* Background */}
      <div 
        className="login-background"
        style={{ backgroundImage: `url(${campusImage})` }}
      >
        <div className="background-overlay"></div>
      </div>

      {/* Theme Toggle */}
      <button 
        className="theme-toggle-floating"
        onClick={toggleTheme}
        aria-label="Toggle theme"
      >
        {isDarkMode ? '☀️' : '🌙'}
      </button>

      {/* Content */}
      <div className="login-content">
        {/* Card with Logo INSIDE (like Login) */}
        <div className="login-card">
          {/* Logo Section INSIDE Card */}
          <div className="login-logo">
            <img src={logoImage} alt="CampXplore Logo" className="logo-image logo" />
            <h1 className="app-title">CampXplore</h1>
            <p className="app-tagline">Dr. Ambedkar Institute of Technology</p>
          </div>

          {/* Form Title */}
          <h2>Create Account </h2>

          {errors.general && (
            <div className="error-message">{errors.general}</div>
          )}

          <form onSubmit={handleRegister} className="login-form">
            {/* Name */}
            <div className="form-group">
              <label htmlFor="name">📧 Full Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter your full name"
                className={errors.name ? 'error' : ''}
              />
              {errors.name && <span className="error-text">{errors.name}</span>}
            </div>

            {/* Email */}
            <div className="form-group">
              <label htmlFor="email">📧 Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="your.email@drait.edu.in"
                className={errors.email ? 'error' : ''}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>

            {/* Department */}
            <div className="form-group">
              <label htmlFor="department">📧 Department</label>
              <input
                type="text"
                id="department"
                name="department"
                value={formData.department}
                onChange={handleChange}
                placeholder="e.g., Computer Science"
                className={errors.department ? 'error' : ''}
              />
              {errors.department && <span className="error-text">{errors.department}</span>}
            </div>

            {/* Phone */}
            <div className="form-group">
              <label htmlFor="phone">📧 Phone Number (Optional)</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="Enter your phone number"
              />
            </div>

            {/* Password */}
            <div className="form-group">
              <label htmlFor="password">🔒 Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                className={errors.password ? 'error' : ''}
              />
              {errors.password && <span className="error-text">{errors.password}</span>}
            </div>

            {/* Confirm Password */}
            <div className="form-group">
              <label htmlFor="confirmPassword">🔒 Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Re-enter your password"
                className={errors.confirmPassword ? 'error' : ''}
              />
              {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
            </div>

            {/* Submit Button */}
            <button 
              type="submit" 
              className="btn-login"
              disabled={loading}
            >
              {loading ? '⏳ Creating Account...' : '🚀 LOGIN'}
            </button>

            {/* Login Link */}
            <div className="register-link">
              <p>
                Already have an account? <Link to="/login">Sign In</Link>
              </p>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="login-footer">
          <p>© 2025 CampXplore - Dr. AIT Campus Management System</p>
        </div>
      </div>
    </div>
  );
}

export default Register;

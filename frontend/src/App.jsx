// FIXED App.jsx - Routes Admin to AdminDashboard
// Location: src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import './styles/darkmode.css';
import './App.css';

// Import Components
import Navbar from './components/Navigation/Navbar';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import AdminDashboard from './components/Admin/Dashboard';
import Analytics from './components/Admin/Analytics';
import CampusMap from './components/Map/CampusMap';
import ComplaintForm from './components/Complaints/ComplaintForm';
import ComplaintList from './components/Complaints/ComplaintList';
import FeedbackForm from './components/Feedback/FeedbackForm';
import FeedbackList from './components/Feedback/FeedbackList';

// Protected Route Component
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return user ? children : <Navigate to="/login" replace />;
}

// Main App Routes (inside AuthProvider)
function AppRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading CampXplore...</p>
      </div>
    );
  }

  return (
    <div className="App">
      {user && <Navbar />}

      <main className="main-content">
        <Routes>
          {/* Public Routes */}
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" replace /> : <Login />} 
          />
          <Route 
            path="/register" 
            element={user ? <Navigate to="/dashboard" replace /> : <Register />} 
          />

          {/* Dashboard - Routes based on role */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                {user?.role === 'admin' ? <AdminDashboard /> : <Dashboard />}
              </ProtectedRoute>
            } 
          />

          {/* Analytics Route - Admin Only */}
          <Route
            path="/admin/analytics"
            element={
              <ProtectedRoute>
                <Analytics />
              </ProtectedRoute>
            }
          />

          {/* Protected Routes */}
          <Route 
            path="/campus-map" 
            element={
              <ProtectedRoute>
                <CampusMap />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/map" 
            element={<Navigate to="/campus-map" replace />} 
          />
          <Route 
            path="/complaints" 
            element={
              <ProtectedRoute>
                <ComplaintList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/complaints/new" 
            element={
              <ProtectedRoute>
                <ComplaintForm />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/feedback" 
            element={
              <ProtectedRoute>
                <FeedbackList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/feedback/new" 
            element={
              <ProtectedRoute>
                <FeedbackForm />
              </ProtectedRoute>
            } 
          />

          {/* Admin route (same as dashboard for admins) */}
          <Route 
            path="/admin" 
            element={<Navigate to="/dashboard" replace />} 
          />

          {/* Default Routes */}
          <Route 
            path="/" 
            element={user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />} 
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

// Main App Component
function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <AppRoutes />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;

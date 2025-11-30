// FIXED Dashboard.jsx - No Navbar (already in App.jsx)
// Location: src/components/Dashboard/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { complaintsAPI, feedbackAPI } from '../../services/api';
import campusImage from '../../assets/images/campus.jpg';
import './Dashboard.css';

function Dashboard() {
  const { user } = useAuth();
  const { isDarkMode } = useTheme();
  const navigate = useNavigate();

  const [stats, setStats] = useState({
    totalComplaints: 0,
    pendingComplaints: 0,
    resolvedComplaints: 0,
    totalFeedback: 0
  });
  const [loading, setLoading] = useState(true);
  const [recentActivity, setRecentActivity] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // Fetch complaints
      const complaintsResponse = await complaintsAPI.getAll();
      const complaints = complaintsResponse.data.complaints || [];

      // Fetch feedback
      const feedbackResponse = await feedbackAPI.getAll();
      const feedbacks = feedbackResponse.data.feedback || [];

      // Calculate stats
      const pending = complaints.filter(c => c.status === 'pending').length;
      const resolved = complaints.filter(c => c.status === 'resolved').length;

      setStats({
        totalComplaints: complaints.length,
        pendingComplaints: pending,
        resolvedComplaints: resolved,
        totalFeedback: feedbacks.length
      });

      // Get recent activity (last 3 complaints)
      const recent = complaints
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 3)
        .map(complaint => ({
          type: 'complaint',
          title: complaint.status === 'resolved' ? 'Complaint resolved' : 'New complaint submitted',
          description: complaint.description,
          time: getRelativeTime(complaint.created_at)
        }));

      setRecentActivity(recent);

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Use fallback dummy data if API fails
      setStats({
        totalComplaints: 0,
        pendingComplaints: 0,
        resolvedComplaints: 0,
        totalFeedback: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const getRelativeTime = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    return `${diffDays} days ago`;
  };

  return (
    <div 
      className="dashboard-container"
      style={{ backgroundImage: `url(${campusImage})` }}
    >
      <div className="dashboard-overlay"></div>

      <div className="dashboard-content">
        {/* Header */}
        <div className="dashboard-header">
          <div className="welcome-section">
            <h1>Welcome back, {user?.name || 'User'}! 👋</h1>
            <p>Here's what's happening with your campus today.</p>
          </div>
          <div className="quick-actions">
            <button className="btn-action" onClick={() => navigate('/campus-map')}>
              🗺️ View Map
            </button>
            <button className="btn-action" onClick={() => navigate('/complaints/new')}>
              📝 New Complaint
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        {loading ? (
          <div className="loading-stats">Loading statistics...</div>
        ) : (
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon" style={{background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
                📋
              </div>
              <div className="stat-info">
                <span className="stat-label">Total Complaints</span>
                <span className="stat-value">{stats.totalComplaints}</span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'}}>
                ⏳
              </div>
              <div className="stat-info">
                <span className="stat-label">Pending</span>
                <span className="stat-value">{stats.pendingComplaints}</span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)'}}>
                ✅
              </div>
              <div className="stat-info">
                <span className="stat-label">Resolved</span>
                <span className="stat-value">{stats.resolvedComplaints}</span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{background: 'linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%)'}}>
                ⭐
              </div>
              <div className="stat-info">
                <span className="stat-label">Feedback</span>
                <span className="stat-value">{stats.totalFeedback}</span>
              </div>
            </div>
          </div>
        )}

        {/* Recent Activity */}
        <div className="dashboard-section">
          <h2>Recent Activity</h2>
          <div className="activity-list">
            {recentActivity.length > 0 ? (
              recentActivity.map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-icon">
                    {activity.title.includes('resolved') ? '✅' : '📝'}
                  </div>
                  <div className="activity-content">
                    <h3>{activity.title}</h3>
                    <p>{activity.description}</p>
                    <span className="activity-time">{activity.time}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-activity">
                <p>No recent activity to display</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

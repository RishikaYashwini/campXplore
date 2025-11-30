// Analytics Dashboard Component - DARK MODE FIX
// Location: src/components/Admin/Analytics.jsx

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext'; // ← ADDED
import { useNavigate } from 'react-router-dom';
import { analyticsAPI } from '../../services/api';
import { showToast, getErrorMessage } from '../../utils/helpers';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import './Analytics.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

function Analytics() {
  const { user } = useAuth();
  const { isDarkMode } = useTheme(); // ← ADDED for dark mode detection
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [analyticsData, setAnalyticsData] = useState(null);

  useEffect(() => {
    // Check if user is admin
    if (user?.role !== 'admin') {
      showToast('Access denied. Admin only.', 'error');
      navigate('/dashboard');
      return;
    }

    fetchAnalytics();
  }, [user, navigate]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);

      // Fetch all analytics data
      const [dashboardRes, complaintsRes, feedbackRes] = await Promise.all([
        analyticsAPI.getDashboard(),
        analyticsAPI.getComplaintAnalytics(),
        analyticsAPI.getFeedbackAnalytics()
      ]);

      setAnalyticsData({
        dashboard: dashboardRes.data,
        complaints: complaintsRes.data,
        feedback: feedbackRes.data
      });

    } catch (error) {
      console.error('Analytics fetch error:', error);
      showToast(getErrorMessage(error), 'error');
    } finally {
      setLoading(false);
    }
  };

  // Chart configurations
  const getComplaintsStatusChart = () => {
    if (!analyticsData?.complaints) return null;

    const data = analyticsData.complaints;

    return {
      labels: ['Open', 'In Progress', 'Resolved'],
      datasets: [
        {
          label: 'Complaints by Status',
          data: [
            data.open_complaints || 0,
            data.in_progress_complaints || 0,
            data.resolved_complaints || 0
          ],
          backgroundColor: [
            'rgba(255, 159, 64, 0.8)',   // Orange - Open
            'rgba(54, 162, 235, 0.8)',   // Blue - In Progress
            'rgba(75, 192, 192, 0.8)',   // Green - Resolved
          ],
          borderColor: [
            'rgba(255, 159, 64, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(75, 192, 192, 1)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  const getComplaintsPriorityChart = () => {
    if (!analyticsData?.complaints) return null;

    const data = analyticsData.complaints;

    return {
      labels: ['Low', 'Medium', 'High'],
      datasets: [
        {
          label: 'Complaints by Priority',
          data: [
            data.low_priority_complaints || 0,
            data.medium_priority_complaints || 0,
            data.high_priority_complaints || 0
          ],
          backgroundColor: [
            'rgba(75, 192, 192, 0.8)',   // Green - Low
            'rgba(255, 206, 86, 0.8)',   // Yellow - Medium
            'rgba(255, 99, 132, 0.8)',   // Red - High
          ],
          borderColor: [
            'rgba(75, 192, 192, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(255, 99, 132, 1)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  const getFeedbackRatingsChart = () => {
    if (!analyticsData?.feedback) return null;

    const data = analyticsData.feedback;

    return {
      labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
      datasets: [
        {
          label: 'Number of Feedback',
          data: [
            data.ratings_1 || 0,
            data.ratings_2 || 0,
            data.ratings_3 || 0,
            data.ratings_4 || 0,
            data.ratings_5 || 0
          ],
          backgroundColor: 'rgba(102, 126, 234, 0.8)',
          borderColor: 'rgba(102, 126, 234, 1)',
          borderWidth: 2,
        },
      ],
    };
  };

  // ✨ FIXED: Chart options with dark mode support
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: isDarkMode ? '#f7fafc' : '#2d3748', // ← FIXED: Light text in dark mode
          font: {
            size: 12,
            weight: 600
          }
        }
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        ticks: {
          color: isDarkMode ? '#e2e8f0' : '#2d3748', // ← FIXED: Light text in dark mode
        },
        grid: {
          color: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
        }
      },
      y: {
        ticks: {
          color: isDarkMode ? '#e2e8f0' : '#2d3748', // ← FIXED: Light text in dark mode
        },
        grid: {
          color: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
        }
      }
    }
  };

  const pieOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      legend: {
        position: 'bottom',
        labels: {
          color: isDarkMode ? '#f7fafc' : '#2d3748', // ← FIXED: Light text in dark mode
          font: {
            size: 12,
            weight: 600
          },
          padding: 15
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading analytics data...</p>
        </div>
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="analytics-container">
        <div className="error-state">
          <p>Failed to load analytics data</p>
          <button onClick={fetchAnalytics} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const { dashboard, complaints, feedback } = analyticsData;

  return (
    <div className="analytics-container">
      {/* Header */}
      <div className="analytics-header">
        <div>
          <h1>📊 Analytics Dashboard</h1>
          <p>Comprehensive insights into campus management</p>
        </div>
        <button onClick={fetchAnalytics} className="btn-refresh">
          🔄 Refresh Data
        </button>
      </div>

      {/* Quick Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
            👥
          </div>
          <div className="stat-content">
            <h3>{dashboard?.total_users || 0}</h3>
            <p>Total Users</p>
            <span className="stat-detail">
              {dashboard?.students || 0} Students · {dashboard?.faculty || 0} Faculty
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
            📝
          </div>
          <div className="stat-content">
            <h3>{complaints?.total_complaints || 0}</h3>
            <p>Total Complaints</p>
            <span className="stat-detail">
              {complaints?.open_complaints || 0} Open · {complaints?.resolved_complaints || 0} Resolved
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
            ⭐
          </div>
          <div className="stat-content">
            <h3>{feedback?.total_feedback || 0}</h3>
            <p>Total Feedback</p>
            <span className="stat-detail">
              Avg Rating: {feedback?.average_rating || 0} ★
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}>
            📈
          </div>
          <div className="stat-content">
            <h3>{complaints?.high_priority_complaints || 0}</h3>
            <p>High Priority</p>
            <span className="stat-detail">
              Requires immediate attention
            </span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <h2>📊 Detailed Analytics</h2>

        <div className="charts-grid">
          {/* Complaints Status Chart */}
          <div className="chart-card">
            <h3>Complaints by Status</h3>
            <div className="chart-container">
              {getComplaintsStatusChart() && (
                <Pie data={getComplaintsStatusChart()} options={pieOptions} />
              )}
            </div>
          </div>

          {/* Complaints Priority Chart */}
          <div className="chart-card">
            <h3>Complaints by Priority</h3>
            <div className="chart-container">
              {getComplaintsPriorityChart() && (
                <Pie data={getComplaintsPriorityChart()} options={pieOptions} />
              )}
            </div>
          </div>

          {/* Feedback Ratings Chart */}
          <div className="chart-card chart-card-wide">
            <h3>Feedback Ratings Distribution</h3>
            <div className="chart-container">
              {getFeedbackRatingsChart() && (
                <Bar data={getFeedbackRatingsChart()} options={chartOptions} />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Additional Insights */}
      <div className="insights-section">
        <h2>💡 Key Insights</h2>

        <div className="insights-grid">
          <div className="insight-card">
            <h4>🎯 Resolution Rate</h4>
            <div className="insight-value">
              {complaints?.total_complaints > 0 
                ? Math.round((complaints.resolved_complaints / complaints.total_complaints) * 100)
                : 0}%
            </div>
            <p>of complaints resolved</p>
          </div>

          <div className="insight-card">
            <h4>⚡ Active Issues</h4>
            <div className="insight-value">
              {(complaints?.open_complaints || 0) + (complaints?.in_progress_complaints || 0)}
            </div>
            <p>complaints pending</p>
          </div>

          <div className="insight-card">
            <h4>⭐ User Satisfaction</h4>
            <div className="insight-value">
              {feedback?.average_rating ? (feedback.average_rating * 20).toFixed(0) : 0}%
            </div>
            <p>based on feedback ratings</p>
          </div>

          <div className="insight-card">
            <h4>🔥 Critical Issues</h4>
            <div className="insight-value">
              {complaints?.high_priority_complaints || 0}
            </div>
            <p>high priority complaints</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Analytics;

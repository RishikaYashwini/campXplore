// Feedback List & Analytics - Full Version
// Location: src/components/Feedback/FeedbackList.jsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { feedbackAPI } from '../../services/api';
import { 
  formatDate, 
  getRatingColor,
  renderStars,
  showToast
} from '../../utils/helpers';
import './Feedback.css';

function FeedbackList() {
  const [allFeedback, setAllFeedback] = useState([]);
  const [myFeedback, setMyFeedback] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterRating, setFilterRating] = useState('all');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [allRes, myRes, summaryRes] = await Promise.all([
        feedbackAPI.getAll(),
        feedbackAPI.getMyFeedback(),
        feedbackAPI.getSummary()
      ]);

      setAllFeedback(allRes.data.feedback || []);
      setMyFeedback(myRes.data.feedback || []);
      setSummary(summaryRes.data);

    } catch (error) {
      console.error('Error fetching feedback:', error);
      showToast('Failed to load feedback', 'error');
    } finally {
      setLoading(false);
    }
  };

  const currentFeedback = activeTab === 'all' ? allFeedback : myFeedback;

  const filteredFeedback = currentFeedback.filter(feedback => {
    if (filterCategory !== 'all' && feedback.category !== filterCategory) return false;
    if (filterRating !== 'all' && feedback.rating !== parseInt(filterRating)) return false;
    return true;
  });

  const categories = [...new Set(allFeedback.map(f => f.category))];

  if (loading) {
    return (
      <div className="feedback-container">
        <div className="loading">Loading feedback...</div>
      </div>
    );
  }

  return (
    <div className="feedback-container">
      {/* Header */}
      <div className="feedback-header">
        <div>
          <h1>⭐ Campus Feedback</h1>
          <p>View and share feedback about campus facilities</p>
        </div>
        <Link to="/feedback/new" className="btn btn-primary">
          + Submit Feedback
        </Link>
      </div>

      {/* Summary Statistics */}
      {summary && (
        <div className="summary-card">
          <div className="summary-header">
            <h2>📊 Overall Summary</h2>
          </div>
          <div className="summary-stats">
            <div className="summary-stat">
              <div className="summary-value">{summary.total_feedback}</div>
              <div className="summary-label">Total Feedback</div>
            </div>
            <div className="summary-stat">
              <div className="summary-value rating-value">
                {summary.average_rating ? summary.average_rating.toFixed(1) : '0.0'}
                <span className="star-icon">★</span>
              </div>
              <div className="summary-label">Average Rating</div>
            </div>
            <div className="summary-stat">
              <div className="rating-bars">
                {[5, 4, 3, 2, 1].map(rating => (
                  <div key={rating} className="rating-bar-item">
                    <span className="rating-bar-label">{rating}★</span>
                    <div className="rating-bar-track">
                      <div 
                        className="rating-bar-fill"
                        style={{ 
                          width: `${(summary.rating_distribution[rating] || 0) / summary.total_feedback * 100}%`,
                          background: getRatingColor(rating)
                        }}
                      />
                    </div>
                    <span className="rating-bar-count">
                      {summary.rating_distribution[rating] || 0}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="tabs-container">
        <button 
          className={`tab ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          All Feedback ({allFeedback.length})
        </button>
        <button 
          className={`tab ${activeTab === 'my' ? 'active' : ''}`}
          onClick={() => setActiveTab('my')}
        >
          My Feedback ({myFeedback.length})
        </button>
      </div>

      {/* Filters */}
      <div className="filters-bar">
        <div className="filter-group">
          <label>Category:</label>
          <select value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)}>
            <option value="all">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Rating:</label>
          <select value={filterRating} onChange={(e) => setFilterRating(e.target.value)}>
            <option value="all">All Ratings</option>
            <option value="5">5 Stars</option>
            <option value="4">4 Stars</option>
            <option value="3">3 Stars</option>
            <option value="2">2 Stars</option>
            <option value="1">1 Star</option>
          </select>
        </div>

        <div className="filter-results">
          Showing {filteredFeedback.length} of {currentFeedback.length}
        </div>
      </div>

      {/* Feedback List */}
      {filteredFeedback.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📭</div>
          <h3>No feedback found</h3>
          <p>
            {activeTab === 'my' 
              ? "You haven't submitted any feedback yet" 
              : "No feedback matches your filters"}
          </p>
          <Link to="/feedback/new" className="btn btn-primary">
            Submit Your First Feedback
          </Link>
        </div>
      ) : (
        <div className="feedback-grid">
          {filteredFeedback.map(feedback => (
            <div key={feedback.feedback_id} className="feedback-card">
              <div className="feedback-card-header">
                <div className="feedback-facility">
                  <h3>{feedback.facility}</h3>
                  <span className="feedback-category">{feedback.category}</span>
                </div>
                <div className="feedback-rating">
                  <div 
                    className="rating-display"
                    style={{ color: getRatingColor(feedback.rating) }}
                  >
                    {renderStars(feedback.rating)}
                  </div>
                  <span className="rating-number">{feedback.rating}/5</span>
                </div>
              </div>

              <div className="feedback-meta">
                <span className="meta-item">
                  📍 {feedback.building_name}
                </span>
                <span className="meta-item">
                  👤 {feedback.user_name}
                </span>
                <span className="meta-item">
                  📅 {formatDate(feedback.created_at)}
                </span>
              </div>

              {feedback.comments && (
                <p className="feedback-comments">
                  {feedback.comments}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FeedbackList;

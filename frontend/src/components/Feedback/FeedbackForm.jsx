// Feedback Submission Form - Full Version
// Location: src/components/Feedback/FeedbackForm.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { feedbackAPI, buildingsAPI } from '../../services/api';
import { showToast, getErrorMessage, validateRating } from '../../utils/helpers';
import './Feedback.css';

function FeedbackForm() {
  const navigate = useNavigate();
  const [buildings, setBuildings] = useState([]);
  const [formData, setFormData] = useState({
    facility: '',
    building_id: '',
    rating: 0,
    comments: '',
    category: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [hoveredRating, setHoveredRating] = useState(0);

  const categories = [
    'Library',
    'Laboratory',
    'Classroom',
    'Cafeteria',
    'Sports Facility',
    'Hostel',
    'Auditorium',
    'Other'
  ];

  useEffect(() => {
    fetchBuildings();
  }, []);

  const fetchBuildings = async () => {
    try {
      const response = await buildingsAPI.getAll();
      setBuildings(response.data.buildings || []);
    } catch (error) {
      console.error('Error fetching buildings:', error);
      showToast('Failed to load buildings', 'error');
    }
  };

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

  const handleRatingClick = (rating) => {
    setFormData(prev => ({
      ...prev,
      rating
    }));

    if (errors.rating) {
      setErrors(prev => ({
        ...prev,
        rating: ''
      }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.facility.trim()) {
      newErrors.facility = 'Facility name is required';
    }

    if (!formData.building_id) {
      newErrors.building_id = 'Please select a building';
    }

    if (!validateRating(formData.rating)) {
      newErrors.rating = 'Please select a rating (1-5 stars)';
    }

    if (!formData.category) {
      newErrors.category = 'Please select a category';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) return;

    setLoading(true);

    try {
      const feedbackData = {
        ...formData,
        building_id: parseInt(formData.building_id),
        rating: parseInt(formData.rating)
      };

      await feedbackAPI.create(feedbackData);

      showToast('Feedback submitted successfully!', 'success');
      navigate('/feedback');

    } catch (error) {
      const errorMsg = getErrorMessage(error);
      showToast(errorMsg, 'error');
      setErrors({ general: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  const getRatingLabel = (rating) => {
    const labels = {
      1: 'Poor',
      2: 'Fair',
      3: 'Good',
      4: 'Very Good',
      5: 'Excellent'
    };
    return labels[rating] || '';
  };

  return (
    <div className="feedback-container">
      <div className="feedback-header">
        <div>
          <h1>⭐ Submit Feedback</h1>
          <p>Share your experience and help improve campus facilities</p>
        </div>
        <button 
          onClick={() => navigate('/feedback')}
          className="btn btn-secondary"
        >
          ← Back to Feedback
        </button>
      </div>

      <div className="form-card">
        <form onSubmit={handleSubmit} className="feedback-form">
          {errors.general && (
            <div className="error-banner">
              {errors.general}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="facility">Facility Name *</label>
            <input
              type="text"
              id="facility"
              name="facility"
              value={formData.facility}
              onChange={handleChange}
              className={errors.facility ? 'error' : ''}
              placeholder="e.g., Computer Lab, Reading Hall, Basketball Court..."
              maxLength="200"
            />
            {errors.facility && <span className="error-text">{errors.facility}</span>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="building_id">Building/Location *</label>
              <select
                id="building_id"
                name="building_id"
                value={formData.building_id}
                onChange={handleChange}
                className={errors.building_id ? 'error' : ''}
              >
                <option value="">Select building...</option>
                {buildings.map(building => (
                  <option key={building.building_id} value={building.building_id}>
                    {building.name} ({building.code})
                  </option>
                ))}
              </select>
              {errors.building_id && <span className="error-text">{errors.building_id}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="category">Category *</label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleChange}
                className={errors.category ? 'error' : ''}
              >
                <option value="">Select category...</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
              {errors.category && <span className="error-text">{errors.category}</span>}
            </div>
          </div>

          <div className="form-group">
            <label>Your Rating *</label>
            <div className="rating-container">
              <div className="stars-wrapper">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    className={`star ${star <= (hoveredRating || formData.rating) ? 'active' : ''}`}
                    onClick={() => handleRatingClick(star)}
                    onMouseEnter={() => setHoveredRating(star)}
                    onMouseLeave={() => setHoveredRating(0)}
                  >
                    ★
                  </button>
                ))}
              </div>
              {(hoveredRating || formData.rating) > 0 && (
                <span className="rating-label">
                  {getRatingLabel(hoveredRating || formData.rating)}
                </span>
              )}
            </div>
            {errors.rating && <span className="error-text">{errors.rating}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="comments">Comments (Optional)</label>
            <textarea
              id="comments"
              name="comments"
              value={formData.comments}
              onChange={handleChange}
              placeholder="Share your thoughts, suggestions, or experiences..."
              rows="6"
              maxLength="500"
            />
            <span className="char-count">{formData.comments.length}/500</span>
          </div>

          <div className="form-actions">
            <button
              type="button"
              onClick={() => navigate('/feedback')}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Submitting...' : 'Submit Feedback'}
            </button>
          </div>
        </form>

        <div className="form-info">
          <h3>💡 Tips for Great Feedback</h3>
          <ul>
            <li>Be specific about the facility you're rating</li>
            <li>Mention both positive aspects and areas for improvement</li>
            <li>Use the rating scale meaningfully (1=Poor, 5=Excellent)</li>
            <li>Your feedback helps improve campus services</li>
            <li>All feedback is reviewed by the administration</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default FeedbackForm;

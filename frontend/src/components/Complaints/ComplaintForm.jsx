// Complaint Submission Form - Full Version
// Location: src/components/Complaints/ComplaintForm.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { complaintsAPI, buildingsAPI } from '../../services/api';
import { showToast, getErrorMessage } from '../../utils/helpers';
import './Complaints.css';

function ComplaintForm() {
  const navigate = useNavigate();
  const [buildings, setBuildings] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    priority: 'medium',
    building_id: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const categories = [
    'Infrastructure',
    'Technology',
    'Cleanliness',
    'Safety',
    'Maintenance',
    'Other'
  ];

  const priorities = [
    { value: 'low', label: 'Low', color: '#95a5a6' },
    { value: 'medium', label: 'Medium', color: '#f39c12' },
    { value: 'high', label: 'High', color: '#e74c3c' },
    { value: 'urgent', label: 'Urgent', color: '#c0392b' }
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

  const validate = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length < 10) {
      newErrors.title = 'Title must be at least 10 characters';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    } else if (formData.description.length < 20) {
      newErrors.description = 'Description must be at least 20 characters';
    }

    if (!formData.category) {
      newErrors.category = 'Please select a category';
    }

    if (!formData.building_id) {
      newErrors.building_id = 'Please select a building';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) return;

    setLoading(true);

    try {
      const complaintData = {
        ...formData,
        building_id: parseInt(formData.building_id)
      };

      await complaintsAPI.create(complaintData);

      showToast('Complaint submitted successfully!', 'success');
      navigate('/complaints');

    } catch (error) {
      const errorMsg = getErrorMessage(error);
      showToast(errorMsg, 'error');
      setErrors({ general: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="complaints-container">
      <div className="complaints-header">
        <div>
          <h1>📝 Submit Complaint</h1>
          <p>Report issues and concerns about campus facilities</p>
        </div>
        <button 
          onClick={() => navigate('/complaints')}
          className="btn btn-secondary"
        >
          ← Back to Complaints
        </button>
      </div>

      <div className="form-card">
        <form onSubmit={handleSubmit} className="complaint-form">
          {errors.general && (
            <div className="error-banner">
              {errors.general}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="title">Complaint Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className={errors.title ? 'error' : ''}
              placeholder="Brief summary of the issue..."
              maxLength="200"
            />
            {errors.title && <span className="error-text">{errors.title}</span>}
            <span className="char-count">{formData.title.length}/200</span>
          </div>

          <div className="form-group">
            <label htmlFor="description">Detailed Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className={errors.description ? 'error' : ''}
              placeholder="Provide detailed information about the issue..."
              rows="6"
              maxLength="1000"
            />
            {errors.description && <span className="error-text">{errors.description}</span>}
            <span className="char-count">{formData.description.length}/1000</span>
          </div>

          <div className="form-row">
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

            <div className="form-group">
              <label htmlFor="priority">Priority Level *</label>
              <select
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
              >
                {priorities.map(p => (
                  <option key={p.value} value={p.value}>
                    {p.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

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

          <div className="form-actions">
            <button
              type="button"
              onClick={() => navigate('/complaints')}
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
              {loading ? 'Submitting...' : 'Submit Complaint'}
            </button>
          </div>
        </form>

        <div className="form-info">
          <h3>📌 Guidelines</h3>
          <ul>
            <li>Provide clear and specific details about the issue</li>
            <li>Select the correct building and category</li>
            <li>Set appropriate priority level</li>
            <li>You'll receive updates on the resolution status</li>
            <li>Admin team will review within 24-48 hours</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ComplaintForm;

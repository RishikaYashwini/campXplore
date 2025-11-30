// Complaint List & Management - Full Version
// Location: src/components/Complaints/ComplaintList.jsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { complaintsAPI } from '../../services/api';
import { 
  formatDate, 
  getStatusColor, 
  getStatusText,
  getPriorityColor,
  getPriorityText,
  showToast,
  getErrorMessage,
  isAdmin
} from '../../utils/helpers';
import './Complaints.css';

function ComplaintList({ user }) {
  const [complaints, setComplaints] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterCategory, setFilterCategory] = useState('all');

  useEffect(() => {
    fetchComplaints();
    fetchStats();
  }, []);

  const fetchComplaints = async () => {
    try {
      const response = await complaintsAPI.getAll();
      setComplaints(response.data.complaints || []);
    } catch (error) {
      console.error('Error fetching complaints:', error);
      showToast('Failed to load complaints', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await complaintsAPI.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleViewDetails = async (complaintId) => {
    try {
      const response = await complaintsAPI.getById(complaintId);
      setSelectedComplaint(response.data.complaint);
    } catch (error) {
      showToast('Failed to load complaint details', 'error');
    }
  };

  const handleUpdateStatus = async (complaintId, newStatus, adminResponse) => {
    try {
      await complaintsAPI.update(complaintId, {
        status: newStatus,
        admin_response: adminResponse
      });

      showToast('Complaint updated successfully', 'success');
      setSelectedComplaint(null);
      fetchComplaints();
      fetchStats();
    } catch (error) {
      showToast(getErrorMessage(error), 'error');
    }
  };

  const filteredComplaints = complaints.filter(complaint => {
    if (filterStatus !== 'all' && complaint.status !== filterStatus) return false;
    if (filterCategory !== 'all' && complaint.category !== filterCategory) return false;
    return true;
  });

  const categories = [...new Set(complaints.map(c => c.category))];

  if (loading) {
    return (
      <div className="complaints-container">
        <div className="loading">Loading complaints...</div>
      </div>
    );
  }

  return (
    <div className="complaints-container">
      {/* Header */}
      <div className="complaints-header">
        <div>
          <h1>📝 My Complaints</h1>
          <p>Track and manage your submitted complaints</p>
        </div>
        <Link to="/complaints/new" className="btn btn-primary">
          + New Complaint
        </Link>
      </div>

      {/* Statistics */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#f39c12' }}>📊</div>
            <div className="stat-content">
              <h3>{stats.total}</h3>
              <p>Total Complaints</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#3498db' }}>⏳</div>
            <div className="stat-content">
              <h3>{stats.open}</h3>
              <p>Open</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#f39c12' }}>🔄</div>
            <div className="stat-content">
              <h3>{stats.in_progress}</h3>
              <p>In Progress</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#27ae60' }}>✅</div>
            <div className="stat-content">
              <h3>{stats.resolved}</h3>
              <p>Resolved</p>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="filters-bar">
        <div className="filter-group">
          <label>Status:</label>
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="all">All Status</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Category:</label>
          <select value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)}>
            <option value="all">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        <div className="filter-results">
          Showing {filteredComplaints.length} of {complaints.length} complaints
        </div>
      </div>

      {/* Complaints List */}
      {filteredComplaints.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📭</div>
          <h3>No complaints found</h3>
          <p>You haven't submitted any complaints yet</p>
          <Link to="/complaints/new" className="btn btn-primary">
            Submit Your First Complaint
          </Link>
        </div>
      ) : (
        <div className="complaints-list">
          {filteredComplaints.map(complaint => (
            <div key={complaint.complaint_id} className="complaint-card">
              <div className="complaint-header">
                <div className="complaint-title">
                  <h3>{complaint.title}</h3>
                  <span className="complaint-id">#{complaint.complaint_id}</span>
                </div>
                <div className="complaint-badges">
                  <span 
                    className="badge badge-status"
                    style={{ background: getStatusColor(complaint.status) }}
                  >
                    {getStatusText(complaint.status)}
                  </span>
                  <span 
                    className="badge badge-priority"
                    style={{ background: getPriorityColor(complaint.priority) }}
                  >
                    {getPriorityText(complaint.priority)}
                  </span>
                </div>
              </div>

              <div className="complaint-meta">
                <span className="meta-item">
                  <strong>Category:</strong> {complaint.category}
                </span>
                <span className="meta-item">
                  <strong>Building:</strong> {complaint.building_name}
                </span>
                <span className="meta-item">
                  <strong>Submitted:</strong> {formatDate(complaint.created_at)}
                </span>
              </div>

              <p className="complaint-description">
                {complaint.description.substring(0, 150)}
                {complaint.description.length > 150 ? '...' : ''}
              </p>

              {complaint.admin_response && (
                <div className="admin-response">
                  <strong>Admin Response:</strong>
                  <p>{complaint.admin_response}</p>
                </div>
              )}

              <button
                onClick={() => handleViewDetails(complaint.complaint_id)}
                className="btn btn-secondary btn-sm"
              >
                View Details
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Details Modal */}
      {selectedComplaint && (
        <ComplaintDetailsModal
          complaint={selectedComplaint}
          isAdmin={isAdmin(user)}
          onClose={() => setSelectedComplaint(null)}
          onUpdate={handleUpdateStatus}
        />
      )}
    </div>
  );
}

// Complaint Details Modal Component
function ComplaintDetailsModal({ complaint, isAdmin, onClose, onUpdate }) {
  const [adminResponse, setAdminResponse] = useState(complaint.admin_response || '');
  const [newStatus, setNewStatus] = useState(complaint.status);

  const handleUpdate = () => {
    onUpdate(complaint.complaint_id, newStatus, adminResponse);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Complaint Details</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          <div className="detail-row">
            <strong>ID:</strong>
            <span>#{complaint.complaint_id}</span>
          </div>

          <div className="detail-row">
            <strong>Title:</strong>
            <span>{complaint.title}</span>
          </div>

          <div className="detail-row">
            <strong>Description:</strong>
            <p>{complaint.description}</p>
          </div>

          <div className="detail-row">
            <strong>Category:</strong>
            <span>{complaint.category}</span>
          </div>

          <div className="detail-row">
            <strong>Priority:</strong>
            <span 
              className="badge"
              style={{ background: getPriorityColor(complaint.priority) }}
            >
              {getPriorityText(complaint.priority)}
            </span>
          </div>

          <div className="detail-row">
            <strong>Building:</strong>
            <span>{complaint.building_name}</span>
          </div>

          <div className="detail-row">
            <strong>Status:</strong>
            <span 
              className="badge"
              style={{ background: getStatusColor(complaint.status) }}
            >
              {getStatusText(complaint.status)}
            </span>
          </div>

          <div className="detail-row">
            <strong>Submitted:</strong>
            <span>{formatDate(complaint.created_at)}</span>
          </div>

          {isAdmin && (
            <>
              <div className="detail-row">
                <strong>Update Status:</strong>
                <select value={newStatus} onChange={(e) => setNewStatus(e.target.value)}>
                  <option value="open">Open</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              <div className="detail-row">
                <strong>Admin Response:</strong>
                <textarea
                  value={adminResponse}
                  onChange={(e) => setAdminResponse(e.target.value)}
                  rows="4"
                  placeholder="Provide response or update..."
                />
              </div>

              <button onClick={handleUpdate} className="btn btn-primary">
                Update Complaint
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default ComplaintList;

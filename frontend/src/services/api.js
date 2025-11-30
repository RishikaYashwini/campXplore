// API Service - Axios wrapper for backend communication
// Location: src/services/api.js

import axios from 'axios';

// Base API URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for cookies/sessions
});

// Request interceptor - add auth token if needed
api.interceptors.request.use(
  (config) => {
    // You can add headers here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.data);

      // Handle 401 Unauthorized
      if (error.response.status === 401) {
        // Redirect to login or clear session
        localStorage.removeItem('user');
      }
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// ============================================================================
// AUTHENTICATION APIs
// ============================================================================

export const authAPI = {
  // Register new user
  register: (userData) => api.post('/api/auth/register', userData),

  // Login
  login: (credentials) => api.post('/api/auth/login', credentials),

  // Logout
  logout: () => api.post('/api/auth/logout'),

  // Get current user
  getCurrentUser: () => api.get('/api/auth/me'),

  // Check authentication status
  checkAuth: () => api.get('/api/auth/check'),
};

// ============================================================================
// BUILDINGS APIs
// ============================================================================

export const buildingsAPI = {
  // Get all buildings
  getAll: () => api.get('/api/buildings'),

  // Get specific building
  getById: (id) => api.get(`/api/buildings/${id}`),

  // Search buildings
  search: (query) => api.get(`/api/buildings/search?q=${query}`),
};

// ============================================================================
// NAVIGATION APIs
// ============================================================================

export const navigationAPI = {
  // Get all paths
  getPaths: () => api.get('/api/navigation/paths'),

  // Calculate route
  calculateRoute: (startBuildingId, endBuildingId) => 
    api.post('/api/navigation/route', { start_building_id: startBuildingId, end_building_id: endBuildingId }),

  // Get nearby buildings
  getNearby: (buildingId) => api.get(`/api/navigation/nearby/${buildingId}`),

  // Get all waypoints
  getWaypoints: () => api.get('/api/navigation/waypoints'),
};


// ============================================================================
// COMPLAINTS APIs
// ============================================================================

export const complaintsAPI = {
  // Get user's complaints
  getAll: (params = {}) => api.get('/api/complaints', { params }),

  // Get specific complaint
  getById: (id) => api.get(`/api/complaints/${id}`),

  // Submit complaint
  create: (complaintData) => api.post('/api/complaints', complaintData),

  // Update complaint (admin)
  update: (id, updateData) => api.put(`/api/complaints/${id}`, updateData),

  // Delete complaint
  delete: (id) => api.delete(`/api/complaints/${id}`),

  // Get user statistics
  getStats: () => api.get('/api/complaints/stats'),
};

// ============================================================================
// FEEDBACK APIs
// ============================================================================

export const feedbackAPI = {
  // Get all feedback
  getAll: (params = {}) => api.get('/api/feedback', { params }),

  // Get specific feedback
  getById: (id) => api.get(`/api/feedback/${id}`),

  // Submit feedback
  create: (feedbackData) => api.post('/api/feedback', feedbackData),

  // Get building feedback
  getByBuilding: (buildingId) => api.get(`/api/feedback/building/${buildingId}`),

  // Get user's feedback
  getMyFeedback: () => api.get('/api/feedback/my-feedback'),

  // Get feedback summary
  getSummary: () => api.get('/api/feedback/summary'),
};

// ============================================================================
// ANALYTICS APIs (Admin only)
// ============================================================================

export const analyticsAPI = {
  // Get dashboard stats
  getDashboard: () => api.get('/api/analytics/dashboard'),

  // Get complaint analytics
  getComplaintAnalytics: () => api.get('/api/analytics/complaints'),

  // Get feedback analytics
  getFeedbackAnalytics: () => api.get('/api/analytics/feedback'),

  // Get building analytics
  getBuildingAnalytics: (buildingId) => 
    api.get(`/api/analytics/buildings/${buildingId}`),

  // Export complaints
  exportComplaints: () => api.get('/api/analytics/export/complaints'),
};

// Export default api instance for custom requests
export default api;

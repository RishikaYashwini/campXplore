// Helper Utilities
// Location: src/utils/helpers.js

// ============================================================================
// DATE & TIME UTILITIES
// ============================================================================

export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';

  const date = new Date(dateString);
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };

  return date.toLocaleDateString('en-US', options);
};

export const formatDateOnly = (dateString) => {
  if (!dateString) return 'N/A';

  const date = new Date(dateString);
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric'
  };

  return date.toLocaleDateString('en-US', options);
};

export const getTimeAgo = (dateString) => {
  if (!dateString) return 'N/A';

  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) return 'Just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;

  return formatDateOnly(dateString);
};

// ============================================================================
// VALIDATION UTILITIES
// ============================================================================

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const validatePassword = (password) => {
  return password && password.length >= 6;
};

export const validateRating = (rating) => {
  return rating >= 1 && rating <= 5;
};

// ============================================================================
// STATUS & PRIORITY UTILITIES
// ============================================================================

export const getStatusColor = (status) => {
  const colors = {
    'open': '#f39c12',
    'in_progress': '#3498db',
    'resolved': '#27ae60',
    'closed': '#95a5a6'
  };
  return colors[status] || '#95a5a6';
};

export const getStatusText = (status) => {
  const texts = {
    'open': 'Open',
    'in_progress': 'In Progress',
    'resolved': 'Resolved',
    'closed': 'Closed'
  };
  return texts[status] || status;
};

export const getPriorityColor = (priority) => {
  const colors = {
    'low': '#95a5a6',
    'medium': '#f39c12',
    'high': '#e74c3c',
    'urgent': '#c0392b'
  };
  return colors[priority] || '#95a5a6';
};

export const getPriorityText = (priority) => {
  const texts = {
    'low': 'Low',
    'medium': 'Medium',
    'high': 'High',
    'urgent': 'Urgent'
  };
  return texts[priority] || priority;
};

// ============================================================================
// RATING UTILITIES
// ============================================================================

export const getRatingColor = (rating) => {
  if (rating >= 4) return '#27ae60';
  if (rating >= 3) return '#f39c12';
  return '#e74c3c';
};

export const renderStars = (rating) => {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating);
};

// ============================================================================
// DISTANCE UTILITIES
// ============================================================================

export const formatDistance = (meters) => {
  if (meters < 1000) {
    return `${Math.round(meters)}m`;
  }
  return `${(meters / 1000).toFixed(2)}km`;
};

export const formatTime = (minutes) => {
  if (minutes < 60) {
    return `${minutes} min`;
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return `${hours}h ${mins}m`;
};

// ============================================================================
// USER UTILITIES
// ============================================================================

export const getUserFromStorage = () => {
  try {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  } catch (error) {
    console.error('Error getting user from storage:', error);
    return null;
  }
};

export const saveUserToStorage = (user) => {
  try {
    localStorage.setItem('user', JSON.stringify(user));
  } catch (error) {
    console.error('Error saving user to storage:', error);
  }
};

export const removeUserFromStorage = () => {
  localStorage.removeItem('user');
};

export const isAdmin = (user) => {
  return user && user.role === 'admin';
};

// ============================================================================
// ERROR HANDLING
// ============================================================================

export const getErrorMessage = (error) => {
  if (error.response) {
    // Server responded with error
    return error.response.data.error || error.response.data.message || 'An error occurred';
  } else if (error.request) {
    // No response from server
    return 'Unable to connect to server. Please check your connection.';
  } else {
    // Other errors
    return error.message || 'An unexpected error occurred';
  }
};

// ============================================================================
// TOAST NOTIFICATIONS
// ============================================================================

export const showToast = (message, type = 'info') => {
  // Simple toast implementation
  // Can be replaced with a library like react-toastify
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
    color: white;
    border-radius: 5px;
    z-index: 9999;
    animation: slideIn 0.3s ease-out;
  `;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => document.body.removeChild(toast), 300);
  }, 3000);
};

// ============================================================================
// DEBOUNCE UTILITY
// ============================================================================

export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// ============================================================================
// EXPORTS
// ============================================================================

export default {
  formatDate,
  formatDateOnly,
  getTimeAgo,
  validateEmail,
  validatePassword,
  validateRating,
  getStatusColor,
  getStatusText,
  getPriorityColor,
  getPriorityText,
  getRatingColor,
  renderStars,
  formatDistance,
  formatTime,
  getUserFromStorage,
  saveUserToStorage,
  removeUserFromStorage,
  isAdmin,
  getErrorMessage,
  showToast,
  debounce
};

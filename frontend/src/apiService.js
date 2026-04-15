import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config) => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.token) {
      config.headers.Authorization = `Bearer ${user.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API Service methods
const apiService = {
  // Authentication
  async register(name, email, password) {
    try {
      const response = await apiClient.post('/register', {
        name,
        email,
        password,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Registration failed',
      };
    }
  },

  async login(email, password) {
    try {
      const response = await apiClient.post('/login', {
        email,
        password,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed',
      };
    }
  },

  // File Upload
  async uploadFile(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'File upload failed',
      };
    }
  },

  // Generate Summary
  async generateSummary(text, userId, options) {
    try {
      const response = await apiClient.post('/generate', {
        text,
        user_id: userId,
        input_type: options.inputType || 'text',
        length: options.length || 'medium',
        format: options.format || 'paragraph',
        include_qa: options.includeQA || false,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Summary generation failed',
      };
    }
  },

  // History
  async getHistory(userId) {
    try {
      const response = await apiClient.get(`/history/${userId}`);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to retrieve history',
      };
    }
  },

  // Download Summary
  async downloadSummary(summaryId, format = 'txt') {
    try {
      const response = await apiClient.get(`/download/${summaryId}`, {
        params: { format },
        responseType: format === 'pdf' ? 'blob' : 'text',
      });

      // Create download link
      const url = window.URL.createObjectURL(
        format === 'pdf' 
          ? new Blob([response.data], { type: 'application/pdf' })
          : new Blob([response.data], { type: 'text/plain' })
      );
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `summary.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Download failed',
      };
    }
  },
};

export default apiService;
import axios, { InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to attach the JWT token
apiClient.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error: any) => Promise.reject(error)
);

// Add a response interceptor to handle 401 Unauthorized
apiClient.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: AxiosError) => {
        // If the error is 401 and we aren't already on the login page
        if (error.response?.status === 401 && window.location.pathname !== '/login') {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default apiClient;

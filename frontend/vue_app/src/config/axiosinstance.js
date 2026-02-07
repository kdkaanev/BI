import axios from 'axios';


const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/';
const ACCESS_TOKEN_KEY = 'bi_saas_token';

const axiosBI = axios.create({
    baseURL: BASE_URL,
   
  
   
});


axiosBI.interceptors.request.use((config) => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
}); 

axiosBI.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (
        error.response && 
        error.response.status === 401 &&
        !window.location.href.includes('/login')
    ) {
        // Handle unauthorized access, e.g., redirect to login
        window.location.href = '/login';
    }
    return Promise.reject(error);
});

export default axiosBI;
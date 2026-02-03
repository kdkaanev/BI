import axiosBI from "../config/axiosinstance";

import { ref } from "vue";
import { jwtDecode } from "jwt-decode";

export const useAuthService = () => {
    const user = ref(null);

    const login = async (credentials) => {
        try {
            const response = await axiosBI.post('api/accounts/login/', credentials);
            const accessToken = response.data.access;
            const refreshToken = response.data.refresh;
            const decodedToken = jwtDecode(accessToken);
           

         
            return { accessToken, refreshToken, decodedToken };
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('bi_saas_token');
        user.value = null;
        window.location.href = '/login';
    };

    const getCurrentUser = () => {
        if (!user.value) {
            const token = localStorage.getItem('bi_saas_token');
            if (token) {
                user.value = jwtDecode(token);
            }
        }
        return user.value;
    };

    const register = async (userInfo) => {
        try {
            const response = await axiosBI.post('api/accounts/register/', userInfo);
            return response;
        } catch (error) {
            throw error;
        }
    };  

    return {
        login,
        logout,
        getCurrentUser,
        register,
        user,
    };
};  
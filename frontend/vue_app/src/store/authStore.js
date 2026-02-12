import { defineStore } from 'pinia'
import { ref } from 'vue'
import axiosBI from '../config/axiosinstance'
import { jwtDecode } from 'jwt-decode'

import { useRouter } from 'vue-router'
import { useAuthService } from '../services/authServices'

export const useAuthStore = defineStore('auth', () => {
const router = useRouter()
    const accessToken = ref(null)
    const refreshToken = ref(null)
    const user = ref(null)
    const isInitialized = ref(false)

    const loginUser = async (credentials) => {
        try {
             const { accessToken: access, refreshToken: refresh, decodedToken } = await useAuthService().login(credentials)
            accessToken.value = access
            console.log('REFRESH TOKEN:', refresh)
            console.log('DECODED TOKEN:', decodedToken)
            console.log('ACCESS TOKEN:', access)
            refreshToken.value = refresh
            user.value = decodedToken
            localStorage.setItem('bi_saas_token', access)
            return { accessToken: access, refreshToken: refresh, decodedToken } 
        } catch (error) {
            throw error 
        }
    }

    const logout = () => {
        localStorage.removeItem('bi_saas_token')
        user.value = null
        accessToken.value = null
        refreshToken.value = null 
        router.push('/login')
        
    }

    const getCurrentUser = () => {
        if (!user.value) {
            const token = localStorage.getItem('bi_saas_token')
            if (token) {
                user.value = jwtDecode(token)
            }
        }
        return user.value
    }

    const registerUser = async (userInfo) => {
        try {
            const response = await useAuthService().register(userInfo)
            return response
        } catch (error) {
            throw error
        }
    }

    return {
        loginUser,
        logout,
        getCurrentUser,
        registerUser,
        user,
    }
})  
import { defineStore } from "pinia";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthService } from "../services/authServices";

export const useAuthStore = defineStore("auth", () => {
  const router = useRouter();
  const authService = useAuthService();

  const accessToken = ref(null);
  const refreshToken = ref(null);
  const user = ref(null);
  const isInitialized = ref(false);

  const loginUser = async (credentials) => {
    try {
      const { accessToken: access, refreshToken: refresh } =
        await authService.login(credentials);

      accessToken.value = access;
      refreshToken.value = refresh;

      // взимаме реалния user от /me
      user.value = await authService.fetchMe();

      router.push("/upload");
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem("bi_saas_token");
    localStorage.removeItem("bi_saas_refresh");

    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;

    router.push("/");
  };

  const initAuth = async () => {
    const token = localStorage.getItem("bi_saas_token");

    if (!token) {
      isInitialized.value = true;
      return;
    }

    accessToken.value = token;

    try {
      user.value = await authService.fetchMe();
    } catch {
      logout();
    }

    isInitialized.value = true;
  };

  const registerUser = async (userInfo) => {
    return await authService.register(userInfo);
  };

  return {
    loginUser,
    logout,
    initAuth,
    registerUser,
    user,
    isInitialized,
  };
});

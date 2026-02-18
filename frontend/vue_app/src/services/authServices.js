import axiosBI from "../config/axiosinstance";

export const useAuthService = () => {

  const login = async (credentials) => {
    const response = await axiosBI.post("api/accounts/login/", credentials);

    const accessToken = response.data.access;
    const refreshToken = response.data.refresh;

    localStorage.setItem("bi_saas_token", accessToken);
    localStorage.setItem("bi_saas_refresh", refreshToken);

    return { accessToken, refreshToken };
  };

  const fetchMe = async () => {
    const response = await axiosBI.get("api/accounts/me/");
    return response.data;
  };

  const register = async (userInfo) => {
    return await axiosBI.post("api/accounts/register/", userInfo);
  };

  return {
    login,
    fetchMe,
    register,
  };
};

import { API_ROUTES } from "../utils/constants";
import axios from "axios";
export function storeTokenInLocalStorage(token) {
  localStorage.setItem("token", token);
}

export function getTokenFromLocalStorage() {
  return localStorage.getItem("token");
}

export async function getAuthenticatedUser() {
  const defaultReturnObject = { authenticated: false, user: null };
  try {
    const token = getTokenFromLocalStorage();
    if (!token) {
      return defaultReturnObject;
    }
    const response = await axios({
      method: "GET",
      url: "http://127.0.0.1:5005/account/auth",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (err) {
    console.log("getAuthenticatedUser, Something Went Wrong", err);
    return defaultReturnObject;
  }
}

import { LimitSchema, UserCreate, UserRead, UserUpdate } from "@/types/schema";
import axios from "axios";
import ApiUrl from "./url";

export interface LoginData {
  username: string;
  password: string;
}

export function loginApi(data: LoginData) {
  const formData = new FormData();
  formData.set("username", data.username);
  formData.set("password", data.password);
  return axios.post<any>(ApiUrl.Login, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function registerApi(userInfo: UserCreate) {
  return axios.post<UserRead>(ApiUrl.Register, userInfo);
}

export function logoutApi() {
  return axios.post<any>(ApiUrl.Logout);
}

export function getUserInfoApi() {
  return axios.get<UserRead>(ApiUrl.UserInfo);
}

export function getAllUserApi() {
  return axios.get<UserRead[]>(ApiUrl.UserList);
}

export function deleteUserApi(user_id: number) {
  return axios.delete(ApiUrl.UserList + `/${user_id}`);
}

export function resetUserPasswordApi(user_id: number, data: any) {
  return axios.patch(ApiUrl.UserList + `/${user_id}/reset-password`, data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
}

// 修改 api_key
export function updateUserApiKey(user_id: number, data:any) {
  return axios.patch(ApiUrl.updateApiKey + `/${user_id}/set_api_key` , data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export function updateUserLimitApi(user_id: number, limit: LimitSchema) {
  return axios.post(ApiUrl.UserList + `/${user_id}/limit`, limit);
}

// export function updateUserInfoApi(userInfo: Partial<UserUpdate>) {
//   return axios.patch<UserRead>(ApiUrl.UserInfo, userInfo);
// }

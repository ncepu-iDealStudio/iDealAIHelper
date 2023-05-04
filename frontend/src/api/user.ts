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

// 修改密码
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

// 是否开启上下文
export function AllowContest(user_id: number, data:any) {
  return axios.patch(ApiUrl.User + `/${user_id}/allow_context` , data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
}

// 上下文阈值/条数
export function SetThreshold(user_id: number, data:any) {
  return axios.patch(ApiUrl.User + `/${user_id}/set_threshold` , data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
}

// 获取 apiKey 统计
export function getBillingInfoAPI() {
  return axios.get<any>(ApiUrl.Billing_info);
} 

export function updateUserLimitApi(user_id: number, limit: LimitSchema) {
  return axios.post(ApiUrl.UserList + `/${user_id}/limit`, limit);
}

// export function updateUserInfoApi(userInfo: Partial<UserUpdate>) {
//   return axios.patch<UserRead>(ApiUrl.UserInfo, userInfo);
// }

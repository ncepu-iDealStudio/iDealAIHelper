import { LogFilterOptions } from "@/types/schema";
import axios from "axios";


export function getSystemInfoApi() {
  return axios.get("/system/info");
}

export function getRequestStatisticsApi() {
  return axios.get("/system/request_statistics");
}

export function getServerLogsApi(options: LogFilterOptions | null) {
  return axios.post("/system/server_logs", options);
}

export function getProxyLogsApi(options: LogFilterOptions | null) {
  return axios.post("/system/proxy_logs", options);
}

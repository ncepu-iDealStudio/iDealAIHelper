import { ServerStatusSchema } from "@/types/schema";
import axios from "axios";

export function getServerStatusApi() {
  return axios.get<ServerStatusSchema>("/status");
}

import axios from "axios";
import ApiUrl from "./url";

export function getPromptListAPI() {
  return axios.get<any>(ApiUrl.Prompt);
}
import axios from "axios";

export function getPromptListAPI() {
  return axios.get<any>("prompt");
}
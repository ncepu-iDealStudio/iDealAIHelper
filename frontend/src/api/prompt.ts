import axios from "axios";

// get promptList
export function getPromptListAPI() {
  return axios.get<any>("prompt");
}

//add a prompt
export function updateUserLimitApi(data: any) {
  return axios.post("/prompt", data);
}

export function resetChildPromptApi(prompt_id: number, data: any) {
  return axios.patch("/prompt" + `/${prompt_id}`, data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
}

//  delete a prompt
export function deleteChildPromptApi(prompt_id: number) {
  return axios.delete("/prompt" + `/${prompt_id}`);
}

// find prompt by prompt_id 
export function getChildPromptApi(parms: any) {
  return axios.get("/prompt/part-prompt", { params: parms });
}

// 获取父类 根据 父亲 查找子类 prompt
export function getParentPromptApi(parms: any) {
  return axios.get("/prompt/part-prompt", { params: parms });
}


enum ApiUrl {
  Register = "/auth/register",
  Login = "/auth/login",
  Logout = "/auth/logout",
  UserInfo = "/user/me",
  updateApiKey = "user",
  User = "user",
  Prompt = "prompt",
  Billing_info="billing_info",

  Conversation = "/conv",
  Conversationv3 = "/chat",
  Verify = "/verify",
  UserList = "/user",

  ServerStatus = "/status",
  SystemInfo = "/system/info",
  SystemRequestStatistics = "/system/request_statistics",
  ProxyLogs = "/system/proxy_logs",
  ServerLogs = "/system/server_logs"
}

export default ApiUrl;

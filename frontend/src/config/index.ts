const DEFAULT_CONFIG = {
  // 标题
  APP_NAME: "bootstrap",
  // 版本号
  APP_VER: "1.6.8",

  // 内核版本号
  CORE_VER: "1.6.8",

  // 测试接口地址
  API_URL: "http://ai.quwancode.com/api",

  // 请求超时
  TIMEOUT: 10000,

  // TokenName
  TOKEN_NAME: "Token",

  // Token前缀，注意最后有个空格，如不需要需设置空字符串
  TOKEN_PREFIX: "",

  // 追加其他头
  HEADERS: {},

  // 请求是否开启缓存
  REQUEST_CACHE: false,

  PUBLIC_KEY: "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCiWHenSzBtfpH/C6qNkaieZecVxNKjLnlUqJVsGH6lfk+B1nAvGCBoDprHeLQCIIuzYarOTZGRe2PPeV3IBMm0fesK3/mzB/+MOmMdJW9MaGGt5yTC3eKaR7MzIOy84EDP44YLFEX8S7jNCdAzk15ajzGeyLowglXaXP9CIY+fXQIDAQAB",

}

const APP_CONFIG = {
  // 生产接口地址
  API_URL: "http://ai.quwancode.com/api",
}

// 生产环境配置
if (process.env.ENV === 'production') {
  Object.assign(DEFAULT_CONFIG, APP_CONFIG)
}

export default DEFAULT_CONFIG

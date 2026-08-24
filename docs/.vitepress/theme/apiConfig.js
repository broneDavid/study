// 共享配置:API 地址、访问 token、站点 base 前缀
// 所有组件从这里引用,改一处全站生效
export const API_BASE = 'https://hermes.4587693.xyz/quiz'

// 轻量访问 token(防滥用;数组拼接仅防爬虫直接抓取)
export const QUIZ_TOKEN = ['31','b7','a7','46','3f','d9','db','60','c4','ff','30','bd','b9','4e','a1','fa','fd','f4','d3','97','bf','81','ab','7c'].join('')

// 站点 base 前缀(VitePress base=/study/,组件内链接用它拼接,避免硬编码)
export const BASE_URL = import.meta.env.BASE_URL || '/study/'

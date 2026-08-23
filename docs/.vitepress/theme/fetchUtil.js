// 公共 fetch 工具:统一超时 + 错误信息
// 用法: fetchWithTimeout(url, options, timeoutMs=10000)
export async function fetchWithTimeout(url, options = {}, timeoutMs = 10000) {
  const ctl = new AbortController()
  const timer = setTimeout(() => ctl.abort(), timeoutMs)
  try {
    const r = await fetch(url, { ...options, signal: ctl.signal })
    clearTimeout(timer)
    return r
  } catch (e) {
    clearTimeout(timer)
    if (e.name === 'AbortError') {
      throw new Error('连接超时,请检查网络后重试')
    }
    throw e
  }
}

// 答案暂存(sessionStorage):提交失败/超时时保存,刷新后可恢复
export function stashAnswers(key, answers) {
  try {
    sessionStorage.setItem('quiz_draft_' + key, JSON.stringify(answers))
  } catch (e) { /* ignore */ }
}

export function restoreAnswers(key) {
  try {
    const raw = sessionStorage.getItem('quiz_draft_' + key)
    return raw ? JSON.parse(raw) : null
  } catch (e) {
    return null
  }
}

export function clearStash(key) {
  try {
    sessionStorage.removeItem('quiz_draft_' + key)
  } catch (e) { /* ignore */ }
}

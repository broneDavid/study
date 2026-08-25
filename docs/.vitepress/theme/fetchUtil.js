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

// 题目身份 uid: subject|seq|title —— 与后端 store 去重键一致,身份稳定。
// 批改移除已判题、cron 追加新题、advance 换题都不会改变"仍在待批单中的题"的 uid。
export function answerUid(q) {
  return (q.subject || '') + '|' + (q.seq || '') + '|' + (q.title || '')
}

// 答案暂存 v2(localStorage):按题目 uid 存储,部分批改/追加题目后仍能按题恢复。
// 旧版(v1:数组下标 + 题集指纹)在"部分题目批改成功、其余未判"后刷新时整体失配,
// 未判题的答案被丢弃——v2 按 uid 逐题回填,天然正确。v1 草稿直接弃用。
export function stashAnswers(key, answersByUid) {
  try {
    localStorage.setItem('quiz_draft_' + key, JSON.stringify({ v: 2, answers: answersByUid || {} }))
  } catch (e) { /* ignore */ }
}

export function restoreAnswers(key) {
  try {
    const raw = localStorage.getItem('quiz_draft_' + key)
    if (!raw) return null
    const d = JSON.parse(raw)
    if (!d || typeof d !== 'object' || d.v !== 2) return null
    return d.answers || null
  } catch (e) {
    return null
  }
}

export function clearStash(key) {
  try {
    localStorage.removeItem('quiz_draft_' + key)
  } catch (e) { /* ignore */ }
}

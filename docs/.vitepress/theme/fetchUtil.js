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

// 答案暂存(localStorage):提交失败/超时/部分未判时保存,刷新或换标签页后均可恢复。
// 用 localStorage 而非 sessionStorage:跨标签页保留,关标签重开也不丢。
// 带题目指纹(seq 列表):换题后旧草稿不误恢复(否则答案会错位到新题同下标位置)。
// 注意:旧版 sessionStorage 草稿不迁移(指纹格式相同,但仅同标签页会话内有效,过期即弃)。
export function stashAnswers(key, answers, fingerprint) {
  try {
    localStorage.setItem('quiz_draft_' + key, JSON.stringify({ fp: fingerprint || '', answers }))
  } catch (e) { /* ignore */ }
}

export function restoreAnswers(key, fingerprint) {
  try {
    const raw = localStorage.getItem('quiz_draft_' + key)
    if (!raw) return null
    const d = JSON.parse(raw)
    if (!d || typeof d !== 'object') return null
    // 旧格式(纯 answers 对象,无 fp)或指纹不匹配(题目已换)→ 草稿作废,防错位
    if (d.fp === undefined) return null
    if (fingerprint && d.fp !== fingerprint) return null
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

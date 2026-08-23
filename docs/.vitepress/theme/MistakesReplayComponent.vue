<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithTimeout } from './fetchUtil.js'

const API_BASE = 'https://hermes.4587693.xyz/quiz'
const _t = ['31','b7','a7','46','3f','d9','db','60','c4','ff','30','bd','b9','4e','a1','fa','fd','f4','d3','97','bf','81','ab','7c'].join('')

const state = ref('loading')  // loading | ready | error
const items = ref([])         // 未解决错题
const index = ref(0)
const showAnswer = ref(false)  // 是否展开回忆(错题只有题干,回忆自己对错题的解法要点)
const msg = ref('')
const errorMsg = ref('')

const SUBJ_ICONS = { '高等数学': '📘', '机械原理': '⚙️', '英语': '🇬🇧', '炼油化工设备': '🏭' }

async function fetchMistakes() {
  state.value = 'loading'
  errorMsg.value = ''
  try {
    const r = await fetchWithTimeout(`${API_BASE}/mistakes`)
    if (!r.ok) throw new Error('HTTP ' + r.status)
    const d = await r.json()
    items.value = (d.items || []).filter(x => !x.resolved)
    index.value = 0
    showAnswer.value = false
    msg.value = ''
    state.value = 'ready'
  } catch (e) {
    state.value = 'error'
    errorMsg.value = '加载错题失败: ' + e.message
  }
}

async function resolveIt(resolved) {
  const it = items.value[index.value]
  if (!it) return
  try {
    const r = await fetchWithTimeout(`${API_BASE}/mistakes/resolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': _t },
      body: JSON.stringify({ subject: it.subject, point: it.point, resolved }),
    })
    const d = await r.json()
    if (!d.ok) {
      msg.value = '⚠️ ' + (d.result || '操作失败')
      return
    }
    // 移出列表,前进
    items.value.splice(index.value, 1)
    if (index.value >= items.value.length) index.value = 0
    showAnswer.value = false
    msg.value = resolved ? '🎉 已标记解决,从错题本移除' : '🔁 已标记"还不会",继续保持复习'
  } catch (e) {
    msg.value = '❌ 操作失败: ' + e.message
  }
}

function prev() {
  if (index.value > 0) { index.value--; showAnswer.value = false; msg.value = '' }
}
function next() {
  if (index.value < items.value.length - 1) { index.value++; showAnswer.value = false; msg.value = '' }
}

onMounted(fetchMistakes)
</script>

<template>
  <div class="mistakes-wrapper">
    <h2>❌ 错题重练</h2>
    <p class="sub">先回忆解法 → 展开核对 → 自评"记住了/还不会"。标记解决后移出错题本。</p>

    <div v-if="state === 'loading'" class="status">⏳ 加载错题...</div>
    <div v-else-if="state === 'error'" class="status error">
      <p>⚠️ {{ errorMsg }}</p>
      <button @click="fetchMistakes">重试</button>
    </div>

    <div v-else-if="items.length === 0" class="status">
      <p>🎉 太棒了,错题本已清零!</p>
      <p class="hint">没有未解决的错题,继续保持。</p>
    </div>

    <div v-else class="card">
      <div class="counter">{{ index + 1 }} / {{ items.length }}</div>
      <div class="qhead">
        <span class="badge">{{ SUBJ_ICONS[items[index].subject] || '' }} {{ items[index].subject }}</span>
        <span class="date">错于 {{ items[index].date }}</span>
      </div>
      <p class="point"><b>知识点:</b> {{ items[index].point }}</p>

      <!-- 回忆步骤:先隐藏,点按钮展开(模拟"先回忆再核对") -->
      <button v-if="!showAnswer" class="recall-btn" @click="showAnswer = true">
        💭 我已经回忆完毕,展开核对
      </button>
      <div v-else class="answer-box">
        <p>✅ 已展开。回想你的解法要点:是公式记错?条件漏判?还是思路断了?</p>
        <p class="hint">若完全想不起来,建议回对应科目笔记页复习后再来标记。</p>
      </div>

      <div class="actions">
        <button class="btn-no" @click="resolveIt(false)" :disabled="!showAnswer">🔁 还不会</button>
        <button class="btn-yes" @click="resolveIt(true)" :disabled="!showAnswer">✅ 记住了</button>
      </div>
      <p v-if="msg" class="msg">{{ msg }}</p>

      <div class="nav">
        <button class="nav-btn" @click="prev" :disabled="index === 0">← 上一题</button>
        <button class="nav-btn" @click="next" :disabled="index >= items.length - 1">下一题 →</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mistakes-wrapper { max-width: 720px; margin: 0 auto; }
.sub { color: #888; margin-top: -6px; }
.status { padding: 20px; text-align: center; color: #666; }
.status.error { color: #d93025; }
.hint { font-size: 13px; color: #999; }
.card { border: 1px solid #e0e0e0; border-radius: 12px; padding: 18px; margin: 14px 0; background: #fff; }
.counter { font-size: 12px; color: #999; text-align: right; }
.qhead { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.badge { background: #f56c6c; color: #fff; padding: 3px 12px; border-radius: 12px; font-size: 13px; }
.date { font-size: 12px; color: #999; }
.point { font-size: 16px; font-weight: 600; margin: 10px 0; line-height: 1.5; }
.recall-btn { width: 100%; background: #f0f0f0; color: #444; border: 1px dashed #bbb; border-radius: 10px; padding: 14px; font-size: 14px; cursor: pointer; }
.answer-box { background: #f9f9f9; border: 1px solid #eee; border-radius: 10px; padding: 14px; font-size: 14px; color: #555; }
.actions { display: flex; gap: 12px; margin-top: 14px; }
.actions button { flex: 1; padding: 14px; border: none; border-radius: 10px; font-size: 15px; cursor: pointer; }
.btn-no { background: #fff; color: #e6a23c; border: 2px solid #e6a23c !important; }
.btn-yes { background: #3eaf7c; color: #fff; }
.actions button:disabled { opacity: .4; cursor: not-allowed; }
.msg { font-size: 13px; color: #3eaf7c; margin-top: 10px; text-align: center; }
.nav { display: flex; justify-content: space-between; margin-top: 14px; }
.nav-btn { background: #fff; color: #666; border: 1px solid #ddd; border-radius: 8px; padding: 8px 16px; font-size: 13px; cursor: pointer; }
.nav-btn:disabled { opacity: .4; cursor: not-allowed; }
</style>

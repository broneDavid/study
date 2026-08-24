<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithTimeout, stashAnswers, restoreAnswers, clearStash } from './fetchUtil.js'
import { API_BASE, QUIZ_TOKEN } from './apiConfig.js'

// 轻量访问 token(集中管理于 apiConfig.js)

const state = ref('loading') // loading | ready | submitting | done | error
const questions = ref([])
const answers = ref({})      // seq -> 用户选择/填答
const date = ref('')
const result = ref('')
const errorMsg = ref('')
const draftNotice = ref('')  // 暂存提示

async function fetchToday() {
  state.value = 'loading'
  errorMsg.value = ''
  try {
    // today 为公开读(无答案),无需 token
    const r = await fetchWithTimeout(`${API_BASE}/today`)
    if (!r.ok) throw new Error('HTTP ' + r.status)
    const d = await r.json()
    date.value = d.date
    questions.value = d.questions
    // 预填答案对象(用数组索引做 key,不依赖 seq——seq 重复时 radio 会同名互斥丢勾选)
    answers.value = {}
    questions.value.forEach((q, qi) => answers.value[qi] = '')
    // 恢复暂存的未提交答案(上次提交失败时存下的)
    const draft = restoreAnswers(date.value || 'today')
    if (draft && Object.keys(draft).length) {
      let restored = 0
      questions.value.forEach((q, qi) => {
        if (draft[qi]) { answers.value[qi] = draft[qi]; restored++ }
      })
      if (restored > 0) draftNotice.value = `📝 已恢复上次未提交的 ${restored} 题答案,可直接提交或修改`
    }
    state.value = 'ready'
  } catch (e) {
    state.value = 'error'
    errorMsg.value = '加载题目失败: ' + e.message
  }
}

async function submit() {
  // 组装答案文本: 选择题用字母, 问答题用文本(放括号里)
  // 答案槽位按索引存;提交时按题目实际 seq 编号(后端已保证 seq 唯一)
  const parts = []
  questions.value.forEach((q, qi) => {
    const a = (answers.value[qi] || '').trim()
    if (!a) return
    if (q.type === 'choice') parts.push(`${q.seq}${a.toUpperCase()}`)
    else parts.push(`${q.seq}${a}`)
  })
  if (parts.length === 0) return
  const answerText = '答案：' + parts.join(' ')

  state.value = 'submitting'
  // 提交前先暂存(万一失败刷新后不丢答案)
  stashAnswers(date.value || 'today', answers.value)
  try {
    const r = await fetchWithTimeout(`${API_BASE}/grade`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': QUIZ_TOKEN },
      body: JSON.stringify({ answer: answerText }),
    }, 15000) // 批改可能较慢,给 15s
    const d = await r.json()
    result.value = d.result || '(无结果)'
    state.value = 'done'
    if (d.ok) clearStash(date.value || 'today')
  } catch (e) {
    state.value = 'error'
    errorMsg.value = '提交失败: ' + e.message + '(答案已暂存,刷新后可恢复,不会丢失)'
  }
}

function isCurrent(q) {
  return q && q.seq === questions.value[questions.value.length - 1]?.seq
}

// 数学符号面板(需求2): 点击插入到当前问答题答案
const MATH_SYMBOLS = ['√', 'π', '±', '×', '÷', '≤', '≥', '∞', '∑', '∫', '≠', '≈', 'θ', 'α', 'β', '°', '²', '³', 'x²', 'x³', 'x^n', '1/2', '-1', '→', 'Δ', 'λ', 'μ', 'π/2', '√x', 'sin', 'cos', 'tan', 'log', 'ln', 'lim']
const currentQaSeq = ref(null)

function insertSymbol(sym, seq) {
  const a = answers.value[seq] || ''
  answers.value[seq] = a + sym
}

function showSymbolPanel(seq) {
  currentQaSeq.value = currentQaSeq.value === seq ? null : seq
}

// 需求3: 下一轮学习 —— 预生成下一批题目(不动学习进度,仅补题)
const advancing = ref(false)
const advanceMsg = ref('')
async function nextRound() {
  if (!confirm('生成下一轮学习题目？\n(需调 AI 出题,约 30-120 秒,请耐心等待)')) return
  advancing.value = true
  advanceMsg.value = ''
  try {
    const r = await fetchWithTimeout(`${API_BASE}/advance`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': QUIZ_TOKEN },
      body: JSON.stringify({ count: 6 }),
    }, 180000) // AI 出题慢,给 3 分钟(此前 10s 超时导致 499 断开)
    const d = await r.json()
    if (d.ok) {
      advanceMsg.value = d.idempotent ? '✅ 已有题目,无需重复生成' : `✅ 下一轮题目已就绪 (${d.pending_now || ''} 道)`
    } else {
      advanceMsg.value = '⚠️ ' + (d.result || '生成失败')
    }
    // 刷新题目
    await fetchToday()
  } catch (e) {
    advanceMsg.value = '❌ 请求失败: ' + e.message
  }
  advancing.value = false
}

onMounted(fetchToday)
</script>

<template>
  <div class="quiz-wrapper">
    <h2>📝 每日在线小测</h2>
    <p class="sub">学习系统实时出题 · 网页答题 · AI 自动批改并写入学习进度</p>

    <div v-if="state === 'loading'" class="status">⏳ 加载今日题目...</div>
    <div v-else-if="state === 'error'" class="status error">
      <p>⚠️ {{ errorMsg }}</p>
      <p class="hint">若长时间加载失败,可能是学习服务(AI后端)未运行。可稍后再试。</p>
      <button @click="fetchToday">重试</button>
    </div>

    <template v-else-if="state === 'ready' || state === 'submitting'">
      <p v-if="draftNotice" class="draft-notice">{{ draftNotice }}</p>
      <p v-if="questions.length === 0" class="status">
        今天暂时没有待批改的小测题。<br>
        小测每天 08:00 由学习系统 @Studyingschedulebot 自动出题,答过的题会自动批改。<br>
        你也可点击下方「⏭️ 下一轮学习」生成新题练手。
      </p>

      <div v-for="(q, qi) in questions" :key="q.seq" class="question">
        <div class="qhead">
          <span class="badge">{{ q.subject }}</span>
          <span class="qtype">{{ q.type === 'choice' ? '选择题' : '问答题' }}</span>
        </div>
        <p class="qtext"><b>[{{ q.seq }}]</b> {{ q.q || q.title }}</p>

        <!-- 选择题 -->
        <div v-if="q.type === 'choice'" class="options">
          <label v-for="(opt, key) in q.options" :key="key"
                 class="opt" :class="{ selected: answers[qi] === key }">
            <!-- name 用索引 qi 保证唯一(seq 重复时同名 radio 会互斥丢勾选) -->
            <input type="radio" :name="'q' + qi" :value="key"
                   :checked="answers[qi] === key"
                   :disabled="state === 'submitting'"
                   @change="answers[qi] = key" />
            <span class="opt-key">{{ key }}</span>
            <span class="opt-text">{{ opt }}</span>
          </label>
        </div>
        <!-- 问答题 -->
        <div v-else class="qa-area">
          <div class="sym-toolbar">
            <button type="button" class="sym-toggle" @click="showSymbolPanel(qi)">
              ➗ 数学符号
            </button>
          </div>
          <!-- v-show 而非 v-if:面板在挂载时即渲染(仅隐藏),避免 iPad WebKit
               首次 v-if 插入时符号空白、点击后才显示的渲染 bug -->
          <!-- 符号面板:用 visibility 常驻渲染(不 display:none),iOS 首次展开即显示全部字形 -->
          <div :class="['sym-panel', { open: currentQaSeq === qi }]">
            <button v-for="s in MATH_SYMBOLS" :key="s" type="button"
                    class="sym-btn" @click="insertSymbol(s, qi)">{{ s }}</button>
          </div>
          <textarea :placeholder="'在此输入你的作答...'"
                    rows="3" :disabled="state === 'submitting'"
                    v-model="answers[qi]"></textarea>
        </div>
      </div>

      <div class="actions" v-if="questions.length > 0">
        <button :disabled="state === 'submitting'" @click="submit">
          {{ state === 'submitting' ? 'AI 批改中...' : '✅ 提交批改' }}
        </button>
      </div>

      <div class="advance-area">
        <button class="advance-btn" :disabled="advancing" @click="nextRound">
          {{ advancing ? '⏳ 生成中...' : '⏭️ 下一轮学习' }}
        </button>
        <p v-if="advanceMsg" class="advance-msg">{{ advanceMsg }}</p>
        <p class="hint">点击后调用 AI 生成下一轮练习题(约 30-120 秒,耐心等待;重复点击不会重复生成)。</p>
      </div>
    </template>

    <div v-else-if="state === 'done'" class="result">
      <h3>批改结果</h3>
      <pre>{{ result }}</pre>
      <p class="hint">进度已自动写入学习系统(掌握度↑ / 错题进错题本)。</p>
      <button @click="fetchToday">继续下一批</button>
    </div>
  </div>
</template>

<style scoped>
.quiz-wrapper { max-width: 720px; margin: 0 auto; }
.sub { color: #888; margin-top: -6px; }
.status { padding: 20px; text-align: center; color: #666; }
.status.error { color: #d93025; }
.hint { font-size: 13px; color: #999; }
.draft-notice { background: #fff8e1; border: 1px solid #e6a23c; color: #b26a00; padding: 8px 12px; border-radius: 8px; font-size: 13px; margin: 8px 0; }
.question { border: 1px solid rgba(255,255,255,.6); border-radius: 16px; padding: 16px; margin: 12px 0; background: rgba(255,255,255,.72); box-shadow: 0 2px 16px rgba(0,0,0,.06); -webkit-backdrop-filter: saturate(180%) blur(20px); backdrop-filter: saturate(180%) blur(20px); }
.qhead { display: flex; gap: 8px; margin-bottom: 6px; }
.badge { background: rgba(0,113,227,.12); color: #0071e3; color: #fff; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
.qtype { background: #f0f0f0; padding: 2px 10px; border-radius: 12px; font-size: 12px; color: #555; }
.qtext { font-size: 15px; margin: 8px 0; }
.options { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.opt { display: flex; gap: 10px; align-items: center; border: 1px solid rgba(128,128,128,.2); padding: 10px 14px; border-radius: 12px; cursor: pointer; background: rgba(255,255,255,.6); transition: transform .15s ease, border-color .2s ease, background-color .2s ease, box-shadow .2s ease; }
.opt:active { transform: scale(.99); }
.opt.selected { border-color: #0071e3; background: rgba(0,113,227,.08); box-shadow: 0 0 0 1px rgba(0,113,227,.3); }
.opt-key { width: 24px; height: 24px; border-radius: 50%; border: 1.5px solid rgba(128,128,128,.35); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; color: #6e6e73; flex-shrink: 0; transition: all .2s ease; }
.opt.selected .opt-key { background: #0071e3; border-color: #0071e3; color: #fff; transform: scale(1.05); }
.opt-text { font-size: 15px; color: #1d1d1f; line-height: 1.5; }
html.dark .opt { background: rgba(28,28,32,.6); border-color: rgba(255,255,255,.12); }
html.dark .opt.selected { border-color: #0a84ff; background: rgba(10,132,255,.12); }
html.dark .opt-text { color: #f5f5f7; }
.opt:hover { background: #f6f6f6; }
textarea { width: 100%; border: 1px solid #ddd; border-radius: 8px; padding: 8px; font-size: 14px; font-family: inherit; }
.qa-area { display: flex; flex-direction: column; gap: 6px; }
.sym-toolbar { display: flex; justify-content: flex-start; }
.sym-toggle { background: #f0f0f0; color: #444; padding: 5px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; }
.sym-toggle:hover { background: #e4e4e4; }
.sym-panel { display: flex; flex-wrap: wrap; gap: 4px; padding: 6px; background: #fafafa; border: 1px solid #eee; border-radius: 8px; height: 0; margin: 0; overflow: hidden; visibility: hidden; }
.sym-panel.open { height: auto; margin: 0 0 8px; visibility: visible; }
.sym-btn { background: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 4px 8px; font-size: 15px; cursor: pointer; min-width: 36px; font-family: "SF Pro Text", -apple-system, "PingFang SC", "Segoe UI Symbol", "Apple Symbols", sans-serif; }
.sym-btn:hover { background: #0071e3; color: #fff; border-color: #0071e3; }
.actions { text-align: center; margin-top: 16px; }
.advance-area { text-align: center; margin-top: 10px; padding-top: 10px; border-top: 1px dashed #ddd; }
.advance-btn { background: transparent; color: #0071e3; border: 1px solid #0071e3; padding: 8px 20px; border-radius: 8px; font-size: 14px; cursor: pointer; }
.advance-btn:hover { background: #0071e3; color: #fff; }
.advance-msg { color: #0071e3; font-size: 13px; margin-top: 6px; }
button { background: linear-gradient(180deg,#0077ed,#0071e3); color: #fff; border: none; padding: 10px 24px; border-radius: 980px; box-shadow: inset 0 1px 0 rgba(255,255,255,.25), 0 2px 8px rgba(0,113,227,.3); font-size: 15px; cursor: pointer; }
button:hover { opacity: .9; }
button:disabled { opacity: .5; cursor: not-allowed; }
.result { border: 1px solid rgba(0,113,227,.3); border-radius: 14px; padding: 16px; background: rgba(0,113,227,.05); }
.result pre { white-space: pre-wrap; background: #f6f6f6; padding: 12px; border-radius: 8px; }
html.dark .question { background: rgba(28,28,32,.72); border-color: rgba(255,255,255,.1); }
</style>
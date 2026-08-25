<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithTimeout, stashAnswers, restoreAnswers, clearStash, answerUid } from './fetchUtil.js'
import { API_BASE, QUIZ_TOKEN } from './apiConfig.js'

// 轻量访问 token(集中管理于 apiConfig.js)

const state = ref('loading') // loading | ready | submitting | done | error
const questions = ref([])
const answers = ref({})      // seq -> 用户选择/填答
const graded = ref([])       // 今日已批改(含对错/正确答案/解析,刷新后仍可见)
const date = ref('')
const result = ref('')
const errorMsg = ref('')
const draftNotice = ref('')  // 暂存提示

async function fetchToday() {
  state.value = 'loading'
  errorMsg.value = ''
  draftNotice.value = ''
  try {
    // today 为公开读(无答案),无需 token
    const r = await fetchWithTimeout(`${API_BASE}/today`)
    if (!r.ok) throw new Error('HTTP ' + r.status)
    const d = await r.json()
    date.value = d.date
    questions.value = d.questions || []
    graded.value = d.graded || []
    // 预填答案对象(用数组索引做 key,不依赖 seq——seq 重复时 radio 会同名互斥丢勾选)
    answers.value = {}
    questions.value.forEach((q, qi) => answers.value[qi] = '')
    // 恢复暂存的未提交答案(v2 按题 uid 逐条回填:部分批改/追加新题后未判题的答案仍能恢复;
    // 旧版按数组下标+题集指纹,部分批改后整体失配导致答案丢失)
    const draft = restoreAnswers(date.value || 'today')
    if (draft && Object.keys(draft).length) {
      let restored = 0
      questions.value.forEach((q, qi) => {
        const a = draft[answerUid(q)]
        if (a) { answers.value[qi] = a; restored++ }
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
  if (parts.length === 0) {
    draftNotice.value = '⚠️ 请先作答再提交(选择或填写至少一题)'
    return
  }
  draftNotice.value = ''
  const answerText = '答案：' + parts.join(' ')

  state.value = 'submitting'
  // 提交前暂存(v2 按题 uid:部分批改后未判题的答案仍能按题恢复)
  const uidAnswers = {}
  questions.value.forEach((q, qi) => {
    const a = (answers.value[qi] || '').trim()
    if (a) uidAnswers[answerUid(q)] = a
  })
  stashAnswers(date.value || 'today', uidAnswers)
  try {
    const r = await fetchWithTimeout(`${API_BASE}/grade`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': QUIZ_TOKEN },
      body: JSON.stringify({ answer: answerText }),
    }, 90000) // 批改可能较慢(AI 单题最坏 ~65s),给 90s(此前 15s 几乎必然超时)
    const d = await r.json().catch(() => null)
    // 统一契约:成功 {ok:true,result,pending_remaining};失败可能是 HTTPException {detail} 或 {ok:false,result}
    if (!r.ok || !d || d.ok !== true) {
      const msg = d && (d.detail || d.result || d.error)
      throw new Error(msg ? (typeof msg === 'string' ? msg : JSON.stringify(msg)) : ('HTTP ' + r.status))
    }
    result.value = d.result || '(无结果)'
    state.value = 'done'
    // 仅当没有剩余未判题(全部批改完成)才清除草稿;
    // 若仍有未判题(如 AI 暂不可用/部分格式未匹配),保留草稿,刷新后按 uid 自动恢复,避免重填。
    if (d.pending_remaining === 0) {
      clearStash(date.value || 'today')
    } else {
      draftNotice.value = '⚠️ 部分题目未判(AI 暂不可用或格式未匹配),你的答案已保存,可稍后重新提交'
    }
    // 注意:此处不再调用 fetchToday()——旧实现同步把 state 改回 loading,导致
    // "批改结果"页永远不渲染(死代码)。停留 done 页展示完整批改结果,点"继续下一批"再刷新。
  } catch (e) {
    state.value = 'error'
    errorMsg.value = '提交失败: ' + e.message + '(答案已保存,刷新后可恢复;若为连接超时,批改可能仍在后台进行,稍后刷新页面即可看到结果)'
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
  let advOk = false
  try {
    const r = await fetchWithTimeout(`${API_BASE}/advance`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': QUIZ_TOKEN },
      body: JSON.stringify({ count: 6 }),
    }, 180000) // AI 出题慢,给 3 分钟(此前 10s 超时导致 499 断开)
    const d = await r.json().catch(() => null)
    if (!r.ok || !d || d.ok !== true) {
      const msg = d && (d.detail || d.result || d.error)
      throw new Error(msg ? (typeof msg === 'string' ? msg : JSON.stringify(msg)) : ('HTTP ' + r.status))
    }
    advOk = true
    advanceMsg.value = d.idempotent ? '✅ 已有题目,无需重复生成' : `✅ 下一轮题目已就绪 (${d.pending_now || ''} 道)`
    // 刷新题目(生成其实已成功;刷新失败不误报生成失败,提示手动刷新)
    await fetchToday()
  } catch (e) {
    advanceMsg.value = advOk
      ? '✅ 题目已生成,但刷新列表失败: ' + e.message + '(请手动刷新页面查看)'
      : '❌ 请求失败: ' + e.message
  }
  advancing.value = false
}

onMounted(() => {
  fetchToday()
  // 双标签页同步:另一标签页 stash/clear 草稿时,本页自动刷新题目与已批改列表
  window.addEventListener('storage', (e) => {
    if (e.key && e.key.startsWith('quiz_draft_') && state.value !== 'submitting') {
      fetchToday()
    }
  })
})
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

    <template v-else>
      <!-- 今日已批改(含对错/正确答案/解析;刷新后仍可见,不再丢失批改结果) -->
      <div v-if="graded.length" class="graded-section">
        <h3>📊 今日已批改 <span class="graded-count">{{ graded.length }} 道</span></h3>
        <div v-for="g in graded" :key="'g' + g.seq + '_' + (g.at || '')"
             class="question graded-card" :class="g.correct ? 'g-correct' : 'g-wrong'">
          <div class="qhead">
            <span class="badge">{{ g.subject || '未知科目' }}</span>
            <span class="g-mark">{{ g.correct ? '✅ 答对' : '❌ 答错' }}</span>
          </div>
          <p class="qtext"><b>[{{ g.seq }}]</b> {{ g.q || g.title || ('题 #' + g.seq) }}</p>
          <p class="g-note">{{ g.note || (g.correct ? '回答正确' : '回答错误') }}</p>
          <!-- 正确答案: 选择题显示选项字母+内容;问答题显示答案要点 -->
          <div v-if="g.type === 'choice' && g.answer" class="g-answer">
            ✅ 正确答案: <b>{{ g.answer }}.</b> {{ (g.options || {})[g.answer] || '' }}
          </div>
          <div v-else-if="g.answer && g.answer.points && g.answer.points.length" class="g-answer">
            <p class="g-ans-title">✅ 答案要点:</p>
            <ul class="g-ans-list">
              <li v-for="(pt, i) in g.answer.points" :key="i">{{ pt }}</li>
            </ul>
          </div>
          <div v-if="g.solution" class="g-solution">
            <p class="g-ans-title">📝 解题步骤:</p>
            <pre>{{ g.solution }}</pre>
          </div>
        </div>
      </div>

      <template v-if="state === 'ready' || state === 'submitting'">
        <p v-if="draftNotice" class="draft-notice">{{ draftNotice }}</p>
        <p v-if="questions.length === 0" class="status">
          今天暂时没有待批改的小测题。<br>
          小测每天 07:30 / 13:30 / 19:00 由学习系统 @Studyingschedulebot 自动出题,答过的题会自动批改。<br>
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
    </template>
  </div>
</template>

<style scoped>
.quiz-wrapper { max-width: 720px; margin: 0 auto; }
.sub { color: #888; margin-top: -6px; }
.status { padding: 20px; text-align: center; color: #666; }
.status.error { color: #d93025; }
.hint { font-size: 13px; color: #999; }
.draft-notice { background: #fff8e1; border: 1px solid #e6a23c; color: #b26a00; padding: 8px 12px; border-radius: 8px; font-size: 13px; margin: 8px 0; }
.question { border: 1px solid rgba(255,255,255,.6); border-radius: 16px; padding: 16px; margin: 12px 0; background: rgba(255,255,255,.94); box-shadow: 0 2px 16px rgba(0,0,0,.06); }
.qhead { display: flex; gap: 8px; margin-bottom: 6px; }
.badge { background: rgba(0,113,227,.12); color: #0071e3; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
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
textarea { width: 100%; border: 1px solid #ddd; border-radius: 8px; padding: 8px; font-size: 16px; font-family: inherit; }
.qa-area { display: flex; flex-direction: column; gap: 6px; }
.sym-toolbar { display: flex; justify-content: flex-start; }
.sym-toggle { background: #f0f0f0; color: #444; padding: 5px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; }
.sym-toggle:hover { background: #e4e4e4; }
.sym-panel { display: flex; flex-wrap: wrap; gap: 4px; padding: 6px; background: #fafafa; border: 1px solid #eee; border-radius: 8px; height: 0; margin: 0; overflow: hidden; visibility: hidden; }
.sym-panel.open { height: auto; margin: 0 0 8px; visibility: visible; }
.sym-btn { background: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 7px 10px; font-size: 15px; cursor: pointer; min-width: 40px; min-height: 40px; font-family: "SF Pro Text", -apple-system, "PingFang SC", "Segoe UI Symbol", "Apple Symbols", sans-serif; }
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
/* 深色模式覆盖:徽章/类型/草稿提示/符号面板/结果/输入框(挂 html.dark,双轨兼容) */
html.dark .badge { color: #0a84ff; }
html.dark .qtype { background: #2c2c2e; color: #aeaeb2; }
html.dark .draft-notice { background: rgba(255,200,87,.12); border-color: rgba(255,200,87,.35); color: #ffd60a; }
html.dark .sym-toggle { background: #2c2c2e; color: #d0d0d4; }
html.dark .sym-toggle:hover { background: #3a3a3c; }
html.dark .sym-panel { background: #1c1c20; border-color: #2c2c2e; }
html.dark .sym-btn { background: #2c2c2e; border-color: #3a3a3c; color: #f5f5f7; }
html.dark .sym-btn:hover { background: #0a84ff; color: #fff; border-color: #0a84ff; }
html.dark .result pre { background: #1c1c20; color: #f5f5f7; }
html.dark textarea { background: #1c1c20; border-color: #3a3a3c; color: #f5f5f7; }
html.dark .advance-area { border-top-color: #2c2c2e; }

/* 今日已批改区块 */
.graded-section { margin: 4px 0 16px; }
.graded-section h3 { display: flex; align-items: center; gap: 8px; font-size: 17px; margin: 12px 0 4px; }
.graded-count { font-size: 12px; font-weight: 600; color: #6e6e73; background: #f0f0f0; padding: 2px 10px; border-radius: 12px; }
.graded-card { border-left: 4px solid #34c759; }
.graded-card.g-wrong { border-left-color: #ff3b30; }
.g-mark { font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 12px; background: rgba(52,199,89,.12); color: #248a3d; }
.g-wrong .g-mark { background: rgba(255,59,48,.12); color: #d70015; }
.g-note { font-size: 14px; color: #3a3a3c; margin: 6px 0; }
.g-answer { font-size: 14px; color: #1d1d1f; background: rgba(52,199,89,.08); border: 1px solid rgba(52,199,89,.25); border-radius: 10px; padding: 8px 12px; margin: 6px 0; }
.g-ans-title { margin: 0 0 4px; font-weight: 600; }
.g-ans-list { margin: 0; padding-left: 20px; }
.g-ans-list li { margin: 2px 0; }
.g-solution { font-size: 14px; background: rgba(255,149,0,.08); border: 1px solid rgba(255,149,0,.25); border-radius: 10px; padding: 8px 12px; margin: 6px 0; }
.g-solution pre { white-space: pre-wrap; margin: 4px 0 0; font-size: 13px; color: #3a3a3c; font-family: inherit; line-height: 1.6; }
html.dark .graded-count { background: #2c2c2e; color: #aeaeb2; }
html.dark .g-mark { background: rgba(48,209,88,.15); color: #30d158; }
html.dark .g-wrong .g-mark { background: rgba(255,69,58,.15); color: #ff453a; }
html.dark .g-note { color: #d1d1d6; }
html.dark .g-answer { background: rgba(48,209,88,.1); border-color: rgba(48,209,88,.3); color: #f5f5f7; }
html.dark .g-solution { background: rgba(255,159,10,.1); border-color: rgba(255,159,10,.3); }
html.dark .g-solution pre { color: #d1d1d6; }
</style>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchWithTimeout } from './fetchUtil.js'
import { API_BASE, QUIZ_TOKEN } from './apiConfig.js'


const state = ref('loading')  // loading | ready | error
const items = ref([])         // 未解决错题
const expanded = ref({})      // point -> bool
const msg = ref('')
const errorMsg = ref('')

const SUBJECTS = ['高等数学', '机械原理', '英语', '炼油化工设备']
const SUBJ_ICONS = { '高等数学': '📘', '机械原理': '⚙️', '英语': '🇬🇧', '炼油化工设备': '🏭' }

// 按科目分组(每科内按日期倒序)
const grouped = computed(() => {
  return SUBJECTS.map(subj => {
    const list = items.value
      .filter(i => i.subject === subj)
      .sort((a, b) => (b.date || '').localeCompare(a.date || ''))
    return { subject: subj, icon: SUBJ_ICONS[subj] || '📘', count: list.length, list }
  }).filter(g => g.count > 0)
})

async function fetchMistakes() {
  state.value = 'loading'
  errorMsg.value = ''
  try {
    const r = await fetchWithTimeout(`${API_BASE}/mistakes`)
    if (!r.ok) throw new Error('HTTP ' + r.status)
    const d = await r.json()
    items.value = (d.items || []).filter(x => !x.resolved)
    msg.value = ''
    state.value = 'ready'
  } catch (e) {
    state.value = 'error'
    errorMsg.value = '加载错题失败: ' + e.message
  }
}

function toggleExpand(it) {
  expanded.value[it.point] = !expanded.value[it.point]
}

async function resolveIt(it, resolved) {
  try {
    const r = await fetchWithTimeout(`${API_BASE}/mistakes/resolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': QUIZ_TOKEN },
      body: JSON.stringify({ subject: it.subject, point: it.point, resolved }),
    })
    const d = await r.json()
    if (!d.ok) {
      msg.value = '⚠️ ' + (d.result || '操作失败')
      return
    }
    items.value = items.value.filter(x => !(x.subject === it.subject && x.point === it.point))
    delete expanded.value[it.point]
    msg.value = resolved ? '🎉 已标记解决,从错题本移除' : '🔁 已标记"还不会",继续保持复习'
  } catch (e) {
    msg.value = '❌ 操作失败: ' + e.message
  }
}

onMounted(fetchMistakes)
</script>

<template>
  <div class="mistakes-wrapper">
    <h2>❌ 错题本</h2>
    <p class="sub">按科目浏览 · 点击错题前的日期,展开该题的解析。</p>

    <div v-if="state === 'loading'" class="status">⏳ 加载错题...</div>
    <div v-else-if="state === 'error'" class="status error">
      <p>⚠️ {{ errorMsg }}</p>
      <button @click="fetchMistakes">重试</button>
    </div>

    <template v-else>
      <div v-if="items.length === 0" class="status">
        <p>🎉 太棒了,错题本已清零!</p>
        <p class="hint">没有未解决的错题,继续保持。</p>
      </div>

      <template v-else>
        <p v-if="msg" class="msg">{{ msg }}</p>

        <!-- 按科目分组 -->
        <div v-for="g in grouped" :key="g.subject" class="subject-group">
          <h3 class="subject-title">{{ g.icon }} {{ g.subject }}
            <span class="subject-count">{{ g.count }} 题待复习</span>
          </h3>

          <!-- 该科目的错题列表 -->
          <div v-for="it in g.list" :key="it.point" class="card">
            <div class="card-head">
              <!-- 点击日期 → 展开该题及解析 -->
              <button class="date-link" :class="{ open: expanded[it.point] }"
                      @click="toggleExpand(it)">
                📅 {{ it.date }} {{ expanded[it.point] ? '▲' : '▼' }}
              </button>
              <span class="point">{{ it.point }}</span>
            </div>

            <!-- 展开:完整错题 + 解析 -->
            <div v-if="expanded[it.point]" class="detail">
              <!-- 题目:优先错题原文,老错题用知识库例题兜底 -->
              <p v-if="it.q" class="qtext"><b>📋 题目:</b> {{ it.q }}</p>
              <p v-else-if="it.knowledge && it.knowledge.example" class="qtext"><b>📋 题目(知识库例题):</b> {{ it.knowledge.example }}</p>
              <p v-if="it.answer" class="answer-text"><b>✅ 正确答案:</b> {{ it.answer }}</p>
              <p v-if="it.solution" class="solution-text"><b>📝 解析:</b><br>{{ it.solution }}</p>
              <div v-if="it.knowledge && it.knowledge.content" class="knowledge-box">
                <p class="knowledge-title"><b>📚 知识点回顾:</b></p>
                <p class="knowledge-content">{{ it.knowledge.content }}</p>
                <p v-if="it.knowledge.example" class="knowledge-example"><b>例题:</b> {{ it.knowledge.example }}</p>
              </div>
              <p v-if="!it.answer && !it.solution && !(it.knowledge && it.knowledge.content)" class="hint">
                ⚠️ 暂无答案与解析,建议回对应科目笔记页复习该知识点后再标记。
              </p>
              <div class="actions">
                <button class="btn-no" @click="resolveIt(it, false)">🔁 还不会</button>
                <button class="btn-yes" @click="resolveIt(it, true)">✅ 记住了</button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </template>
  </div>
</template>

<style scoped>
.mistakes-wrapper { max-width: 720px; margin: 0 auto; }
.sub { color: #888; margin-top: -6px; }
.status { padding: 20px; text-align: center; color: #666; }
.status.error { color: #d93025; }
.hint { font-size: 13px; color: #999; }
.msg { font-size: 13px; color: #3eaf7c; margin: 8px 0; }
.subject-group { margin: 18px 0; }
.subject-title { font-size: 18px; font-weight: 700; border-bottom: 2px solid #eee; padding-bottom: 6px; margin-bottom: 8px; }
.subject-count { font-size: 12px; color: #f56c6c; font-weight: 400; margin-left: 8px; }
.card { border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px 12px; margin: 8px 0; background: #fff; }
.card-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.date-link { background: #fff3e0; border: 1px solid #ffb74d; color: #b26a00; border-radius: 14px; padding: 3px 10px; font-size: 12px; cursor: pointer; white-space: nowrap; }
.date-link.open { background: #ffb74d; color: #fff; }
.point { font-size: 14px; font-weight: 600; color: #333; }
.detail { margin-top: 8px; padding-top: 8px; border-top: 1px dashed #e0e0e0; }
.qtext { font-size: 14px; color: #333; margin: 6px 0; line-height: 1.5; }
.answer-text { font-size: 14px; color: #2e7d32; background: #e8f5e9; border-radius: 6px; padding: 6px 10px; margin: 6px 0; }
.solution-text { font-size: 14px; color: #333; line-height: 1.6; white-space: pre-wrap; }
.knowledge-box { background: #f0f7ff; border: 1px solid #b3d4fc; border-radius: 8px; padding: 10px; margin: 8px 0; }
.knowledge-title { font-size: 14px; color: #1a56db; margin-bottom: 4px; }
.knowledge-content { font-size: 14px; color: #333; line-height: 1.6; }
.knowledge-example { font-size: 13px; color: #555; margin-top: 6px; }
.actions { display: flex; gap: 10px; margin-top: 10px; }
.actions button { flex: 1; padding: 12px; border: none; border-radius: 10px; font-size: 14px; cursor: pointer; }
.btn-no { background: #fff; color: #e6a23c; border: 2px solid #e6a23c !important; }
.btn-yes { background: #3eaf7c; color: #fff; }
</style>

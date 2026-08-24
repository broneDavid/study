<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithTimeout } from './fetchUtil.js'
import { API_BASE, QUIZ_TOKEN } from './apiConfig.js'


const loading = ref(true)
const status = ref(null)
const errorMsg = ref('')
const celebrated = ref(false)  // 全完成庆祝是否已显示(本会话)
const picking = ref(false)     // 是否展开打卡模式选择
const submitting = ref(false)
const checkinMsg = ref('')

const MODES = {
  light: { label: '轻量', desc: '15分钟', color: '#e6a23c' },
  standard: { label: '标准', desc: '30分钟', color: '#3eaf7c' },
  intensive: { label: '加强', desc: '60分钟', color: '#f56c6c' },
  off: { label: '休息', desc: '今天不学', color: '#909399' },
}

async function fetchStatus() {
  loading.value = true
  errorMsg.value = ''
  try {
    const r = await fetchWithTimeout(`${API_BASE}/status`)
    if (!r.ok) throw new Error('HTTP ' + r.status)
    status.value = await r.json()
    loading.value = false
    if (allDone() && !celebrated.value) {
      celebrated.value = true
      setTimeout(() => {
        window.alert('🎉 今日学习全部完成!连续学习 ' + (status.value?.streak_days || 0) + ' 天,继续保持!')
      }, 300)
    }
  } catch (e) {
    loading.value = false
    errorMsg.value = '状态加载失败: ' + e.message
  }
}

async function doCheckin(m) {
  if (submitting.value) return
  submitting.value = true
  checkinMsg.value = ''
  try {
    const r = await fetchWithTimeout(`${API_BASE}/checkin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': QUIZ_TOKEN },
      body: JSON.stringify({ mode: m }),
    })
    const d = await r.json()
    if (d.ok) {
      picking.value = false
      checkinMsg.value = `✅ 打卡成功 · 今日${MODES[m]?.label || m}模式`
      await fetchStatus()  // 刷新全部状态
    } else {
      checkinMsg.value = '⚠️ ' + (d.result || '打卡失败')
    }
  } catch (e) {
    checkinMsg.value = '❌ 请求失败: ' + e.message
  }
  submitting.value = false
}

function allDone() {
  const s = status.value
  return s && s.checkin_done && s.lesson_done && s.quiz_done && s.review_done
}

const MODE_LABELS = { light: '轻量', standard: '标准', intensive: '加强', off: '休息' }
</script>

<template>
  <div class="tasks-wrapper">
    <div v-if="loading" class="status">⏳ 加载今日任务状态...</div>
    <div v-else-if="errorMsg" class="status error">
      <p>⚠️ {{ errorMsg }}</p>
      <button class="retry" @click="fetchStatus">🔄 重试</button>
    </div>
    <template v-else>
      <!-- 全完成横幅 -->
      <div v-if="allDone()" class="all-done-banner">
        🎉 今日学习全部完成!连续学习 {{ status.streak_days }} 天
      </div>
      <div class="summary">
        今日模式:<b>{{ MODE_LABELS[status.mode] || status.mode }}</b>
        · 连续答对 {{ status.streak_correct }} 次
        · 连续学习 {{ status.streak_days }} 天
      </div>

      <div class="grid">
        <!-- 打卡卡:未打卡时点开选模式 -->
        <div class="cell" :class="status.checkin_done ? 'done' : 'todo'">
          <div class="cell-label">☀️ 晨间打卡</div>
          <div v-if="status.checkin_done" class="cell-badge done">✅ 已完成</div>
          <div v-else>
            <div class="cell-badge todo">⏳ 未打卡</div>
            <button v-if="!picking" class="mini-btn" @click="picking = true">选择模式</button>
            <div v-else class="mode-picker">
              <button v-for="(info, key) in MODES" :key="key" class="mode-opt"
                      :style="{ borderColor: info.color, color: info.color }"
                      :disabled="submitting" @click="doCheckin(key)">
                {{ info.label }} {{ info.desc }}
              </button>
              <button class="mode-cancel" @click="picking = false">取消</button>
            </div>
          </div>
        </div>

        <a class="cell link" :class="status.lesson_done ? 'done' : 'todo'" href="/study/daily#today-lesson">
          <div class="cell-label">📚 知识点</div>
          <div class="cell-badge" :class="status.lesson_done ? 'done' : 'todo'">{{ status.lesson_done ? '✅ 已完成' : '⏳ 去完成' }}</div>
        </a>
        <a class="cell link" :class="status.quiz_done ? 'done' : 'todo'" href="/study/quiz">
          <div class="cell-label">📝 每日小测</div>
          <div class="cell-badge" :class="status.quiz_done ? 'done' : 'todo'">{{ status.quiz_done ? '✅ 已完成' : '⏳ 去完成' }}</div>
        </a>
        <a class="cell link" :class="status.review_done ? 'done' : 'todo'" href="/study/mistakes">
          <div class="cell-label">🔁 复盘复习</div>
          <div class="cell-badge" :class="status.review_done ? 'done' : 'todo'">{{ status.review_done ? '✅ 已完成' : '⏳ 去完成' }}</div>
        </a>
      </div>
      <p v-if="checkinMsg" class="checkin-msg">{{ checkinMsg }}</p>
    </template>
  </div>
</template>

<style scoped>
.tasks-wrapper { max-width: 720px; margin: 0 auto; }
.status { padding: 16px; text-align: center; color: #666; }
.status.error { color: #d93025; }
.retry { margin-top: 8px; padding: 6px 16px; border: 1px solid #e6a23c; background: #fff; color: #b26a00; border-radius: 8px; cursor: pointer; }
.all-done-banner { background: linear-gradient(135deg, #e8f5e9, #c8e6c9); border: 1px solid #3eaf7c; border-radius: 10px; padding: 12px; text-align: center; font-size: 15px; font-weight: 700; color: #1b5e20; margin-bottom: 10px; }
.summary { font-size: 13px; color: #666; margin-bottom: 10px; text-align: center; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
.cell { border-radius: 10px; padding: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,.06); display: block; text-decoration: none; color: inherit; }
.cell.done { background: #e8f5e9; border: 1px solid #3eaf7c; }
.cell.todo { background: #fff8e1; border: 1px solid #e6a23c; }
.cell-label { font-size: 14px; }
.cell-badge { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.cell-badge.done { color: #2e7d32; }
.cell-badge.todo { color: #b26a00; }
.mini-btn { margin-top: 4px; padding: 5px 12px; border: none; border-radius: 6px; background: #e6a23c; color: #fff; font-size: 12px; cursor: pointer; }
.mode-picker { display: flex; flex-direction: column; gap: 4px; margin-top: 6px; }
.mode-opt { background: #fff; border: 1.5px solid; border-radius: 6px; padding: 5px; font-size: 12px; cursor: pointer; }
.mode-opt:disabled { opacity: .5; }
.mode-cancel { margin-top: 2px; background: none; border: none; color: #999; font-size: 11px; cursor: pointer; }
.checkin-msg { font-size: 13px; color: #3eaf7c; text-align: center; margin-top: 8px; }
</style>

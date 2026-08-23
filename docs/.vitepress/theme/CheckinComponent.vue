<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithTimeout } from './fetchUtil.js'

const API_BASE = 'https://hermes.4587693.xyz/quiz'
// 与 QuizComponent 相同的访问 token(网页端轻量防滥用)
const _t = ['31','b7','a7','46','3f','d9','db','60','c4','ff','30','bd','b9','4e','a1','fa','fd','f4','d3','97','bf','81','ab','7c'].join('')

const loading = ref(true)
const done = ref(false)
const mode = ref('standard')
const picking = ref(false)
const submitting = ref(false)
const msg = ref('')

const MODES = {
  light: { label: '轻量', desc: '15分钟', color: '#e6a23c' },
  standard: { label: '标准', desc: '30分钟', color: '#3eaf7c' },
  intensive: { label: '加强', desc: '60分钟', color: '#f56c6c' },
  off: { label: '休息', desc: '今天不学', color: '#909399' },
}

async function fetchStatus() {
  loading.value = true
  msg.value = ''
  try {
    const r = await fetchWithTimeout(`${API_BASE}/checkin-status`)
    if (!r.ok) throw new Error('HTTP ' + r.status)
    const d = await r.json()
    done.value = !!d.checkin_done
    mode.value = d.mode || 'standard'
    loading.value = false
  } catch (e) {
    loading.value = false
    msg.value = '状态加载失败:' + e.message
  }
}

async function doCheckin(m) {
  if (submitting.value) return
  submitting.value = true
  msg.value = ''
  try {
    const r = await fetchWithTimeout(`${API_BASE}/checkin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Quiz-Token': _t },
      body: JSON.stringify({ mode: m }),
    })
    const d = await r.json()
    if (d.ok) {
      done.value = true
      mode.value = m
      picking.value = false
      const info = MODES[m] || {}
      msg.value = `✅ 打卡成功 · 今日${info.label || m}模式${info.desc ? '(' + info.desc + ')' : ''}`
    } else {
      msg.value = '⚠️ ' + (d.result || '打卡失败')
    }
  } catch (e) {
    msg.value = '❌ 请求失败: ' + e.message
  }
  submitting.value = false
}
</script>

<template>
  <div class="checkin-card">
    <!-- 已完成状态 -->
    <div v-if="!loading && done" class="done-box">
      <div class="done-icon">✅</div>
      <div class="done-label">晨间打卡 · 已完成</div>
      <div class="done-mode">今日模式:{{ MODES[mode]?.label || mode }} ({{ MODES[mode]?.desc || '' }})</div>
    </div>

    <!-- 未完成状态 -->
    <div v-else-if="!loading && !done" class="todo-box">
      <template v-if="!picking">
        <div class="todo-label">☀️ 晨间打卡 · 未完成</div>
        <button class="pick-btn" @click="picking = true" :disabled="submitting">
          选择今日模式开始
        </button>
      </template>
      <template v-else>
        <div class="todo-label">🎚️ 选择今日模式</div>
        <div class="mode-grid">
          <button v-for="(info, key) in MODES" :key="key"
                  class="mode-btn" :style="{ borderColor: info.color }"
                  @click="doCheckin(key)" :disabled="submitting">
            <div class="mode-name" :style="{ color: info.color }">{{ info.label }}</div>
            <div class="mode-desc">{{ info.desc }}</div>
          </button>
        </div>
        <button class="cancel-btn" @click="picking = false" :disabled="submitting">取消</button>
      </template>
      <p v-if="msg" class="msg">{{ msg }}</p>
    </div>

    <!-- 加载中 -->
    <div v-else class="loading-box">
      <div>⏳ 加载打卡状态...</div>
      <p v-if="msg" class="msg">{{ msg }}</p>
      <button v-if="msg" class="retry-btn" @click="fetchStatus">🔄 重试</button>
    </div>
  </div>
</template>

<style scoped>
.checkin-card { max-width: 720px; margin: 0 auto; }
.done-box, .todo-box, .loading-box {
  border-radius: 10px; padding: 14px; text-align: center;
}
.done-box { background: #e8f5e9; border: 1px solid #3eaf7c; }
.done-icon { font-size: 24px; }
.done-label { font-size: 14px; font-weight: 600; color: #2e7d32; margin-top: 4px; }
.done-mode { font-size: 13px; color: #555; margin-top: 4px; }
.todo-box { background: #fff8e1; border: 1px solid #e6a23c; }
.todo-label { font-size: 14px; font-weight: 600; color: #b26a00; }
.pick-btn {
  margin-top: 10px; padding: 8px 18px; border: none; border-radius: 8px;
  background: #e6a23c; color: #fff; font-size: 14px; cursor: pointer;
}
.pick-btn:disabled { opacity: .6; cursor: not-allowed; }
.mode-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px; margin-top: 10px;
}
.mode-btn {
  background: #fff; border: 2px solid #ddd; border-radius: 10px;
  padding: 10px 6px; cursor: pointer; transition: transform .1s;
}
.mode-btn:hover { transform: translateY(-2px); }
.mode-btn:disabled { opacity: .6; cursor: not-allowed; }
.mode-name { font-size: 15px; font-weight: 700; }
.mode-desc { font-size: 12px; color: #888; margin-top: 2px; }
.cancel-btn {
  margin-top: 10px; background: none; border: 1px solid #ccc; color: #888;
  border-radius: 8px; padding: 6px 14px; font-size: 13px; cursor: pointer;
}
.msg { font-size: 13px; color: #b26a00; margin-top: 8px; }
.retry-btn {
  margin-top: 8px; padding: 6px 14px; border: 1px solid #e6a23c;
  background: #fff; color: #b26a00; border-radius: 8px; font-size: 13px; cursor: pointer;
}
.loading-box { color: #999; }
</style>

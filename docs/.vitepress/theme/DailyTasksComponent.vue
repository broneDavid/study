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
  light: { label: '轻量', desc: '15分钟', color: '#ff9500' },
  standard: { label: '标准', desc: '30分钟', color: '#34c759' },
  intensive: { label: '加强', desc: '60分钟', color: '#ff3b30' },
  off: { label: '休息', desc: '今天不学', color: '#8e8e93' },
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
      // 页内毛玻璃横幅庆祝(替换 window.alert,详见模板 all-done-banner)
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
      await fetchStatus()
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
      <!-- 全完成横幅(页内毛玻璃庆祝) -->
      <Transition name="celebrate">
      <div v-if="allDone()" class="all-done-banner">
        <span class="banner-emoji">🎉</span> 今日学习全部完成!连续学习 {{ status.streak_days }} 天,继续保持
      </div>
      </Transition>
      <div class="summary">
        今日模式:<b class="mode-tag">{{ MODE_LABELS[status.mode] || status.mode }}</b>
        · 连续答对 {{ status.streak_correct }} 次
        · 连续学习 {{ status.streak_days }} 天
      </div>

      <div class="steps">
        <!-- 打卡步骤:未打卡时点开选模式 -->
        <div class="step" :class="status.checkin_done ? 'done' : 'todo'">
          <div class="step-icon">{{ status.checkin_done ? '✓' : '1' }}</div>
          <div class="step-body">
            <div class="step-name">晨间打卡</div>
            <div class="step-desc">{{ status.checkin_done ? '已完成 · ' + (MODE_LABELS[status.mode] || '') + ' 模式' : '选择今日学习模式' }}</div>
            <div v-if="!status.checkin_done" class="step-action">
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
          <div class="step-chev">›</div>
        </div>

        <a class="step link" :class="status.lesson_done ? 'done' : (status.checkin_done ? 'active' : 'todo')" href="/study/daily#today-lesson">
          <div class="step-icon">{{ status.lesson_done ? '✓' : '2' }}</div>
          <div class="step-body">
            <div class="step-name">学习知识点</div>
            <div class="step-desc">{{ status.lesson_done ? '已完成' : '今日科目 · 高数/设备' }}</div>
          </div>
          <div class="step-chev">›</div>
        </a>

        <a class="step link" :class="status.quiz_done ? 'done' : (status.checkin_done && status.lesson_done ? 'active' : 'todo')" href="/study/quiz">
          <div class="step-icon">{{ status.quiz_done ? '✓' : '3' }}</div>
          <div class="step-body">
            <div class="step-name">在线小测</div>
            <div class="step-desc">{{ status.quiz_done ? '已完成' : '6 题 · AI 批改 + 解析' }}</div>
          </div>
          <div class="step-chev">›</div>
        </a>

        <a class="step link" :class="status.review_done ? 'done' : 'todo'" href="/study/mistakes">
          <div class="step-icon">{{ status.review_done ? '✓' : '4' }}</div>
          <div class="step-body">
            <div class="step-name">复盘错题</div>
            <div class="step-desc">{{ status.review_done ? '已完成' : '错题重练 · 看解析' }}</div>
          </div>
          <div class="step-chev">›</div>
        </a>
      </div>
      <p v-if="checkinMsg" class="checkin-msg">{{ checkinMsg }}</p>
    </template>
  </div>
</template>

<style scoped>
.tasks-wrapper { max-width: 860px; margin: 0 auto; }
.status { padding: 16px; text-align: center; color: #86868b; }
.status.error { color: #ff3b30; }
.retry { margin-top: 8px; padding: 8px 20px; border: none; background: linear-gradient(180deg, #0077ed, #0071e3); color: #fff; border-radius: 980px; cursor: pointer; font-size: 14px; box-shadow: inset 0 1px 0 rgba(255,255,255,.25), 0 2px 8px rgba(0,113,227,.3); transition: transform .15s ease; }
.retry:active { transform: scale(.96); }
.all-done-banner {
  background: linear-gradient(135deg, rgba(52,199,89,.14), rgba(52,199,89,.08));
  -webkit-backdrop-filter: saturate(180%) blur(16px); backdrop-filter: saturate(180%) blur(16px);
  border: 1px solid rgba(52,199,89,.35); border-radius: 16px;
  padding: 14px; text-align: center; font-size: 15px; font-weight: 600; color: var(--app-green, #34c759);
  margin-bottom: 12px; box-shadow: var(--app-shadow-sm, 0 1px 6px rgba(0,0,0,.05));
}
.banner-emoji { font-size: 18px; margin-right: 4px; }
.celebrate-enter-active { animation: app-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.celebrate-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.celebrate-leave-to { opacity: 0; transform: scale(0.9); }
.step.done .step-icon { animation: app-pop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.summary { font-size: 13px; color: #86868b; margin-bottom: 12px; text-align: center; }
.mode-tag { color: #0071e3; }

/* 步骤条:手机=纵向,平板/桌面=横向卡片 */
.steps { display: flex; flex-direction: column; }
.step {
  display: flex; align-items: center; gap: 14px;
  background: rgba(255,255,255,.72);
  -webkit-backdrop-filter: saturate(180%) blur(20px); backdrop-filter: saturate(180%) blur(20px);
  border: 1px solid rgba(255,255,255,.6);
  border-radius: 18px; box-shadow: 0 4px 24px rgba(0,0,0,.08);
  padding: 14px 16px; margin-bottom: 10px;
  text-decoration: none; color: inherit;
}
.step-icon {
  width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  background: rgba(128,128,128,.12); color: #86868b; font-size: 16px; font-weight: 700;
}
.step.done .step-icon { background: #34c759; color: #fff; }
.step.active .step-icon { background: #0071e3; color: #fff; box-shadow: 0 0 0 4px rgba(0,113,227,.18); }
.step-body { flex: 1; min-width: 0; }
.step-name { font-size: 16px; font-weight: 600; color: #1d1d1f; }
.step-desc { font-size: 13px; color: #86868b; margin-top: 1px; }
.step.active .step-name { color: #0071e3; }
.step-chev { color: #aeaeb2; font-size: 18px; }
.step-action { margin-top: 6px; }
.mini-btn { padding: 6px 16px; border: none; border-radius: 980px; background: linear-gradient(180deg, #0077ed, #0071e3); color: #fff; font-size: 13px; cursor: pointer; box-shadow: inset 0 1px 0 rgba(255,255,255,.25), 0 2px 8px rgba(0,113,227,.3); transition: transform .15s ease; }
.mini-btn:active { transform: scale(.96); }
.mode-picker { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
.mode-opt { background: #fff; border: 1.5px solid; border-radius: 980px; padding: 6px 12px; font-size: 12px; cursor: pointer; }
.mode-opt:disabled { opacity: .5; }
.mode-cancel { background: none; border: none; color: #8e8e93; font-size: 12px; cursor: pointer; margin-left: 4px; }
.checkin-msg { font-size: 13px; color: #34c759; text-align: center; margin-top: 8px; }

/* 深色模式(挂 html.dark,双轨兼容) */
html.dark .step { background: rgba(28,28,32,.72); border-color: rgba(255,255,255,.1); box-shadow: 0 4px 24px rgba(0,0,0,.5); }
html.dark .step-name { color: #f5f5f7; }
html.dark .step-desc { color: #98989d; }
html.dark .mode-opt { background: #1c1c20; }

/* 平板/桌面:横向 4 卡 */
@media (min-width: 768px) {
  .steps { flex-direction: row; gap: 12px; }
  .step { flex: 1; flex-direction: column; text-align: center; padding: 20px 14px; margin-bottom: 0; }
  .step-body { text-align: center; }
  .step-chev { display: none; }
  .step-action { width: 100%; }
  .mode-picker { justify-content: center; }
  .summary { text-align: left; }
}
</style>

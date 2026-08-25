<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithTimeout } from './fetchUtil.js'
import { API_BASE } from './apiConfig.js'

const state = ref('loading')
const tab = ref('review')      // review | map
const reviews = ref([])
const knowledge = ref({})
const open = ref({})           // 知识地图:科目 -> 是否展开
const errorMsg = ref('')

const masteryColor = m => m >= 80 ? '#34c759' : m >= 40 ? '#0071e3' : '#ff9500'

async function load() {
  state.value = 'loading'
  errorMsg.value = ''
  try {
    const [r, k] = await Promise.all([
      fetchWithTimeout(`${API_BASE}/reviews`),
      fetchWithTimeout(`${API_BASE}/knowledge`),
    ])
    if (!r.ok) throw new Error('HTTP ' + r.status)
    const rd = await r.json()
    const kd = await k.json()
    reviews.value = rd.items || []
    knowledge.value = kd.subjects || {}
    state.value = 'ready'
  } catch (e) {
    state.value = 'error'
    errorMsg.value = '加载失败: ' + e.message
  }
}

function toggle(subj) {
  open.value[subj] = !open.value[subj]
}

onMounted(load)
</script>

<template>
  <div class="map-wrapper">
    <h2>🗺️ 复习地图</h2>
    <p class="sub">FSRS 智能调度 · 下个复习时间由你的记忆表现动态决定</p>

    <div class="tabs">
      <button :class="['tab', { active: tab === 'review' }]" @click="tab = 'review'">
        📌 今日复习
        <span v-if="reviews.length" class="tab-dot">{{ reviews.length }}</span>
      </button>
      <button :class="['tab', { active: tab === 'map' }]" @click="tab = 'map'">
        🧠 知识地图
      </button>
    </div>

    <div v-if="state === 'loading'" class="status">⏳ 加载中...</div>
    <div v-else-if="state === 'error'" class="status error">
      <p>⚠️ {{ errorMsg }}</p>
      <button @click="load">重试</button>
    </div>

    <template v-else>
      <!-- 今日复习队列 -->
      <div v-if="tab === 'review'">
        <div v-if="reviews.length === 0" class="status">
          <p>🎉 今日没有到期复习</p>
          <p class="hint">FSRS 会把间隔按你的掌握度拉长,记得复习完的要注意。</p>
        </div>
        <template v-else>
          <p class="hint">按掌握度升序(薄弱优先),今日 {{ reviews.length }} 条待复习</p>
          <div v-for="(it, i) in reviews" :key="i" class="rev-item">
            <span class="subj-tag">{{ it.subject.slice(0, 2) }}</span>
            <div class="rev-body">
              <div class="rev-title">{{ it.title }}</div>
              <div class="bar"><div class="bar-fill" :style="{ width: it.mastery + '%', background: masteryColor(it.mastery) }"></div></div>
            </div>
            <span class="mastery" :style="{ color: masteryColor(it.mastery) }">{{ it.mastery }}</span>
          </div>
          <p class="footnote">答对 → 间隔拉长(2→11→46 天);答错 → 明后天重看。复习走学习系统批改。</p>
        </template>
      </div>

      <!-- 知识地图 -->
      <div v-else>
        <div v-for="(s, subj) in knowledge" :key="subj" class="subj-block">
          <h3 class="subj-head" @click="toggle(subj)">
            {{ subj }} {{ open[subj] ? '▾' : '▸' }}
            <span class="stat">总{{ s.total }} · 掌握{{ s.mastered }} · 薄弱{{ s.weak }} · 今日{{ s.due_today }}</span>
          </h3>
          <div v-if="open[subj]" class="map-list">
            <div v-for="(it, i) in s.items" :key="i" class="map-item">
              <span class="mastery-pill" :style="{ background: masteryColor(it.mastery) }">{{ it.mastery }}</span>
              <div class="map-body">
                <div class="map-title">{{ it.title }}</div>
                <div class="map-sub">下次 {{ it.next_review || '未排' }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.map-wrapper { max-width: 760px; margin: 0 auto; }
.sub { color: #888; margin-top: -6px; }
.status { padding: 24px; text-align: center; color: #666; }
.status.error { color: #d93025; }
.hint { font-size: 13px; color: #999; margin: 8px 0; }
.footnote { font-size: 12px; color: #86868b; margin-top: 12px; }

.tabs { display: flex; gap: 8px; margin: 12px 0; }
.tab { background: #f0f0f0; color: #444; border: none; border-radius: 980px; padding: 8px 16px; font-size: 14px; cursor: pointer; }
.tab.active { background: linear-gradient(180deg,#0077ed,#0071e3); color: #fff; font-weight: 600; }
.tab-dot { background: #ff3b30; color: #fff; border-radius: 999px; padding: 0 7px; font-size: 12px; margin-left: 5px; }

.rev-item { display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,.94); border: 1px solid rgba(255,255,255,.6); border-radius: 12px; padding: 10px 12px; margin: 6px 0; box-shadow: 0 1px 6px rgba(0,0,0,.05); }
.subj-tag { flex-shrink: 0; background: rgba(0,113,227,.12); color: #0071e3; border-radius: 8px; padding: 3px 7px; font-size: 12px; font-weight: 600; }
.rev-body { flex: 1; min-width: 0; }
.rev-title { font-size: 14px; color: #1d1d1f; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar { height: 4px; background: #ececec; border-radius: 2px; margin-top: 5px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 2px; }
.mastery { font-size: 14px; font-weight: 700; width: 26px; text-align: right; }

.subj-block { margin: 14px 0; }
.subj-head { font-size: 16px; font-weight: 700; cursor: pointer; padding: 8px 4px; border-bottom: 2px solid #eee; display: flex; align-items: center; gap: 8px; }
.stat { font-size: 12px; color: #86868b; font-weight: 400; margin-left: auto; }
.map-list { margin-top: 4px; }
.map-item { display: flex; align-items: center; gap: 10px; padding: 8px 6px; border-bottom: 1px solid #f0f0f0; }
.mastery-pill { width: 34px; height: 22px; border-radius: 6px; color: #fff; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.map-body { flex: 1; min-width: 0; }
.map-title { font-size: 14px; color: #333; }
.map-sub { font-size: 12px; color: #999; }

/* 深色模式挂 html.dark,双轨兼容 */
html.dark .tab { background: #2c2c2e; color: #d0d0d4; }
html.dark .tab.active { background: linear-gradient(180deg,#0a84ff,#0071e3); color: #fff; }
html.dark .rev-item { background: rgba(28,28,32,.72); border-color: rgba(255,255,255,.1); }
html.dark .rev-title { color: #f5f5f7; }
html.dark .bar { background: #2c2c2e; }
html.dark .subj-tag { background: rgba(10,132,255,.12); color: #0a84ff; }
html.dark .subj-head { border-color: #2c2c2e; color: #f5f5f7; }
html.dark .stat { color: #98989d; }
html.dark .map-item { border-color: #2c2c2e; }
html.dark .map-title { color: #e8e8ea; }
html.dark .map-sub { color: #98989d; }
</style>
import DefaultTheme from 'vitepress/theme'
import './katex-css/katex.min.css'
import './apple.css'
import QuizComponent from './QuizComponent.vue'
import MistakesReplayComponent from './MistakesReplayComponent.vue'
import DailyTasksComponent from './DailyTasksComponent.vue'
import ReviewMapComponent from './ReviewMapComponent.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('QuizComponent', QuizComponent)
    app.component('MistakesReplayComponent', MistakesReplayComponent)
    app.component('DailyTasksComponent', DailyTasksComponent)
    app.component('ReviewMapComponent', ReviewMapComponent)
    // PWA:注册 service worker(离线缓存静态内容;iPad 添加到主屏更像 App)
    if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/study/sw.js').catch(() => { /* 安静失败 */ })
      })
    }
  },
}
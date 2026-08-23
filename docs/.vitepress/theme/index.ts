import DefaultTheme from 'vitepress/theme'
import './katex-css/katex.min.css'
import QuizComponent from './QuizComponent.vue'
import CheckinComponent from './CheckinComponent.vue'
import MistakesReplayComponent from './MistakesReplayComponent.vue'
import DailyTasksComponent from './DailyTasksComponent.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('QuizComponent', QuizComponent)
    app.component('CheckinComponent', CheckinComponent)
    app.component('MistakesReplayComponent', MistakesReplayComponent)
    app.component('DailyTasksComponent', DailyTasksComponent)
  },
}
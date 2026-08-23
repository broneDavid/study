import DefaultTheme from 'vitepress/theme'
import './katex-css/katex.min.css'
import QuizComponent from './QuizComponent.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('QuizComponent', QuizComponent)
  },
}
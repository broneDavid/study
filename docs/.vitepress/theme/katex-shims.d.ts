declare module 'markdown-it-katex' {
  import MarkdownIt from 'markdown-it'
  const plugin: (md: MarkdownIt, options?: any) => void
  export default plugin
}
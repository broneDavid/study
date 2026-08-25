import { defineConfig } from 'vitepress'

// 公式渲染:2019 华科考研经典型,markdown-it-katex
import katex from 'markdown-it-katex'

export default defineConfig({
  title: '启的考研笔记',
  description: '考研备考学习记录 · 高等数学 / 机械原理 / 英语 / 炼油化工设备',
  lang: 'zh-CN',
  base: '/study/',
  cleanUrls: true,
  lastUpdated: true,

  head: [
    ['meta', { name: 'description', content: '记录学习积累内容 (考研: 数一·机械原理·英一·化工设备)' }],
    ['meta', { name: 'theme-color', content: '#0071e3' }],
    // PWA:可安装到 iPad 主屏 + 支持离线阅读静态内容
    ['link', { rel: 'manifest', href: '/study/manifest.webmanifest' }],
    ['link', { rel: 'apple-touch-icon', href: '/study/icons/apple-touch-icon.png' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'default' }],
  ],

  markdown: {
    config: (md) => { md.use(katex) },
  },

  themeConfig: {
    // 导航(高频 5 项,低频项在侧边栏/门户页)
    nav: [
      { text: '每日学习', link: '/daily' },
      { text: '复习地图', link: '/map' },
      { text: '在线小测', link: '/quiz' },
      { text: '错题本', link: '/mistakes' },
      { text: '每周周报', link: '/reports/' },
    ],

    // 侧边栏:按路径分组(不再复制导航)
    sidebar: {
      '/subjects/': [
        {
          text: '📘 学科笔记',
          items: [
            { text: '高等数学', link: '/subjects/高等数学' },
            { text: '机械原理', link: '/subjects/机械原理' },
            { text: '英语', link: '/subjects/英语' },
            { text: '炼油化工设备', link: '/subjects/炼油化工设备' },
          ],
        },
      ],
      '/': [
        {
          text: '🎯 每日行动',
          items: [
            { text: '首页', link: '/' },
            { text: '每日学习', link: '/daily' },
            { text: '复习地图', link: '/map' },
            { text: '在线小测', link: '/quiz' },
            { text: '错题本', link: '/mistakes' },
          ],
        },
        {
          text: '📊 学习回顾',
          items: [
            { text: '学习进度', link: '/progress' },
            { text: '学习计划', link: '/plan' },
            { text: '每周周报', link: '/reports/' },
          ],
        },
        {
          text: '📘 学科笔记',
          items: [
            { text: '高等数学', link: '/subjects/高等数学' },
            { text: '机械原理', link: '/subjects/机械原理' },
            { text: '英语', link: '/subjects/英语' },
            { text: '炼油化工设备', link: '/subjects/炼油化工设备' },
          ],
        },
      ],
    },

    footer: {
      message: '考研备考 · 每日更新 · MIT License',
      copyright: 'Copyright © 2026 Jeson Bern',
    },

    lastUpdated: true,
    outline: { level: [2, 3], label: '本页导航' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索笔记', buttonAriaLabel: '搜索' },
          modal: { noResultsText: '未找到相关内容' },
        },
      },
    },
  },
})
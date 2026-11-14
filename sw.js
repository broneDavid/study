// 学习网站 service worker —— 提供离线阅读静态内容(笔记/知识点/周报)与 PWA 安装能力。
// 策略:
//   - 静态资源(js/css/图片/字体/PDF):cache-first + 后台更新(离线可用)
//   - 导航/页面:network-first,离线 fallback 到缓存(最后兜底首页)
// API(/quiz/*)不缓存(动态数据,走网络)。
const CACHE = 'study-v2'
const BASE = '/study/'

self.addEventListener('install', () => { self.skipWaiting() })

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', (e) => {
  const req = e.request
  if (req.method !== 'GET') return
  const url = new URL(req.url)
  if (url.origin !== location.origin) return  // 跨域(API/字体CDN)不拦

  // 静态资源:cache-first + 后台刷新
  if (/\.(js|css|png|jpe?g|webp|svg|gif|woff2?|ttf|otf|pdf|webmanifest)$/.test(url.pathname)) {
    e.respondWith(
      caches.match(req).then((hit) => {
        const fetchP = fetch(req).then((res) => {
          if (res.ok) { const c = res.clone(); caches.open(CACHE).then((cache) => cache.put(req, c)) }
          return res
        }).catch(() => hit)
        return hit || fetchP
      })
    )
    return
  }

  // 导航/页面:network-first,离线兜底缓存
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then((res) => {
        const cp = res.clone()
        caches.open(CACHE).then((cache) => cache.put(req, cp))
        return res
      }).catch(() =>
        caches.match(req).then((hit) => hit || caches.match(BASE))
      )
    )
  }
})
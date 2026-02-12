/* Offline: cache-first static, network-first API */
const CACHE_VERSION = 'kb-analyzer-v1';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const STATIC_ASSETS = ['/', '/manifest.json', '/static/js/chart.umd.min.js'];
self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(STATIC_CACHE).then((cache) => cache.addAll(STATIC_ASSETS)));
  self.skipWaiting();
});
self.addEventListener('activate', (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.map((k) => (k.startsWith('kb-analyzer-') && k !== STATIC_CACHE) ? caches.delete(k) : null))));
  self.clients.claim();
});
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(fetch(event.request).catch(() => caches.match('/')));
    return;
  }
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request).then((res) => {
      if (event.request.method === 'GET' && url.origin === self.location.origin) {
        const clone = res.clone();
        caches.open(STATIC_CACHE).then((cache) => cache.put(event.request, clone));
      }
      return res;
    }))
  );
});

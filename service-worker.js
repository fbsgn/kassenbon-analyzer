// Service Worker für Kassenbon-Analyzer PWA
const CACHE_NAME = 'kassenbon-analyzer-v1';
const RUNTIME_CACHE = 'kassenbon-runtime-v1';

// Dateien die beim Install gecacht werden
const PRECACHE_URLS = [
  '/',
  '/static/icon-192.png',
  '/static/icon-512.png'
];

// Install Event - Precache wichtige Dateien
self.addEventListener('install', event => {
  console.log('[SW] Installing Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] Precaching app shell');
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate Event - Alte Caches löschen
self.addEventListener('activate', event => {
  console.log('[SW] Activating Service Worker...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => {
            return cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE;
          })
          .map(cacheName => {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Network First für API, Cache First für Statische Dateien
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // API-Requests: Network First (immer frische Daten)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Clone response weil Stream nur einmal gelesen werden kann
          const responseClone = response.clone();
          
          // Cache für Offline-Fallback
          caches.open(RUNTIME_CACHE).then(cache => {
            cache.put(request, responseClone);
          });
          
          return response;
        })
        .catch(() => {
          // Offline: Versuche aus Cache
          return caches.match(request);
        })
    );
    return;
  }
  
  // Statische Dateien: Cache First (schneller)
  if (request.destination === 'image' || 
      request.destination === 'script' || 
      request.destination === 'style') {
    
    event.respondWith(
      caches.match(request).then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }
        
        return fetch(request).then(response => {
          return caches.open(RUNTIME_CACHE).then(cache => {
            cache.put(request, response.clone());
            return response;
          });
        });
      })
    );
    return;
  }
  
  // HTML-Seiten: Network First, mit Cache-Fallback
  event.respondWith(
    fetch(request)
      .then(response => {
        const responseClone = response.clone();
        caches.open(RUNTIME_CACHE).then(cache => {
          cache.put(request, responseClone);
        });
        return response;
      })
      .catch(() => {
        return caches.match(request).then(response => {
          return response || caches.match('/');
        });
      })
  );
});

// Background Sync (optional - für spätere Features)
self.addEventListener('sync', event => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'sync-receipts') {
    event.waitUntil(
      // Hier könnten wir später PDFs synchronisieren
      Promise.resolve()
    );
  }
});

// Push Notifications (optional - für spätere Features)
self.addEventListener('push', event => {
  console.log('[SW] Push received:', event);
  
  const options = {
    body: event.data ? event.data.text() : 'Neue Nachricht',
    icon: '/static/icon-192.png',
    badge: '/static/icon-192.png',
    vibrate: [200, 100, 200],
    tag: 'kassenbon-notification',
    requireInteraction: false
  };
  
  event.waitUntil(
    self.registration.showNotification('Kassenbon-Analyzer', options)
  );
});

// Notification Click
self.addEventListener('notificationclick', event => {
  console.log('[SW] Notification clicked');
  
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow('/')
  );
});

console.log('[SW] Service Worker loaded');

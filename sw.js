/* SOC Events Cheat Sheet — service worker (офлайн + автообновление) */
const CACHE = 'soc-cheatsheet-v2';
const ASSETS = ['./', 'index.html', 'lol-links.html', 'help.html', 'data.js', 'manifest.json', 'icon.svg'];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

// stale-while-revalidate: отдаём из кэша сразу (быстро + офлайн), фоном обновляем
self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  try { if (new URL(req.url).origin !== location.origin) return; } catch (_) { return; }
  e.respondWith(
    caches.open(CACHE).then(function (cache) {
      return cache.match(req).then(function (cached) {
        var net = fetch(req).then(function (res) {
          if (res && res.status === 200) cache.put(req, res.clone());
          return res;
        }).catch(function () { return cached; });
        return cached || net;
      });
    })
  );
});

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open("hangarin-cache-v1").then(function (cache) {
      return Promise.all([
        cache.add("/").catch(err => console.log("Failed:", err)),
        cache.add("/static/css/bootstrap.min.css").catch(err => console.log("Failed:", err)),
        cache.add("/static/js/main.js").catch(err => console.log("Failed:", err))
      ]);
    })
  );
});

self.addEventListener("fetch", function (e) {
  e.respondWith(
    caches.match(e.request).then(function (response) {
      return response || fetch(e.request);
    })
  );
});

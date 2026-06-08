self.addEventListener('push', function(event) {
  let data = {};
  try { data = event.data.json(); } catch(e) {}
  const title   = data.title || '線上有位';
  const options = {
    body:    data.body || '',
    icon:    '/icon-192.png',
    badge:   '/icon-192.png',
    data:    { url: data.url || '/' },
    silent:  false,
    vibrate: [200, 100, 200],
    tag:     data.tag || 'price-alert',
    renotify: true,
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(list) {
      for (const client of list) {
        if (client.url && 'focus' in client) return client.focus();
      }
      return clients.openWindow(event.notification.data.url || '/');
    })
  );
});

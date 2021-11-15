// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here. Other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.2.0/workbox-sw.js');

firebase.initializeApp({
  apiKey: 'AIzaSyBFHIY07QF7_HQOaxgPdng648sZgIyL3Wg',
  authDomain: 'onebarangay-malanday.firebaseapp.com',
  projectId: 'onebarangay-malanday',
  storageBucket: 'onebarangay-malanday.appspot.com',
  messagingSenderId: '151952863728',
  appId: '1:151952863728:web:7660ee42c28cd0b391ad35',
  measurementId: 'G-MJRG0CGME7',
});
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => self.registration.showNotification(`[BG] ${payload.data.title}`,
  { data: payload.data, ...payload.data }));

workbox.routing.registerRoute(
  ({ request }) => request.destination === 'image',
  new workbox.strategies.CacheFirst(),
);

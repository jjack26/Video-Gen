const CACHE='video-gen-studio-v2';
const FILES=['./','./index.html','./studio.css','./studio.js','./team.json','./research.json','./official-cohort.json','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',event=>{if(event.request.method!=='GET'||new URL(event.request.url).origin!==self.location.origin)return;event.respondWith(fetch(event.request).then(res=>{if(res.ok){const copy=res.clone();caches.open(CACHE).then(c=>c.put(event.request,copy))}return res}).catch(()=>caches.match(event.request).then(res=>res||new Response('Offline. Open the studio home page to use cached briefs.',{status:503}))))});

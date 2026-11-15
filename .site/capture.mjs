// Capture a web page as an iPhone would show it (mobile emulation over the Chrome DevTools protocol, no libraries).
// Usage, from the Website folder:
//   node .site/capture.mjs https://ybmedwm-stack.github.io/sparkys-electric/ .site/captures/sparkys-mobile.png 440 902 3
//   node .site/capture.mjs https://ybmedwm-stack.github.io/sparkys-electric/ .site/captures/sparkys-desktop.png 1280 800 2
// A width of 1000 or more captures as a desktop browser; under 1000, as an iPhone.
// Then run python3 .site/shots.py, which frames it for the site. Needs Google Chrome and Node 22+.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os'; import { join } from 'node:path';
const [url, out, w = '440', h = '956', dpr = '3'] = process.argv.slice(2);
const prof = mkdtempSync(join(tmpdir(), 'mshot-'));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--remote-debugging-port=0', `--user-data-dir=${prof}`, 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
const wsUrl = await new Promise((res) => { let b = ''; chrome.stderr.on('data', (d) => { b += d; const m = b.match(/ws:\/\/[^\s]+/); if (m) res(m[0]); }); });
const port = new URL(wsUrl).port;
const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
const ws = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); const events = [];
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } else events.push(m); });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable');
const phone = +w < 1000;
await send('Emulation.setDeviceMetricsOverride', { width: +w, height: +h, deviceScaleFactor: +dpr, mobile: phone });
if (phone) {
  await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Emulation.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
}
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
await send('Page.navigate', { url });
await new Promise((r) => setTimeout(r, 6000));
const shot = await send('Page.captureScreenshot', { format: 'png' });
writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
const sw = await send('Runtime.evaluate', { expression: 'JSON.stringify({sw: document.documentElement.scrollWidth, iw: innerWidth})', returnByValue: true });
console.log(sw.result.result.value);
chrome.kill();

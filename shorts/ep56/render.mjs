// 使い方: node render.mjs [frames出力先] [fps] [並列数]  /  プレビュー: node render.mjs out 24 1 --at 3.5,10.2
import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
import path from 'path'; import fs from 'fs'; import { fileURLToPath } from 'url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(process.argv[2] || 'frames'); const fps = +(process.argv[3] || 24); const par = +(process.argv[4] || 4);
const atIdx = process.argv.indexOf('--at'); const ats = atIdx > 0 ? process.argv[atIdx + 1].split(',').map(Number) : null;
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const open = async () => { const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + dir + '/index.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500); return p; };
const shot = async (p, t, f) => { await p.evaluate(t => render(t), t); await p.screenshot({ path: f, type: 'jpeg', quality: 92 }); };
if (ats) { const p = await open(); for (const t of ats) await shot(p, t, `${out}/at_${t}.jpg`); }
else {
  const p0 = await open(); const total = await p0.evaluate(() => TOTAL); const n = Math.ceil(total * fps);
  console.log('total', total, 'frames', n);
  const pages = [p0]; for (let i = 1; i < par; i++) pages.push(await open());
  await Promise.all(pages.map(async (p, k) => { for (let i = k; i < n; i += par) await shot(p, i / fps, `${out}/${String(i).padStart(5, '0')}.jpg`); }));
}
await browser.close();

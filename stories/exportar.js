// uso: node stories/exportar.js [D04]   → stories/dNN/01-manha.png, 02-tarde.png, 03-palavra.png
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const dia = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 2000 } });
  p.on('pageerror', e => console.log('ERRO', e.message));
  await p.goto('file://' + path.join(__dirname, 'motor.html') + (dia ? '?d=' + dia : ''), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const els = p.locator('.story'), n = await els.count();
  for (let i = 0; i < n; i++) {
    const f = await els.nth(i).getAttribute('data-file'), out = path.join(__dirname, f);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await els.nth(i).screenshot({ path: out });
  }
  console.log(n, 'stories');
  await b.close();
})();

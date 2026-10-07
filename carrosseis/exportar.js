// uso: node carrosseis/exportar.js <id> <pasta-saida> [pdf]
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
(async () => {
  const [id, dir, pdf] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 } });
  p.on('pageerror', e => console.log('ERRO', e.message));
  await p.goto('file://' + require('path').join(__dirname, 'motor.html') + '?c=' + id, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  if (pdf) { await p.pdf({ path: pdf, width: '1080px', height: '1350px', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } }); }
  const n = await p.locator('.slide').count();
  for (let i = 0; i < n; i++) await p.locator('.slide').nth(i).screenshot({ path: `${dir}/slide-${String(i + 1).padStart(2, '0')}.png` });
  console.log(id, n, 'slides');
  await b.close();
})();

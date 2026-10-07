// uso: node reels/render.js <id> <modo: stills|video|capa|meta> <saida> [tempos...]
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const MOTOR = require('path').join(__dirname, 'motor.html');
(async () => {
  const [id, mode, out, ...rest] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('ERRO', e.message));
  p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto('file://' + MOTOR + '?r=' + id, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const stage = p.locator('#stage');
  const meta = await p.evaluate(() => ({ dur: DURATION, bpm: SPEC.bpm, events: EVENTS, estrutura: ESTRUTURA }));
  if (mode === 'meta') { fs.writeFileSync(out, JSON.stringify(meta)); console.log('dur', meta.dur, 'eventos', meta.events.length); }
  else if (mode === 'auto') {
    const ts = await p.evaluate(() => { const r = []; SPEC.cenas.forEach(c => { r.push(c.t0 + c.dur * 0.5, c.t0 + c.dur * 0.93); }); return r; });
    for (const t of ts) { await p.evaluate(t => render(t), t); await stage.screenshot({ path: `${out}-${t.toFixed(2)}.png` }); }
  }
  else if (mode === 'stills') {
    for (const t of rest.map(Number)) { await p.evaluate(t => render(t), t); await stage.screenshot({ path: `${out}-${t}.png` }); }
  } else if (mode === 'capa') {
    await p.evaluate(t => render(t), +rest[0]); await stage.screenshot({ path: out });
  } else {
    fs.writeFileSync(out.replace(/\.mp4$/, '.json'), JSON.stringify(meta));
    const fps = 30;
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(fps), '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(meta.dur * fps);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => render(t), i / fps);
      const buf = await stage.screenshot({ type: 'jpeg', quality: 94 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log(id, 'quadros', n);
  }
  await b.close();
})();

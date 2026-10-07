// Render every *-mockup.svg (300 dpi) and *-print.svg (600 dpi) in this folder to PNG.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--lang=en-US'] });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const [, wmm, hmm] = svg.match(/width="([\d.]+)mm" height="([\d.]+)mm"/);
    const dpi = f.includes('print') ? 600 : 300;
    const pxW = Math.round(wmm / 25.4 * 96), pxH = Math.round(hmm / 25.4 * 96);
    const p = await b.newPage({ viewport: { width: pxW, height: pxH }, deviceScaleFactor: dpi / 96 });
    await p.setContent(`<html><body style="margin:0">${svg.replace(/width="[\d.]+mm" height="[\d.]+mm"/, `width="${pxW}" height="${pxH}"`)}</body></html>`);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1200);
    await p.screenshot({ path: path.join(dir, f.replace('.svg', '.png')) });
    await p.close();
  }
  await b.close();
})();

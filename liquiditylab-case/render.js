const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--lang=en-US'] });
  const dir = '/home/user/Facebook/liquiditylab-case/';
  for (const [name, wmm, hmm, dpi] of [['mockup', 90.4, 166, 300], ['print', 80.4, 156, 600]]) {
    const svg = fs.readFileSync(dir + `liquiditylab-iphone15pro-${name}.svg`, 'utf8');
    const pxW = Math.round(wmm / 25.4 * 96), pxH = Math.round(hmm / 25.4 * 96);
    const p = await b.newPage({ viewport: { width: pxW, height: pxH }, deviceScaleFactor: dpi / 96 });
    await p.setContent(`<html><body style="margin:0">${svg.replace(/width="[\d.]+mm" height="[\d.]+mm"/, `width="${pxW}" height="${pxH}"`)}</body></html>`);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1500);
    await p.screenshot({ path: dir + `liquiditylab-iphone15pro-${name}.png` });
    console.log(name, await p.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.status).join(',')));
  }
  await b.close();
})();

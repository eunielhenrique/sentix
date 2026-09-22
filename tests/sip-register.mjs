// Teste de viabilidade da fase 1: registrar um ramal da API4COM a partir de um
// softphone próprio (JsSIP num Chromium headless) e validar a sinalização de
// uma chamada de saída. Credenciais vêm de env — nunca ficam no repositório.
//   SIP_DOMAIN=... SIP_USER=... SIP_PASS=... node tests/sip-register.mjs
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const jssip = readFileSync(new URL('./jssip.bundle.js', import.meta.url), 'utf8');
const { SIP_DOMAIN, SIP_USER, SIP_PASS, TEST_DIAL = '1999' } = process.env;
if (!SIP_DOMAIN || !SIP_USER || !SIP_PASS) throw new Error('SIP_DOMAIN, SIP_USER e SIP_PASS são obrigatórios');

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'],
});
const page = await browser.newPage();
page.on('console', (m) => console.log('[page]', m.text()));
await page.setContent('<html><body></body></html>');
await page.addScriptTag({ content: jssip });

const result = await page.evaluate(
  ({ domain, user, pass, dial }) =>
    new Promise((resolve) => {
      const log = [];
      const socket = new JsSIP.WebSocketInterface(`wss://${domain}:6443`);
      const ua = new JsSIP.UA({
        sockets: [socket],
        uri: `sip:${user}@${domain}`,
        password: pass,
        register: true,
        register_expires: 120,
        user_agent: 'sentix-dialer/0.1',
      });
      const done = (status) => { ua.stop(); resolve({ status, log }); };
      setTimeout(() => done('timeout'), 25000);
      ua.on('connected', () => log.push('ws connected'));
      ua.on('disconnected', (e) => log.push('ws disconnected ' + (e?.code ?? '')));
      ua.on('registrationFailed', (e) => { log.push('registrationFailed ' + e.cause + ' ' + (e.response?.status_code ?? '')); done('register_failed'); });
      ua.on('registered', () => {
        log.push('REGISTERED as ' + user);
        const session = ua.call(`sip:${dial}@${domain}`, {
          mediaConstraints: { audio: true, video: false },
          pcConfig: { iceServers: [] },
        });
        session.on('progress', () => log.push('call progress (ringing)'));
        session.on('accepted', () => { log.push('call accepted'); session.terminate(); });
        session.on('failed', (e) => { log.push('call failed: ' + e.cause + ' ' + (e.message?.status_code ?? '')); ua.unregister(); done('ok'); });
        session.on('ended', (e) => { log.push('call ended: ' + e.cause); ua.unregister(); done('ok'); });
      });
      ua.start();
    }),
  { domain: SIP_DOMAIN, user: SIP_USER, pass: SIP_PASS, dial: TEST_DIAL },
);
await browser.close();
console.log(JSON.stringify(result, null, 2));
process.exit(result.status === 'ok' ? 0 : 1);

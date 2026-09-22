# Sentix — Fase 1: Discador web funcional (prompt para a sessão de front)

Você vai construir o **discador da Sentix**, um softphone web que roda como popup dentro
da plataforma Sentix e usa a **API4COM** como operadora de voz por baixo. A Sentix é um
produto novo, repositório novo, sem relação com outros produtos. Nada de outro projeto
entra aqui.

**Regra de marca:** a Sentix tem identidade própria. É proibido copiar layout, textos,
ícones, cores ou nome da API4COM. Replicamos a FUNÇÃO, não a interface.

## 1. Entrega da fase 1 (definição de "funcional")

O discador está pronto quando, logado com um usuário real da API4COM:

1. Registra o ramal do usuário no PBX da API4COM (status "Online" visível).
2. Faz uma chamada para um número externo (ex.: celular do Euniel) e o áudio funciona nos dois sentidos.
3. Recebe uma chamada (ligar para o número do ramal/DID e o popup toca).
4. Durante a chamada: mudo, espera/retomar, teclado DTMF, transferência para outro ramal, desligar, cronômetro.
5. Histórico de chamadas do usuário (hoje / ontem / 3 dias) vindo da API.
6. Lista da equipe (ramais da organização) com clique para ligar.
7. Saldo de créditos no cabeçalho.
8. Roda como **popup flutuante** (`<DialerWidget />`) que qualquer tela da Sentix monta uma vez no shell e abre/fecha por um evento global, com `openDialer({ number, name })` para click-to-call.

Fora da fase 1 (não construir agora): kanban, leads da Meta, distribuição, gravação/transcrição, backend próprio.

## 2. Stack

- React 18+ com Vite (JavaScript ou TypeScript, escolha uma e mantenha).
- `jssip` (npm) para SIP sobre WebSocket + WebRTC.
- Estado do discador em um Context (`DialerProvider`), sem Redux.
- CSS próprio ou Tailwind. Sem bibliotecas de UI pesadas.
- Sem backend nesta fase: o front fala direto com a API da API4COM usando o token do usuário.
  Se o navegador bloquear por CORS, use o proxy do Vite em dev (`/api → https://api.api4com.com`)
  e registre no README que produção precisará de um proxy fino.

## 3. Contratos da API4COM (validados em 22/09/2026)

Base: `https://api.api4com.com/api/v1/` (LoopBack). Todas as chamadas autenticadas levam o
header `Authorization: <token>` (o token puro, sem "Bearer").

| O quê | Chamada | Retorno relevante |
|---|---|---|
| Login | `POST /users/login` body `{ "email", "password" }` | `{ id: "<token>", ttl, created }` |
| Logout | `POST /users/logout` body `{ access_token }` | 204 |
| Perfil | `GET /users/me` | `{ uuid, name, email, role }` |
| Credenciais SIP do usuário | `GET /integrations?filter[where][gateway]=sippulse` | `[{ metadata: { domain, username, password, first_name } }]` |
| Saldo | `GET /credits/balance` | `{ balance: "1138.56" }` |
| Ramais da organização (equipe) | `GET /extensions` | `[{ ramal, first_name, email_address, domain, ... }]` — **use só ramal, nome e e-mail; nunca exiba nem armazene o campo `senha`** |
| Histórico | `GET /calls?page=1&filter=<JSON url-encoded>` com `{"where":{...},"limit":50,"order":"started_at desc"}` | `{ data: [...] }` — inspecione os campos reais no primeiro GET e documente no README |
| Tokens da conta | `GET /users/accessTokens` | lista de tokens (informativo) |

Ausência de token → 401. Filtros seguem o padrão LoopBack (`filter[where][campo]=valor`).

## 4. Configuração SIP (é o que o webphone oficial usa; replique)

```js
const socket = new JsSIP.WebSocketInterface(`wss://${domain}:6443`);
const ua = new JsSIP.UA({
  sockets: [socket],
  uri: `sip:${username}@${domain}`,          // ex.: sip:1011@snowprint.api4com.com
  password,
  realm: domain,
  register: true,
  register_expires: 600,
  no_answer_timeout: 30,
  user_agent: 'sentix-dialer/0.1',
  connection_recovery_min_interval: 2,
  connection_recovery_max_interval: 30,
});
```

- Chamada: `ua.call(`sip:${numero}@${domain}`, { mediaConstraints: { audio: true, video: false } })`.
- Número: aceitar o que o usuário digitar e normalizar para E.164 sem "+" (ex.: `5511987654321`).
  Se o PBX rejeitar, testar o formato nacional `11987654321` e documentar qual funcionou.
- Eventos da sessão a tratar: `progress`, `accepted`, `confirmed`, `hold`, `unhold`, `muted`,
  `unmuted`, `ended`, `failed` (mostrar a causa de forma humana).
- Chamada recebida: `ua.on('newRTCSession')` com `originator === 'remote'` → tocar ringtone,
  mostrar tela de atendimento com nome/número.
- Áudio: um `<audio autoplay>` ligado ao stream remoto (`session.connection.ontrack`).
- Transferência: `session.refer(`sip:${ramal}@${domain}`)`.
- DTMF: `session.sendDTMF(tecla)`.
- Presença: derivar do estado do próprio UA (registered / unregistered / conectando). Presença
  de outros ramais fica para depois.

## 5. Arquitetura mínima

```
src/
  voice/
    VoiceAdapter.js        # interface: connect, call, answer, hangup, mute, hold, dtmf, transfer, on(event)
    api4comAdapter.js      # implementação JsSIP (única que existe hoje)
  api/api4com.js           # login, me, sipCredentials, balance, extensions, calls
  dialer/
    DialerProvider.jsx     # sessão, estado da chamada, histórico, equipe
    DialerWidget.jsx       # popup flutuante (botão + janela)
    screens/ Keypad, InCall, Incoming, History, Team, Settings, Login
  main.jsx                 # app de demonstração que monta o widget
```

O discador nunca chama JsSIP direto: só via `VoiceAdapter`. É o que permite trocar de operadora
no futuro sem reescrever a interface.

## 6. Segurança

- Token da API só em memória ou `sessionStorage`; nunca em `localStorage` nem em cookie.
- Senha SIP fica em memória durante a sessão; nunca vai para log, storage ou URL.
- Nenhuma credencial no repositório. Testes leem de variáveis de ambiente.
- Não logar payloads de API no console em produção.

## 7. Teste obrigatório antes de qualquer tela: registro do ramal

Rode este teste na SUA máquina (ambientes com proxy corporativo bloqueiam a porta 6443).
Ele prova que o PBX aceita um softphone próprio. Só depois disso comece a UI.

```bash
npm i jssip && npm i -D playwright esbuild && npx playwright install chromium
npx esbuild node_modules/jssip/lib/JsSIP.js --bundle --format=iife --global-name=JsSIP --platform=browser --outfile=tests/jssip.bundle.js
SIP_DOMAIN=snowprint.api4com.com SIP_USER=<ramal> SIP_PASS=<senha_sip> node tests/sip-register.mjs
```

`tests/sip-register.mjs`:

```js
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
const jssip = readFileSync(new URL('./jssip.bundle.js', import.meta.url), 'utf8');
const { SIP_DOMAIN, SIP_USER, SIP_PASS, TEST_DIAL = '1999' } = process.env;
if (!SIP_DOMAIN || !SIP_USER || !SIP_PASS) throw new Error('SIP_DOMAIN, SIP_USER e SIP_PASS são obrigatórios');
const browser = await chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'] });
const page = await browser.newPage();
page.on('console', (m) => console.log('[page]', m.text()));
await page.setContent('<html><body></body></html>');
await page.addScriptTag({ content: jssip });
const result = await page.evaluate(({ domain, user, pass, dial }) => new Promise((resolve) => {
  const log = [];
  const ua = new JsSIP.UA({ sockets: [new JsSIP.WebSocketInterface(`wss://${domain}:6443`)], uri: `sip:${user}@${domain}`, password: pass, register: true, register_expires: 120, user_agent: 'sentix-dialer/0.1' });
  const done = (status) => { ua.stop(); resolve({ status, log }); };
  setTimeout(() => done('timeout'), 25000);
  ua.on('connected', () => log.push('ws connected'));
  ua.on('disconnected', (e) => log.push('ws disconnected ' + (e?.code ?? '')));
  ua.on('registrationFailed', (e) => { log.push('registrationFailed ' + e.cause + ' ' + (e.response?.status_code ?? '')); done('register_failed'); });
  ua.on('registered', () => {
    log.push('REGISTERED as ' + user);
    const s = ua.call(`sip:${dial}@${domain}`, { mediaConstraints: { audio: true, video: false } });
    s.on('progress', () => log.push('ringing'));
    s.on('accepted', () => { log.push('accepted'); s.terminate(); });
    s.on('failed', (e) => { log.push('call failed: ' + e.cause + ' ' + (e.message?.status_code ?? '')); ua.unregister(); done('ok'); });
    s.on('ended', (e) => { log.push('ended: ' + e.cause); ua.unregister(); done('ok'); });
  });
  ua.start();
}), { domain: SIP_DOMAIN, user: SIP_USER, pass: SIP_PASS, dial: TEST_DIAL });
await browser.close();
console.log(JSON.stringify(result, null, 2));
process.exit(result.status === 'ok' ? 0 : 1);
```

Resultado esperado: `REGISTERED as <ramal>` seguido de `call failed: Not Found` ou similar
(o ramal 1999 não existe; isso prova a sinalização sem gastar crédito nem tocar em ninguém).
Se vier `registrationFailed 403`, o PBX está filtrando por user-agent: teste com
`user_agent: 'api4com-webphone(5.12.0)'` e reporte antes de seguir.

Os dados de domínio, ramal e senha SIP vêm de `GET /integrations?filter[where][gateway]=sippulse`
após o login, ou o Euniel passa direto.

## 8. Critérios de aceite (checklist para o PR)

- [ ] Teste de registro passou na máquina do dev (cole o log no PR, sem a senha).
- [ ] Login com e-mail/senha da API4COM e logout.
- [ ] Ramal registra e o status reflete conectado/desconectado/reconectando.
- [ ] Chamada externa com áudio nos dois sentidos, testada com telefone real.
- [ ] Chamada recebida toca e é atendida no popup.
- [ ] Mudo, espera, DTMF, transferência e desligar funcionam durante a chamada.
- [ ] Histórico, equipe e saldo carregam da API com estado de erro honesto (sem dado fake).
- [ ] `openDialer({ number, name })` abre o popup já discando.
- [ ] Nenhuma credencial no repo, no console ou no storage persistente.
- [ ] README com: como rodar, formato de número que funcionou, campos reais do `/calls`,
      e qualquer contrato que divergiu desta spec.

Reporte de volta por item desta lista. Se algum contrato da API estiver diferente do descrito
aqui, anote no PR e não invente campo.

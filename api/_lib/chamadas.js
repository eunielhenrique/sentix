// Núcleo do pipeline no Vercel: busca chamadas na API4COM, transcreve e classifica com o Gemini
// (uma chamada de modelo por gravação) e guarda o resultado no Vercel Blob privado.
import { list, put, get } from '@vercel/blob';
import fs from 'node:fs';
import path from 'node:path';

const API = 'https://api.api4com.com/api/v1';
const MODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
const PREFIX = 'chamadas/';

let schemaCache;
function esquema() {
  if (!schemaCache) {
    schemaCache = fs.readFileSync(path.join(process.cwd(), 'pipeline', 'CLASSIFICACAO.md'), 'utf8');
  }
  return schemaCache;
}

function exigir(nome) {
  const v = process.env[nome];
  if (!v) throw new Error(`variável de ambiente ${nome} não configurada`);
  return v;
}

export async function buscarChamadas({ desde, paginasMax = 5 }) {
  const token = exigir('API4COM_TOKEN');
  const where = desde ? { started_at: { gte: desde } } : {};
  const todas = [];
  for (let page = 1; page <= paginasMax; page++) {
    const filtro = encodeURIComponent(JSON.stringify({ where, limit: 100, order: 'started_at desc' }));
    const r = await fetch(`${API}/calls?page=${page}&filter=${filtro}`, { headers: { Authorization: token } });
    if (!r.ok) throw new Error(`API4COM /calls respondeu ${r.status}`);
    const d = await r.json();
    todas.push(...(d.data || []));
    if (!d.meta || page >= (d.meta.totalPageCount || 1)) break;
  }
  return todas;
}

export async function idsJaProcessados() {
  const ids = new Set();
  let cursor;
  do {
    const r = await list({ prefix: `${PREFIX}`, cursor, limit: 1000 });
    for (const b of r.blobs) {
      const m = b.pathname.match(/^chamadas\/([^/]+)\/analise\.json$/);
      if (m) ids.add(m[1]);
    }
    cursor = r.hasMore ? r.cursor : undefined;
  } while (cursor);
  return ids;
}

async function gemini(audioB64, chamada) {
  const key = exigir('GEMINI_API_KEY');
  const instrucao =
    'Você recebe a gravação de uma ligação de uma equipe de mobilização/vendas no Brasil. ' +
    'Primeiro transcreva o áudio em pt-BR marcando quem fala ("Vendedor:" / "Lead:"). ' +
    'Depois classifique a ligação no formato do esquema abaixo, usando apenas o que foi dito. ' +
    'Responda SOMENTE um JSON com todos os campos do esquema MAIS o campo "transcricao" (texto completo).\n\n' +
    esquema();
  const contexto =
    `Chamada id=${chamada.id} telefone=${chamada.to} vendedor=${chamada.first_name} ` +
    `duracao_s=${chamada.duration} data=${chamada.started_at}`;
  const body = {
    systemInstruction: { parts: [{ text: instrucao }] },
    contents: [{ role: 'user', parts: [{ inline_data: { mime_type: 'audio/mp3', data: audioB64 } }, { text: contexto }] }],
    generationConfig: { responseMimeType: 'application/json', temperature: 0.2 },
  };
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${key}`;
  const r = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`Gemini respondeu ${r.status}: ${(await r.text()).slice(0, 300)}`);
  const d = await r.json();
  const txt = d.candidates?.[0]?.content?.parts?.map((p) => p.text || '').join('') || '';
  const json = JSON.parse(txt.replace(/^```(json)?\s*|\s*```$/g, ''));
  return { json, uso: d.usageMetadata || null };
}

export async function processarChamada(chamada) {
  const audio = await fetch(chamada.record_url);
  if (!audio.ok) throw new Error(`gravação ${chamada.id} respondeu ${audio.status}`);
  const buf = Buffer.from(await audio.arrayBuffer());
  // cópia privada do áudio (a URL da operadora é pública)
  await put(`${PREFIX}${chamada.id}/audio.mp3`, buf, {
    access: 'private', contentType: 'audio/mpeg', allowOverwrite: true,
  });
  const { json, uso } = await gemini(buf.toString('base64'), chamada);
  const registro = {
    ...json,
    id: chamada.id,
    telefone: chamada.to,
    vendedor: chamada.first_name,
    duracao_s: chamada.duration,
    iniciada_em: chamada.started_at,
    ramal: chamada.from,
    modelo: MODEL,
    uso_tokens: uso,
    processada_em: new Date().toISOString(),
  };
  await put(`${PREFIX}${chamada.id}/analise.json`, JSON.stringify(registro), {
    access: 'private', contentType: 'application/json', allowOverwrite: true,
  });
  return registro;
}

// Processa chamadas com gravação ainda não analisadas, respeitando um orçamento de tempo.
export async function varrer({ horas = 6, orcamentoMs = 240_000, paralelo = 3 } = {}) {
  const inicio = Date.now();
  const desde = new Date(Date.now() - horas * 3600_000).toISOString();
  const [chamadas, feitos] = await Promise.all([buscarChamadas({ desde, paginasMax: 20 }), idsJaProcessados()]);
  const fila = chamadas.filter((c) => c.record_url && !feitos.has(c.id));
  const ok = [], erros = [];
  while (fila.length && Date.now() - inicio < orcamentoMs) {
    const lote = fila.splice(0, paralelo);
    const res = await Promise.allSettled(lote.map(processarChamada));
    res.forEach((r, i) => (r.status === 'fulfilled' ? ok.push(lote[i].id) : erros.push({ id: lote[i].id, erro: String(r.reason?.message || r.reason) })));
  }
  return { janela_horas: horas, chamadas: chamadas.length, pendentes_restantes: fila.length, processadas: ok.length, erros };
}

export async function lerAnalises() {
  const out = [];
  let cursor;
  do {
    const r = await list({ prefix: PREFIX, cursor, limit: 1000 });
    const alvos = r.blobs.filter((b) => b.pathname.endsWith('/analise.json'));
    const lidos = await Promise.all(alvos.map(async (b) => {
      const g = await get(b.pathname, { access: 'private' });
      return JSON.parse(await new Response(g.stream).text());
    }));
    out.push(...lidos);
    cursor = r.hasMore ? r.cursor : undefined;
  } while (cursor);
  return out;
}

export function autorizado(req, envName) {
  const segredo = process.env[envName];
  if (!segredo) return false;
  const url = new URL(req.url, 'http://x');
  const h = req.headers?.authorization || req.headers?.get?.('authorization') || '';
  return url.searchParams.get('key') === segredo || h === `Bearer ${segredo}`;
}

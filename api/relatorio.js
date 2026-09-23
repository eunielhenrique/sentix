// Relatório consolidado das análises: ?key=<REPORT_KEY>&formato=json|leads.csv|vendedores.csv
// Mesma lógica do pipeline/consolidate.py (última conversa define a classificação do telefone).
import { lerAnalises, autorizado } from './_lib/chamadas.js';

export const config = { maxDuration: 60 };

const CRIT = ['abertura', 'escuta', 'objecoes', 'clareza', 'fechamento', 'proximo_passo'];
const tel = (t) => String(t || '').replace(/\D/g, '').slice(-11);
const media = (a) => (a.length ? Math.round((a.reduce((x, y) => x + y, 0) / a.length) * 100) / 100 : null);

function csv(linhas) {
  if (!linhas.length) return '';
  const cols = Object.keys(linhas[0]);
  const esc = (v) => (v == null ? '' : /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v));
  return [cols.join(','), ...linhas.map((l) => cols.map((c) => esc(l[c])).join(','))].join('\n');
}

export default async function handler(req, res) {
  if (!autorizado(req, 'REPORT_KEY')) return res.status(401).json({ erro: 'não autorizado' });
  const formato = new URL(req.url, 'http://x').searchParams.get('formato') || 'json';
  const an = (await lerAnalises()).sort((a, b) => String(a.iniciada_em).localeCompare(String(b.iniciada_em)));

  const porTel = new Map();
  for (const a of an) {
    const k = tel(a.telefone);
    const d = porTel.get(k) || { tentativas: 0, ultima: null, conversas: 0 };
    d.tentativas++;
    if (a.falou_com_lead) { d.conversas++; d.ultima = a; } else if (!d.ultima) d.ultima = a;
    porTel.set(k, d);
  }
  const leads = [...porTel.entries()].map(([t, d]) => ({
    telefone: t, tentativas_gravadas: d.tentativas, conversas: d.conversas,
    classificacao: d.ultima?.classificacao_lead ?? null, interesse: d.ultima?.interesse ?? null,
    sentimento: d.ultima?.sentimento_lead ?? null, aceitou_grupo: d.ultima?.aceitou_grupo ?? null,
    proximo_passo: d.ultima?.proximo_passo ?? null, vendedor: d.ultima?.vendedor ?? null,
    cidade: d.ultima?.cidade_mencionada ?? null, resumo: d.ultima?.resumo ?? null,
    alertas: (d.ultima?.alertas || []).join('; '), ultima_chamada: d.ultima?.iniciada_em ?? null,
  })).sort((a, b) => (b.interesse ?? -1) - (a.interesse ?? -1));

  const porVend = new Map();
  for (const a of an) {
    const v = porVend.get(a.vendedor) || { chamadas: 0, conversas: 0, engajados: 0, notas: Object.fromEntries(CRIT.map((c) => [c, []])) };
    v.chamadas++;
    if (a.falou_com_lead) v.conversas++;
    if (['apoiador_ativo', 'engajado', 'recebeu_material'].includes(a.classificacao_lead)) v.engajados++;
    for (const c of CRIT) { const n = a.rubrica_vendedor?.[c]?.nota; if (typeof n === 'number') v.notas[c].push(n); }
    porVend.set(a.vendedor, v);
  }
  const vendedores = [...porVend.entries()].map(([nome, v]) => {
    const m = Object.fromEntries(CRIT.map((c) => [`nota_${c}`, media(v.notas[c])]));
    return { vendedor: nome, chamadas_gravadas: v.chamadas, conversas: v.conversas, engajados: v.engajados,
      taxa_engajamento: v.conversas ? Math.round((v.engajados / v.conversas) * 100) / 100 : null, ...m,
      nota_geral: media(Object.values(m).filter((x) => x != null)) };
  }).sort((a, b) => (b.nota_geral ?? 0) - (a.nota_geral ?? 0));

  if (formato === 'leads.csv') { res.setHeader('content-type', 'text/csv; charset=utf-8'); return res.send(csv(leads)); }
  if (formato === 'vendedores.csv') { res.setHeader('content-type', 'text/csv; charset=utf-8'); return res.send(csv(vendedores)); }
  const contagem = (arr, k) => arr.reduce((acc, x) => ((acc[x[k] ?? 'sem_valor'] = (acc[x[k] ?? 'sem_valor'] || 0) + 1), acc), {});
  return res.status(200).json({
    gerado_em: new Date().toISOString(), analises: an.length, telefones: leads.length,
    por_classificacao: contagem(leads, 'classificacao'), por_proximo_passo: contagem(leads, 'proximo_passo'),
    vendedores, alertas: an.filter((a) => a.alertas?.length).map((a) => ({ id: a.id, vendedor: a.vendedor, alertas: a.alertas })),
    top_leads: leads.slice(0, 30),
  });
}

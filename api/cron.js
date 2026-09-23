// Varredura de segurança (cron diário do Vercel): pega qualquer gravação das últimas 48 h que o
// webhook tenha perdido. Também pode ser chamada manualmente com ?key=<CRON_SECRET>&horas=N.
import { varrer, autorizado } from './_lib/chamadas.js';

export const config = { maxDuration: 300 };

export default async function handler(req, res) {
  if (!autorizado(req, 'CRON_SECRET')) return res.status(401).json({ erro: 'não autorizado' });
  const horas = Number(new URL(req.url, 'http://x').searchParams.get('horas')) || 48;
  try {
    return res.status(200).json(await varrer({ horas, orcamentoMs: 270_000 }));
  } catch (e) {
    return res.status(500).json({ erro: String(e.message || e) });
  }
}

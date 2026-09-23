// Recebe o webhook "channel-hangup" da API4COM a cada chamada encerrada e processa as gravações
// pendentes das últimas 2 horas (inclui a chamada que acabou de terminar).
// URL configurada na API4COM: https://<dominio>/api/webhook?key=<WEBHOOK_SECRET>
import { varrer, autorizado } from './_lib/chamadas.js';

export const config = { maxDuration: 300 };

export default async function handler(req, res) {
  if (!autorizado(req, 'WEBHOOK_SECRET')) return res.status(401).json({ erro: 'não autorizado' });
  // a gravação pode levar alguns segundos para ficar disponível depois do hangup
  await new Promise((r) => setTimeout(r, 8000));
  try {
    const r = await varrer({ horas: 2, orcamentoMs: 250_000 });
    return res.status(200).json(r);
  } catch (e) {
    return res.status(500).json({ erro: String(e.message || e) });
  }
}

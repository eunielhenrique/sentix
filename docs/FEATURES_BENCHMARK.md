# Sentix — Funcionalidades sugeridas a partir do benchmark (22/09/2026)

Fonte: `reports/Benchmark de plataformas Sentix.md`. Ordem = prioridade sugerida.
Escopo já definido (não repetido aqui): discador, kanban, leads Meta com distribuição, WhatsApp por QR,
análise de IA de ligações e chats, gamificação, agente de voz Retell.

## A. Faixas abertas (nenhum concorrente brasileiro tem)

1. **Plano de coaching por vendedor** — página por vendedor com os 6 critérios da rubrica ao longo do
   tempo, 3 pontos fortes, 3 a melhorar, trechos reais como exemplo e uma meta da semana. O Gong só faz
   isso em inglês; PipeRun dá dicas por ligação, não plano. É o que justifica a IA no preço do assento.
2. **Pontuação de WhatsApp e ligação na mesma régua** — mesma rubrica, mesmo ranking. Koee pontua só chat,
   PipeRun só voz. Ninguém junta.
3. **Lead Ads nativo no plano de entrada** — captura, distribuição e SLA de primeiro contato sem Zapier.
   Só a Meets tem nativo e os demais cobram no plano intermediário.

## B. O que o mercado já considera básico e a Sentix ainda não listou

4. **Discador em modo power/preview** — fila do vendedor toca o próximo card sozinho ao desligar
   (Callix, Nvoip, Meetime têm). Preditivo não: exige operadora própria e esbarra na regra anti-robocall.
5. **Classificador de caixa postal e chamada curta** — API4COM cobra chamada acima de 3 s e classifica
   voicemail; a Sentix precisa detectar caixa postal para não contar como "tentativa" nem gastar minuto.
6. **BINA por região e Origem Verificada** — número de saída com o DDD do lead (Directcall, API4COM) e
   suporte a STIR/SHAKEN desde o dia 1, obrigatório acima de 500 mil chamadas/mês.
7. **Resumo automático e próximos passos por interação** — já é padrão em Kommo, Digisac, Umbler,
   Exact. Entra como saída da mesma análise da rubrica, sem custo extra.
8. **Agendamento de mensagem e follow-up com lembrete** — padrão em todos os WhatsApp CRM.

## C. Exigidas pela regulação (viram diferencial de confiança)

9. **Registro de consentimento e base legal por lead** — origem do consentimento (formulário Meta,
   opt-in no WhatsApp), aviso de gravação na chamada, opt-out em 48 h no WhatsApp, e base legal
   separada para análise por IA. Cobre LGPD, Meta e TSE; nenhum concorrente expõe isso na interface.
10. **Painel de saúde do número de WhatsApp** — mensagens novas/dia, taxa de resposta, bloqueios e
    desconexões por vendedor, com limite automático. Kommo tem 220+ reclamações por banimento após
    disparo; quem mostra o risco antes vende segurança.

## D. Para depois (dependem de escala ou de operadora própria)

- Fila de atendimento receptivo com URA simples e horário (Huggy, Zenvia).
- Discador preditivo (só com tronco próprio e volume).
- Loja de recompensas na gamificação (SalesScreen/Spinify têm; só faz sentido com vários clientes).
- Marketplace de integrações (Pipedrive, RD, HubSpot) — a Sentix substitui o CRM, então é entrada de
  dados, não saída; adiar até um cliente pedir.

## O que NÃO copiar

- "Ilimitado" de voz sem operadora própria (API4COM oscilou R$ 249,90 → 199,90 → 209,90 por isso).
- Setup de R$ 1.000 a 3.800 e contrato de 12 meses (Poli, RD, Octadesk): a tese da Sentix é sem
  setup e cancela quando quiser.
- Prometer "sem bloqueio" no WhatsApp por QR.

# Sentix — Planos, preços e viabilidade comercial (22/09/2026)

Base: `reports/Benchmark de plataformas Sentix.md` + catálogo e tarifa reais da API4COM lidos hoje
(Ilimitado R$ 209,90 mensal / R$ 169,90 anual; IA4COM +R$ 129,90; pré-pago R$ 0,41/min celular e
R$ 0,09/min fixo, cobrado por minuto iniciado).

## Planos sugeridos (por vendedor/mês, em reais, sem setup, sem fidelidade; anual −15 %)

| Plano | Mensal | Anual | O que inclui |
|---|---|---|---|
| **Conversas** | R$ 149 | R$ 127 | WhatsApp por QR ou API oficial, kanban, entrada automática de leads (WhatsApp e Lead Ads), distribuição, cadência, IA no chat (sugerir/otimizar, análise da conversa), gamificação, painel do gestor |
| **Completo** | R$ 299 | R$ 254 | Tudo do Conversas + discador web com **300 min** de voz, gravação, transcrição e análise de ligações, coaching por vendedor, BINA dinâmica, classificador de caixa postal |
| **Pro** | R$ 449 | R$ 382 | Tudo do Completo com **800 min** de voz + plano de coaching semanal + **100 min de agente de voz IA** + relatórios avançados e webhooks |

Adicionais: minuto de voz excedente R$ 0,55 (fixo R$ 0,15); agente de voz IA R$ 1,50/min; templates
de WhatsApp oficial repassados com +25 %; assento Gestor (sem voz) grátis até 1 por 5 vendedores.
Mínimo de 3 assentos. Teste grátis de 14 dias no Conversas com importação de planilha.

Por que esses números: o pacote que o cliente compra hoje em três fornecedores (CRM R$ 59–131 +
API4COM Ilimitado R$ 169,90–209,90 + IA4COM R$ 99,90–129,90) fica entre R$ 330 e R$ 470 por vendedor,
sem kanban de WhatsApp, sem leads da Meta e sem gamificação. O Completo entra 10–35 % abaixo com mais
módulos. O Conversas compete com Umbler Talk (R$ 99,90–219,90), Kommo (~R$ 106–239) e Meets (R$ 89)
entregando gamificação e coaching que nenhum deles tem.

## Margem por assento (custo direto estimado)

| Plano | Custo hoje (voz na API4COM pré-paga) | Margem | Custo com operadora própria (R$ 0,10/min) | Margem |
|---|---|---|---|---|
| Conversas R$ 149 | motor WhatsApp ~R$ 8 + IA ~R$ 4 + infra ~R$ 5 = **R$ 17** | **89 %** | igual | 89 % |
| Completo R$ 299 | 300 min × 0,41 = R$ 123 + IA ~R$ 15 + WA/infra R$ 13 = **R$ 151** | **49 %** | 300 × 0,10 = R$ 30 + 28 = **R$ 58** | **81 %** |
| Pro R$ 449 | 800 × 0,41 = R$ 328 + 100 min IA voz × ~R$ 1,00 = R$ 100 + R$ 30 = **R$ 458** | **−2 %** | 800 × 0,10 = R$ 80 + 100 + 30 = **R$ 210** | **53 %** |

Leitura: **Conversas e Completo vendem desde já.** O **Pro só existe depois da operadora própria**
(ou com o assento Ilimitado anual da API4COM a R$ 169,90 como custo, que dá 33 % de margem no Pro).
Se um cliente do Completo usar mais de 300 min, o excedente a R$ 0,55 cobre o custo de R$ 0,41.

## Somos vendáveis? Sim, com duas condições

**A favor**
1. Ninguém no Brasil junta os seis módulos; gamificação não existe em nenhum WhatsApp CRM ou
   telefonia nacional; Lead Ads nativo e coaching por vendedor são faixas abertas.
2. Mercado grande e sem sistema: 82 % das pequenas empresas vendem principalmente pelo WhatsApp e só
   29 % usam CRM. O cliente-alvo não troca de CRM, ele ganha o primeiro.
3. Canal de venda já existe: a agência gerencia dezenas de contas de anúncio de clientes (varejo,
   serviços, campanhas). Cada conta que roda anúncio de "Conversas no WhatsApp" é um cliente natural
   da Sentix, vendida junto com o tráfego.
4. Caso de uso próprio como prova: a operação da campanha (540 leads, 67 % sem contato) vira o estudo
   de caso de "antes e depois" em 30 dias.
5. Custo de IA baixo (centavos por interação) permite incluir a IA no assento em vez de vender como
   adicional caro, que é o que a API4COM faz.

**Condições**
1. **Voz com margem exige operadora própria.** Enquanto a API4COM for o custo, vender só Conversas e
   Completo, com limite de 300 min e excedente cobrado. Pro entra depois do SIPPulse + tronco.
2. **WhatsApp por QR precisa de contrato claro.** O cliente assina termo reconhecendo que número
   pessoal por QR está sujeito às regras da Meta; a Sentix entrega limites, aquecimento e painel de
   saúde, e oferece a API oficial como alternativa. Nunca vender "sem bloqueio".

**Metas para provar a tese (90 dias)**: 5 clientes pagantes no Conversas/Completo (3 vindos da
carteira da agência), NPS > 50, churn mensal < 5 %, custo de IA < 5 % da receita, um caso publicado.

## Posicionamento em uma frase

"A Sentix coloca WhatsApp, telefone, leads da Meta e IA de coaching no mesmo lugar, em reais, sem
setup e sem fidelidade, e transforma cada vendedor num jogador com pódio."

## Revisão 22/09 (após questionamento do Euniel)

**Agente de voz (Retell), custo por minuto em pt-BR, página de preços vista em 22/09/2026:**
infraestrutura de voz US$ 0,055 + voz ElevenLabs US$ 0,040 (ou Cartesia/Retell US$ 0,015) + modelo
Gemini 3.5 Flash US$ 0,048 + tronco SIP próprio sem custo = **US$ 0,118 a 0,143/min** (R$ 0,63 a 0,76 a
R$ 5,30/US$). Somando a terminação brasileira: hoje R$ 0,41 (API4COM) → **R$ 1,04 a 1,17/min**; com
operadora própria a R$ 0,10 → **R$ 0,73 a 0,86/min**. Inclui 20 chamadas simultâneas; extra US$ 8/mês
cada. A Retell não vende número brasileiro: é tronco SIP próprio, e há relato de julho/2026 de
falha com operadora brasileira ainda sem solução pública. Logo, 100 min de agente custam **R$ 104 a
117 hoje** e R$ 73 a 86 com tronco próprio; vendidos a R$ 1,50/min rendem 22 % a 51 % de margem.
Correção: a linha do Pro usava R$ 1,00/min; o custo real hoje é R$ 1,04–1,17. Conclusão mantida:
Pro só depois da operadora própria e do teste de compatibilidade Retell + SIPPulse.

**300 minutos no Completo:** são minutos **falados** (não atendida, caixa postal e cancelada não
custam nada na API4COM). 300 min = ~100 conversas de 3 min por vendedor/mês, ou ~5 por dia útil, o que
cobre a operação de campanha observada (ligações de 10 s a 3 min). É também o mesmo corte que a
API4COM usa no plano Negociação para "closers/pré-vendas", então o cliente reconhece a régua. A R$ 0,41
o custo é R$ 123 e a margem do Completo fica em 49 %; com 500 min inclusos a margem cairia para 22 %.
Alternativa se o cliente pedir mais: Completo 500 a R$ 349 (margem 33 % hoje, 75 % com tronco próprio).

**Plano de coaching semanal:** é a página por vendedor que, toda segunda, mostra a evolução dos 6
critérios (8 semanas), 3 pontos fortes e 3 a melhorar com trechos reais, e **uma meta da semana**
acompanhada pelo gestor (spec em `PROMPT_FRONT_F4.md`, §3). Decisão revista: a análise por interação e
a página do vendedor entram no **Completo**; o Pro diferencia por volume (800 min), agente de voz e
relatórios avançados, não por esconder o coaching. Coaching é o argumento de venda, não o adicional.

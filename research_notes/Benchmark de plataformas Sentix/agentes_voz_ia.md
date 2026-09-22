# Plataformas de agentes de voz com IA (ligações telefônicas) — foco Brasil / pt-BR

Data de coleta: 2026-09-22 (todos os "visto em" abaixo referem-se a esta data, salvo indicação). Todos os preços internacionais em USD; brasileiros em BRL quando publicados.

## KQ1 — Retell AI: preço por minuto, SIP trunking, pt-BR, pós-chamada, limites

### Takeaway
Retell cobra por componente: infraestrutura de voz US$0,055/min + TTS US$0,015–0,040/min + LLM US$0,048–0,16/min + telefonia (Twilio US$0,015/min ou SIP próprio sem custo), resultando na faixa anunciada de US$0,07–0,31/min; pt-BR é idioma oficialmente suportado e BYO SIP trunk (TCP/UDP/TLS, PCMU/PCMA/G.722) é gratuito, mas há relato recente (jul/2026) de falha com operadora VoIP brasileira.

### Cited Findings
- Faixa anunciada "AI Voice Agents: $0.07–$0.31/min"; chat "$0.002+/msg"; US$10 em créditos grátis — [Retell pricing](https://www.retellai.com/pricing) (visto 2026-09-22)
- "Retell Voice Infrastructure": US$0,055/min — [Retell pricing](https://www.retellai.com/pricing)
- TTS: Retell Platform/Minimax/Fish/Cartesia/OpenAI/Inworld US$0,015/min; ElevenLabs US$0,040/min — [Retell pricing](https://www.retellai.com/pricing)
- LLM (tier Standard, por minuto): GPT 5.6 Terra US$0,064; Claude 5 Sonnet US$0,064; GPT 5.5 US$0,16; GPT 5.4 US$0,080; Claude 4.5 Sonnet US$0,08; Gemini 3.5 Flash US$0,048 — [Retell pricing](https://www.retellai.com/pricing)
- Telefonia: chamadas padrão "$0.015/min" (exemplo Twilio EUA); "SIP Trunking/Custom Telephony: No Charge"; número Retell US$2,00/mês; número verificado US$10,00/mês — [Retell pricing](https://www.retellai.com/pricing)
- Add-ons: Knowledge Base US$0,005/min ou US$8/mês; Advanced Denoising US$0,005/min; Safety Guardrails US$0,005/min; PII Removal US$0,01/min; AI Quality Assurance 100 min grátis e depois US$0,10/min; Branded Call US$0,10/chamada saída — [Retell pricing](https://www.retellai.com/pricing)
- Concorrência: 20 chamadas simultâneas incluídas; adicional US$8,00/concorrência/mês; Enterprise "Custom Pricing" — [Retell pricing](https://www.retellai.com/pricing)
- Telefonia customizada: dois métodos — "Elastic SIP Trunking" (recomendado) e "Dial to SIP URI" (este último não suporta o recurso de transferência de chamada); provedores com guia: Twilio, Telnyx, Vonage; contact centers Avaya, Genesys Cloud, Five9, Amazon Connect; "qualquer provedor com SIP trunk" — [Retell docs custom telephony](https://docs.retellai.com/deploy/custom-telephony)
- Requisitos SIP: servidor `sip:sip.retellai.com`; transporte TCP (recomendado), UDP, TLS ou mTLS; codecs PCMU, PCMA, G.722; SRTP exige TLS; IPs para allowlist 18.98.16.120/30, 3.42.144.0/23, 153.57.128.0/18 (+143.223.88.0/21, 161.115.160.0/19 para parte do tráfego EUA); chamada via "Dial to SIP URI" deve conectar em até 5 min após registro na API — [Retell docs custom telephony](https://docs.retellai.com/deploy/custom-telephony)
- Página dedicada "Portuguese (Brazil) AI Voice Agents": pt-BR está entre "55+ idiomas"; claims genéricos de "industry-leading low latency"; compliance SOC 2 Type II, HIPAA, PCI, GDPR, TCPA; casos de uso listados incluem "Sales Outreach and Lead Qualification", "Appointment Scheduling and Reminders", "Surveys and Feedback"; a página NÃO informa vozes, engine de transcrição, latência em ms, números no Brasil nem cases — [Retell pt-BR page](https://www.retellai.com/languages-ai/brazil-portuguese-ai)
- Relato de integração BYO SIP com operadora brasileira "Fale Vono" (URI 190.89.248.47 / vono2.me): chamadas de saída com status "dial no answer", provedor não recebia INVITE; thread aberta em 20/07/2026, suporte pediu Call ID/Org ID em 21/07/2026, sem resolução pública — [Retell community](https://community.retellai.com/t/retell-byo-sip-trunk-not-sending-invite-to-provider-dial-no-answer/3387)
- Relato anterior: número Retell conectado via Twilio Elastic SIP Trunk "conecta cerca de 50% das vezes" — [Retell community](https://community.retellai.com/t/my-retell-phone-number-connected-via-twilio-elastic-sip-trunk-connects-about-50-of-the-time/1063)
- Pós-chamada: webhook `call_analyzed` disparado após `call_ended` (o payload de call_ended NÃO traz `call_analysis`); campos customizados de extração tipos Boolean, Text, Number, Enum; leitura via webhook ou Get Call API em `call.call_analysis.custom_analysis_data`; campos não são populados em chamadas não conectadas/sem conversa — [Retell docs post-call](https://docs.retellai.com/features/post-call-analysis-overview); [Retell feature page](https://www.retellai.com/features/post-call-analysis)
- Relato de usuários de variáveis de pós-chamada ausentes no payload do webhook — [Retell community](https://community.retellai.com/t/post-call-analysis-variables-missing-from-webhook-payload-anyone-else/2949)
- Comparativo de terceiro (SquadStack, 09/07/2026): Retell "advertised $0.07/min", "true all-in $0.13–$0.31/min" — [SquadStack](https://www.squadstack.ai/voicebot/ai-outbound-calling-cost)
- Comparativo de concorrente (EchoCall, 22/05/2026, fonte interessada): latência Vapi/Retell "400–500 ms" vs. "<200 ms" própria — [EchoCall](https://echocall.de/en/blog/ai-voice-agent-statistik-2026)

### Inferences
- Custo típico Retell para ligação em pt-BR com voz ElevenLabs + Gemini 3.5 Flash + SIP próprio: 0,055 + 0,040 + 0,048 = ~US$0,143/min (+ custo da operadora brasileira), antes de add-ons; com voz Cartesia/Retell cai a ~US$0,118/min.
- Números telefônicos brasileiros não são vendidos diretamente pela Retell (a página cita Twilio/EUA); operação no Brasil implica BYO SIP com operadora local (ex.: Fale Vono, Nvoip, VulcaNet, Twilio BR) — e há evidência de atrito de compatibilidade.

### Gaps
- Retell não publica latência em ms para pt-BR nem lista de vozes pt-BR; nenhum case brasileiro localizado.
- Não encontrei confirmação de disponibilidade de números brasileiros nativos na Retell.

## KQ2 — Vapi, Bland, ElevenLabs, Synthflow (e Air AI, Twilio/Google/Vonage): preço, telefonia, pt-BR, recursos

### Takeaway
Vapi cobra US$0,05/min de plataforma + provedores pass-through (total ~US$0,15–0,33/min all-in); Bland é all-in US$0,12–0,14/min; ElevenLabs Agents é US$0,08/min (LLM à parte, telefonia "at cost") com planos de US$0 a US$990/mês; Synthflow migrou para modelo enterprise (a partir de US$30k/ano) com PAYG relatado por terceiros em ~US$0,09/min de engine; Air AI exige licença de US$25k–100k.

### Cited Findings
**Vapi**
- Plataforma: "$0.05/min" pay-as-you-go; Pro "10% of Vapi hosting fee" com "$999/mo minimum"; US$5 de crédito grátis — [Vapi pricing](https://vapi.ai/pricing)
- Pass-through: Deepgram STT "$0.0095–$0.0099/min"; LLM OpenAI "$0.0077–$0.0452/min"; voz ElevenLabs "$0.0146–$0.0238/min" — [Vapi pricing](https://vapi.ai/pricing)
- Telefonia: Vapi Telephony/SIP: grátis; Twilio inbound US$0,008/min, outbound US$0,014/min; Vonage US$0,00814/min; Telnyx US$0,0055/min — [Vapi pricing](https://vapi.ai/pricing)
- Números/concorrência: sem plano = 1 número e 4 chamadas simultâneas; Core US$29/mês = 5 números, 10 simultâneas; Pro (mín. US$999/mês) = 10 números, 30 simultâneas; extra "$10/line/month"; HIPAA "$2,000/month"; org adicional US$20/mês — [Vapi pricing](https://vapi.ai/pricing)
- Idiomas: docs de Vapi citam suporte a Português entre 30+/100+ idiomas, com configuração por código de idioma (ex. es-ES) — [Vapi docs multilingual](https://docs.vapi.ai/assistants/examples/multilingual-agent); [Vapi voices](https://docs.vapi.ai/providers/voice/vapi-voices)
- Terceiro (SquadStack): Vapi "advertised $0.05/min; true all-in $0.15–$0.33/min" — [SquadStack](https://www.squadstack.ai/voicebot/ai-outbound-calling-cost)

**Bland AI**
- Start (US$0): "$0.14/min" talk time, "$0.05/min" transfers; inclui "2 credits + an inbound number ($15/mo value)"; 10 chamadas simultâneas, 100/dia, 1 voz, 10 knowledge bases — [Bland pricing](https://www.bland.ai/pricing)
- Build (US$299/mês): "$0.12/min", transfers "$0.04/min"; 50 simultâneas, 2.000 chamadas/dia, 5 vozes, 50 KBs — [Bland pricing](https://www.bland.ai/pricing)
- Enterprise: custom, on-prem/VPC, engenheiro dedicado; per-minute inclui "LLM, No token charges, STT, TTS Premium voices"; BYOT (bring your own telephony) suportado e "BYOT customers do not pay transfer fees" — [Bland pricing](https://www.bland.ai/pricing)
- Idiomas: modelo de transcrição "Fluent" suporta 6 idiomas incl. Português; "Auto" suporta 10 incl. Português; TTS em Português marcado como "experimental" — [Bland Fluent blog](https://www.bland.ai/blog/fluent-next-generation-multilingual-transcription-voice-agents); [Bland multilingual blog](https://www.bland.ai/blog/multilingual-ai-voice-assistant)
- Conflito: SquadStack lista Bland como "$0.09/min advertised" (jul/2026) vs. US$0,12–0,14 na página oficial (set/2026) — [SquadStack](https://www.squadstack.ai/voicebot/ai-outbound-calling-cost) vs. [Bland pricing](https://www.bland.ai/pricing)

**ElevenLabs Agents (ElevenAgents)**
- Todos os planos pagos: "$0.080/minute" (incluídos e adicionais); burst acima da concorrência "$0.160/minute"; SMS "$0.003/message" — [ElevenLabs agents pricing](https://elevenlabs.io/pricing/agents)
- Planos: Free US$0/15 min/4 simultâneas; Starter US$6/75 min/6; Creator US$22 (US$11 1º mês)/275 min/10; Pro US$99/1.238 min/20; Scale US$299/3.738 min/30; Business US$990/12.375 min/40; Enterprise custom — [ElevenLabs agents pricing](https://elevenlabs.io/pricing/agents)
- LLM: "fees for model usage ... deducted from your ElevenLabs credits" (pass-through); telefonia "at cost" — [ElevenLabs agents pricing](https://elevenlabs.io/pricing/agents)
- SIP trunking: inbound e outbound; autenticação digest (usuário/senha) ou ACL; TLS 1.2+ obrigatório para sinalização; TCP/TLS prontos para produção, UDP experimental; codecs G711 8 kHz ou G722 16 kHz; provedores testados "Twilio, Vonage, RingCentral, Sinch, Infobip, Telnyx, Exotel, Plivo, Bandwidth"; SIP com IP estático (/24) em US, EU, Índia, Singapura "available for Enterprise accounts" — [ElevenLabs SIP docs](https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking)
- pt-BR/latência: ElevenLabs em página PT afirma captar "sotaques locais" em português; Flash v2.5 com "~75 ms" de inferência e "<500 ms" end-to-end — [ElevenLabs TTS português](https://elevenlabs.io/pt/text-to-speech/portuguese); [ElevenLabs API pt](https://elevenlabs.io/pt/api)
- Comparativo de terceiro: "ElevenLabs leads on voice quality and latency: Sub-100ms latency, 11,000+ voice options, and 70+ languages" — [DigitalApplied](https://www.digitalapplied.com/blog/voice-ai-agents-business-elevenlabs-vapi-retell-bland)

**Synthflow**
- Página oficial mostra apenas Enterprise "starting $30,000 annually", inclui "Synthflow Native Telephony, SIP trunking, or approved enterprise telephony", "CRM, calendar, contact-center stack, webhook, API"; "65M+ voice calls every month in 30+ countries"; SOC 2, GDPR, HIPAA, ISO 27001; G2 4,5/5 com 1.000+ reviews — [Synthflow pricing](https://synthflow.ai/pricing)
- Terceiros (2026): planos legados Starter US$29/50 min, Pro US$450/2.000 min, Growth US$900/4.000 min, Agency US$1.400/6.000 min foram aposentados; PAYG atual "$0.09/minute" de engine + LLM US$0,02–0,05 + telefonia US$0–0,02 = "$0.11–$0.24/min" — [Ringly](https://www.ringly.io/blog/synthflow-pricing); [Layer3Labs](https://www.layer3labs.io/guides/synthflow-pricing); [VoiceAI.guide](https://voiceai.guide/synthflow-review/pricing) — NÃO confirmado na página oficial

**Air AI**
- Terceiros: outbound US$0,11/min, inbound US$0,32/min; licença "US$25.000 a US$100.000"; carrier US$0,0075–0,015/min; cobra tempo de toque ("ringing time"); "does not publish detailed pricing publicly as of April 2026"; estimativa "$0.20–$0.40/min", tiers US$1.499 a US$14.999+/mês — [Lindy](https://www.lindy.ai/blog/airai-pricing); [ServiceAgent](https://serviceagent.ai/blogs/air-ai-review/); [Tested.media](https://tested.media/air-ai-review/)

**Twilio / Google / Vonage**
- Twilio ConversationRelay: "$0.07/minute"; "Voice costs are calculated separately"; STT/TTS não incluídos; Conversation Intelligence: operadores Twilio US$0,005/1K chars, custom input US$0,002/1K, output US$0,018/1K — [Twilio conversational AI pricing](https://www.twilio.com/en-us/products/conversational-ai/pricing)
- Google Conversational Agents (Dialogflow CX): cobra por "seconds of audio" para agentes de voz; comparativo Retell estima "US$600–800 para 5.000 min/mês" — [Google pricing](https://cloud.google.com/products/conversational-agents/pricing); [Retell comparativo](https://www.retellai.com/resources/inbound-vs-outbound-callers-pricing-comparison-2025)
- Vonage AI Studio: tier grátis; planos pagos "a partir de ~US$1.000/mês"; NLU "$0.00803/text request" — [Vonage AI Studio pricing](https://www.vonage.com/communications-apis/ai-studio/pricing/); [BytePlus](https://www.byteplus.com/en/topic/552056)

### Inferences
- ElevenLabs tem o preço de plataforma mais previsível (US$0,08/min flat, LLM à parte) e a melhor evidência pública de qualidade de voz em pt-BR (TTS próprio); Retell/Vapi podem usar as vozes ElevenLabs por pass-through, o que iguala a qualidade de voz mas soma custo.
- Para o Brasil, o gargalo comum é telefonia: nenhuma das cinco vende número BR nativo de forma documentada; o caminho é SIP trunk de operadora brasileira (grátis na Retell/Vapi/ElevenLabs; ElevenLabs IP-estático só Enterprise).

### Gaps
- Synthflow: página oficial não expõe PAYG/tiers; números PAYG vêm apenas de blogs de concorrentes.
- Air AI: sem página de preço oficial; tudo é reporte de terceiros.
- Nenhuma medição independente de latência para pt-BR localizada (só claims de fornecedores).

## KQ3 — Alternativas brasileiras e preços em BRL

### Takeaway
Os players brasileiros com preço público são VulcaNet (agente de voz IA "a partir de R$499/mês"), Toolzz Voice (R$899/mês com 1.000 min a R$3.900+/mês), API4COM (telefonia R$169,90–209,90/usuário/mês + IA4COM R$99,90–129,90/usuário/mês, mas o IA4COM é copiloto de vendedor, não agente de voz autônomo) e Zenvia (voz no WhatsApp R$0,0812–0,0950/min); Vozy, Nvoip, Ligo, Leucotron e Cloudia não publicam preço de agente de voz telefônico.

### Cited Findings
- VulcaNet "Agente de Voz": "a partir de R$499 por mês" (Plano Crescimento); preço final por volume de chamadas/minutos, canais simultâneos, números, integrações; inclui receptivo 24x7, ativo para vendas/cobrança/agendamento, integração CRM/ERP/agenda/PABX/APIs/webhook, gravação, transcrição, classificação de intenção; handoff humano com "resumo da conversa", intenção detectada e dados coletados; registra "protocolo, desfecho, próxima ação"; cita LGPD, Origem Verificada (STIR/SHAKEN), RCD, "Não Perturbe" e horários adequados — [VulcaNet](https://vulcanet.com.br/solucoes/telefonia/agente-de-voz/)
- Toolzz Voice: planos "a partir de R$899/mês com 1.000 minutos inclusos" (Mini) até Enterprise "a partir de R$3.900/mês" — [Toolzz Voice](https://toolzz.dev/voice); [Toolzz LP](https://www.toolzz.com.br/lp/agente-ia-voz-automacao-aa3d63)
- API4COM: plano Ilimitado (telefonia, minutos ilimitados/usuário) R$209,90/usuário/mês mensal ou R$169,90 anual; IA4COM (IA) R$129,90/usuário/mês mensal ou R$99,90 anual; IA4COM é "assistente de vendas ... especialista em SPIN Selling ... orienta o vendedor" (copiloto, não agente autônomo); assinaturas independentes — [API4COM](https://www.api4com.com/)
- Zenvia (BRL, via terceiro): Starter R$0 (1 usuário, 100 interações), Specialist R$600/mês (10 usuários), Expert R$1.800/mês (30), Professional R$3.900/mês (50), Enterprise sob consulta; "Solução Completa de Voz no WhatsApp" R$0,0950 a R$0,0812/min; canais a partir de R$100/mês; setup WhatsApp a partir de R$649 — [Nação Digital](https://nacao.digital/blog/agentes-de-ia-para-atendimento/)
- Zenvia (USD, página oficial EN): Starter US$0; Specialist US$130; Expert US$390; Professional US$845/mês; setup US$137–842; voz no WhatsApp US$0,0235–0,0342/min; a página NÃO menciona agente de voz IA para telefone (PSTN) — [Zenvia prices](https://zenvia.com/en/prices/)
- Vozy (Lili / Lili Resolve): assistente de voz com IA generativa; sem preço público, venda por demo/consulta — [Vozy](https://www.vozy.ai/en/soluciones/lili-resolve); [Vozy soluciones](https://www.vozy.co/soluciones)
- Nvoip: modelo de créditos para ligar/receber por número nacional; tem produto "Voicebot com IA na sua telefonia"; página de planos retornou 403 e reajuste de preços em 2026 anunciado sem valores nos resultados — [Nvoip voicebot](https://www.nvoip.com.br/voicebot/); [Nvoip reajuste 2026](https://www.nvoip.com.br/blog/novidades/reajuste-de-precos-nvoip-2026/)
- Cloudia: secretária virtual com IA para clínicas; canal principal WhatsApp (+ Messenger/Instagram/site); "Agente de IA que responde áudio com áudio" (mensagens de voz, não ligações); implementação "a partir de R$700"; número WhatsApp extra R$200/mês; resumo IA adicional R$100/mês; usuário extra R$30/mês; preços mensais não renderizados na página ("-- /Mensal") — [Cloudia planos](https://cloudia.com.br/planos/); [Cloudia](https://cloudia.com.br/)
- Ligo Cloud: plataforma com "bots de texto e voz", módulos Ligo Journeys, Dialer, Bots, IVR, Omni; sem preço público — [Ligo](https://ligo.cloud/); [Ligo contact center](https://ligo.cloud/segmento-contact-center/)
- Leucotron Tech: "atendimento por voz e chat com agentes de IA e análise inteligente de conversas em uma única plataforma"; sem preço público — [Leucotron](https://leucotron.com.br/)
- Talkdesk: nenhum preço ou dado pt-BR específico localizado nas buscas realizadas — (gap)

### Inferences
- Nenhum player brasileiro publica preço por minuto de agente de voz IA para PSTN; o mercado local vende por mensalidade/projeto (VulcaNet, Toolzz) ou por assento (API4COM), o que dificulta comparação direta com o modelo por minuto dos players globais.
- Cloudia e Zenvia são essencialmente WhatsApp-first; não são substitutos diretos para ligações telefônicas com IA.

### Gaps
- Preços de Vozy, Nvoip (voicebot), Ligo, Leucotron, Talkdesk não localizados.
- Não encontrei benchmark ou review independente de qualidade de voz/latência dos players brasileiros.

## KQ4 — Regulatório no Brasil: 0303, Não Me Perturbe, robocalls, LGPD

### Takeaway
O prefixo 0303 deixou de ser obrigatório em 14/08/2025 (Acórdão nº 201/2025) e foi substituído pela autenticação de chamadas "Origem Verificada" (STIR/SHAKEN, Resolução nº 777/2025), obrigatória desde 15/11/2025 para quem origina >500 mil chamadas/mês e para todos até out/2028; a cautelar anti-robocall (bloqueio de quem dispara ≥100 mil chamadas/dia com ≥85% de até 6 s) foi prorrogada até 31/10/2028; o "Não Me Perturbe" cobre telecom e crédito consignado/cartão; LGPD exige informar gravação e base legal, e o uso da gravação para IA exige finalidade compatível/base própria.

### Cited Findings
**Prefixo 0303**
- Anatel: Ato nº 10.413/2021 criou o 0303 para telemarketing ativo; Ato nº 12.712/2024 define procedimentos; Acórdão nº 201 (14/08/2025) tornou o uso do 0303 **facultativo** e impôs autenticação de chamadas — [Anatel 0303](https://www.gov.br/anatel/pt-br/regulado/numeracao/telemarketing-ativo-prefixo-0303)
- Regra anterior (2022) exigia 0303 de empresas com mais de 10.000 chamadas/dia; a Anatel revogou porque consumidores passaram a bloquear/ignorar tudo que começa com 0303 — [Exame](https://exame.com/brasil/anatel-deixa-de-exigir-uso-do-prefixo-0303-em-ligacoes-de-telemarketing/); [Meireles e Freitas](https://meirelesefreitas.com.br/blog/noticias/anatel-revoga-obrigatoriedade-do-prefixo-0303-veja-o-que-muda/)
- Sanções por descumprimento (prestadoras e empresas de telemarketing): art. 173 da Lei 9.472/97, multa e suspensão do uso de recursos de numeração — [Anatel 0303](https://www.gov.br/anatel/pt-br/regulado/numeracao/telemarketing-ativo-prefixo-0303)

**Origem Verificada / autenticação de chamadas**
- Resolução Anatel nº 777, de 28/05/2025, torna a autenticação obrigatória até 2028 — [Correio Braziliense](https://www.correiobraziliense.com.br/economia/2025/10/7276745-anatel-torna-obrigatoria-a-autenticacao-de-chamadas-telefonicas-ate-2028.html)
- Fase 1: "grandes chamadores" (>500 mil chamadas/mês, somando todos os códigos do mesmo CNPJ incl. filiais, conectadas ou não) obrigados desde 15/11/2025 (90 dias após o Acórdão 201); ~350 empresas, ~50% do tráfego — [Anatel 0303](https://www.gov.br/anatel/pt-br/regulado/numeracao/telemarketing-ativo-prefixo-0303); [Sigatel](https://sigatel.com.br/origem-verificada-stir-shaken/)
- Fase 2: demais prestadoras até out/2028 (3 anos) — [Sigatel](https://sigatel.com.br/origem-verificada-stir-shaken/)
- Tecnologia STIR/SHAKEN + RCD; "autenticação" (obrigatória, invisível) vs. "identificação" (contratada à parte: nome, logo, motivo da chamada); exibição em Samsung Android 14+ (nome, número, selo, logo, motivo) e iOS 18.2+ (nome, número, selo, logo); exige 4G/5G com VoLTE; ~75% dos aparelhos compatíveis em meados de 2025 — [Sigatel](https://sigatel.com.br/origem-verificada-stir-shaken/); [Olhar Digital](https://olhardigital.com.br/2025/10/18/pro/ligacoes-de-grandes-empresas-terao-selo-de-verificacao/)

**Robocalls / chamadas curtas**
- Cautelar da Anatel: bloqueio por 15 dias (pelas operadoras) de quem gera ≥100 mil chamadas/dia com ≥85% de chamadas de até 6 segundos; prorrogada até 31/10/2028 — [Teletime](https://teletime.com.br/27/05/2026/robocall-anatel-2028/); [Convergência Digital](https://convergenciadigital.com.br/telecom/anatel-prorroga-medidas-contra-chamadas-abusivas-ate-2028/); [Mobile Time](https://www.mobiletime.com.br/noticias/30/05/2025/chamadas-curtas-anatel/)
- Multa por descumprimento do acordo: até R$50 milhões — [VCX](https://vcx.solutions/telemarketing-abusivo/)
- Anatel: ~220 bilhões de ligações abusivas deixaram de ser geradas entre jun/2022 e jul/2025 — [Correio Braziliense](https://www.correiobraziliense.com.br/economia/2025/10/7276745-anatel-torna-obrigatoria-a-autenticacao-de-chamadas-telefonicas-ate-2028.html)
- Estimativa de "10 bilhões de robocalls mensais" no Brasil (abr/2025, fonte secundária) — [MixVale](https://www.mixvale.com.br/2025/04/28/procon-e-anatel-enfrentam-a-onda-de-10-bilhoes-de-robocalls-mensais-no-brasil/)

**Não Me Perturbe**
- Cadastro nacional (naomeperturbe.com.br) formalizado pela Anatel e operado pelas prestadoras: bloqueia telemarketing de empresas de telecomunicações e ofertas de crédito consignado/cartão de bancos; NÃO bloqueia confirmação de dados, prevenção a fraude, cobrança; efeito em até 30 dias; gratuito — [Procon SP](https://www.procon.sp.gov.br/bloqueio-de-telemarketing-2/); [Procon RS](https://www.procon.rs.gov.br/passo-a-passo-do-bloqueio); [HPG](https://hpg.com.br/nao-me-perturbe-cadastro-anatel-procon-funciona.html)
- Listas estaduais/municipais de Procon cobrem outros setores (bancos, financeiras, imobiliárias etc.) — [Procon SP](https://www.procon.sp.gov.br/bloqueio-de-telemarketing-2/)
- Mais de 11 milhões de telefones cadastrados em 2022 — [Procon Niterói](https://procon.niteroi.rj.gov.br/2023/01/30/nao-me-perturbe-ultrapassa-11-milhoes-de-telefones-cadastrados-em-2022/)

**LGPD — gravação e IA**
- Gravação de ligação: interlocutor deve consentir ou enquadrar-se em exceção (execução de contrato, proteção da vida, prevenção à fraude, proteção do crédito); é preciso informar que grava e a finalidade; dados não podem ser usados para finalidade não acordada; Decreto 6.523/2008 (SAC) exige retenção de gravações por 90 dias — [Del Grande](https://delgrande.com.br/blog/como-adequar-a-gravacao-de-ligacao-a-lgpd/)
- "Sempre que houver tratamento de dados pessoais, a LGPD se aplica, independentemente da tecnologia ou modelo de IA"; consentimento coletado para uma finalidade não cobre treino de IA; "a mesma gravação pode exigir bases legais diferentes dependendo de como a IA a usa" — [Halk LGPD e agentes de IA](https://www.halk.io/blog/pt/lgpd-agentes-de-ia-compliance); [Confidata](https://confidata.com.br/blog/ia-lgpd-inteligencia-artificial-privacidade)
- Monitoramento por IA em call center e LGPD (guia de fornecedor) — [Intelia](https://blog.intelia.com.br/inteligencia-artificial-e-lgpd-no-call-center-como-monitorar-atendimentos-com-seguranca/)

### Inferences
- Para um agente de voz IA de saída (outbound) no Brasil: abaixo de 500 mil chamadas/mês não há obrigação de autenticação STIR/SHAKEN nem de 0303 hoje, mas a operadora/SIP trunk precisa evitar padrão de "chamadas curtas" (≥100 mil/dia, ≥85% ≤6 s) sob pena de bloqueio — chamadas de IA que caem em caixa postal e desligam rápido podem disparar esse gatilho em escala.
- O Não Me Perturbe é setorial (telecom + crédito); para outros setores, a obrigação prática é honrar opt-out e listas de Procon estaduais; VulcaNet já embute esses controles como diferencial de fornecedor local.
- Recomendação de compliance: anunciar no início da chamada que é um agente automatizado e que a ligação é gravada/transcrita, com base legal definida (legítimo interesse ou consentimento) e retenção ≥90 dias quando for SAC.

### Gaps
- Não localizei regra da Anatel específica sobre "voz sintética/IA deve se identificar como robô" (não parece existir norma dedicada; ausência não confirmada por fonte oficial).
- Não encontrei orientação formal da ANPD sobre transcrição/análise de chamadas por IA.
- Horário permitido de telemarketing: varia por lei estadual/municipal; não pesquisado em detalhe.

## KQ5 — Benchmarks de desempenho de IA em ligações outbound (2025–2026)

### Takeaway
Os dados públicos são majoritariamente de fornecedores: SquadStack (jul/2026) fala em "70% menor custo por lead qualificado" e "até 40% mais conversões"; um piloto interno da VoiceGenie reporta +173% demos e −79% custo/demo; o único estudo revisado por pares (saúde, 2026) mostra 3,4x mais consultas concluídas; em contrapartida, comparativos de SDR reportam que humanos geram 2,6x mais receita e 71% vs. 52% de comparecimento — não existe estudo independente comparando IA vs. humano em agendamento de vendas.

### Cited Findings
- "Cost per qualified lead 70% lower" vs. humanos; "~90% lead connectivity"; "Up to 40% higher conversions"; "ROI Year 1 ~41%"; "2–3x lower CAC"; SDR humano "60–80 calls a day" vs. IA "10,000 to 100,000 calls in a single day"; faixa de mercado "$0.05–$0.15 per minute all-in" (artigo de fornecedor, 09/07/2026) — [SquadStack](https://www.squadstack.ai/voicebot/ai-outbound-calling-cost)
- "AI outbound calls with a personalised script achieve conversation rates of 45 to 60%"; 3x conversão vs. reativação só por e-mail; +38% LTV de reativação em híbrido; IA €0,11–0,19/min em volume vs. €4–8 por conversa humana inbound (Europa); handle time −30–40%; latência >700 ms "desconfortável"; 91% das ligações de reserva em clínicas automatizáveis; no-show 18%→9% com lembretes — [EchoCall, 22/05/2026, fornecedor](https://echocall.de/en/blog/ai-voice-agent-statistik-2026)
- Outreach dataset 2025: chamadas personalizadas por IA com "36% higher meeting conversion rates" vs. genérico — [MarketsandMarkets/SalesPlay](https://www.marketsandmarkets.com/AI-sales/voice-ai-can-agents-successfully-cold-call)
- 28–34% dos times B2B mid-market/enterprise com ≥1 agente de voz IA para prospecção em Q1 2026 (vs. 11% em 2024) — [Auto Interview AI](https://www.autointerviewai.com/blog/ai-calling-statistics-benchmarks-data-2026)
- Invoca 2025 (60 milhões de chamadas): 37% dos leads telefônicos convertem na ligação; 61% falam com pessoa — [Invoca via Seeking Alpha](https://seekingalpha.com/pr/20131959-invoca-releases-definitive-cross-channel-and-cross-industry-buyer-conversion-benchmark-report)
- Estudo revisado por pares (International Conference on AI in Medicine, 2026): IA de voz aumentou conclusão de consultas 3,4x (24,7x em pacientes com conta sem agendamento), volume de chamadas 9x vs. humanos — [PR Newswire](https://www.prnewswire.com/news-releases/study-finds-ai-voice-agents-increased-specialty-care-program-enrollment-rates-340-in-real-world-clinical-setting-302818900.html); [Deepgram](https://deepgram.com/learn/ai-voice-agents-patient-engagement-evidence)
- Comparativo AI SDR vs. humano: humanos geraram 2,6x mais receita (US$147k vs. US$56k) e 71% vs. 52% de show rate; reuniões marcadas por IA com show rate 40–60% vs. 70–85% humanas — [Salesmotion](https://salesmotion.io/blog/ai-sdrs-vs-human-sdrs); [CallingAgency](https://callingagency.com/blog/ai-sdr-vs-human-sdr/)
- Piloto interno VoiceGenie: +173% demos, −79% custo/demo (não revisado por pares) — [VoiceGenie](https://blogs.voicegenie.ai/ai-voice-agent-vs-human-sdr)
- "Zero peer-reviewed studies exist specifically comparing AI voice agents to human SDRs on appointment booking rates in sales contexts" — [VoiceGenie](https://blogs.voicegenie.ai/ai-voice-agent-vs-human-sdr)
- Retell KPIs recomendados para outbound com IA (answer rate, conversion, cost per lead etc.) — [Retell blog KPIs](https://www.retellai.com/blog/the-8-kpis-every-ai-outbound-calling-strategy-should-track)

### Inferences
- Os ganhos consistentes e mais defensáveis são de custo e volume (custo/min 10–50x menor que humano, escala de milhares de chamadas/dia); os ganhos de conversão são contestados e dependem de contexto (saúde/lembretes > vendas frias), com risco de qualidade menor das reuniões (show rate).
- Nenhum benchmark com dado brasileiro (taxa de atendimento de números BR, pt-BR) foi encontrado; qualquer projeção para o Brasil deve descontar o efeito de bloqueio por apps/operadoras pós-robocall (220 bi de ligações bloqueadas) na taxa de atendimento.

### Gaps
- Sem dados de answer rate para outbound de IA no Brasil.
- Sem custo por lead qualificado em BRL publicado por nenhum fornecedor brasileiro.
- Sem estudo independente (não-fornecedor) de conversão IA vs. humano em vendas.

# Sentix — Entrada de leads (verificado em 22/09/2026)

## Como o lead chega hoje (caso Campanha Ratinho / Wesley Cezar)

- Não existe formulário de Lead Ads nas contas da campanha. As campanhas são de vídeo (ThruPlay,
  Views, Alcance) e **uma de "Conversas no WhatsApp"** ("Captacao apoio WhatsApp", conta Fundo
  Eleitoral). O anúncio abre o WhatsApp do candidato/equipe e a pessoa manda a primeira mensagem.
- A planilha "Campanha Ratinho" (criada em 17/09/2026, uma aba, colunas Nome, Telefone, Cidade,
  Feedback, Observação) é preenchida **à mão** pela equipe a partir dessas conversas: sem data, sem
  id, sem anúncio de origem. A "Cidade" é derivada do DDD. Nenhuma automação escreve nela.
- Consequência: 540 leads, 363 nunca ligados, e a origem (qual vídeo, qual praça) se perde.

## O que muda na Sentix

1. **O módulo de WhatsApp é a porta de entrada principal**, não o webhook de Lead Ads. Toda conversa
   nova que chega no número conectado vira um card em "Novo" automaticamente, com nome do perfil,
   telefone, DDD/região e o **anúncio de origem** (a mensagem vinda de anúncio traz referência do
   anúncio: na API oficial `referral` com `source_id`, `headline`, `ctwa_clid`; no motor por QR o
   payload traz `externalAdReply` com título e URL do anúncio).
2. **Distribuição imediata**: o card nasce atribuído pelo rodízio e o vendedor recebe a conversa já
   aberta no módulo de chat, com o botão Ligar ao lado.
3. **Lead Ads continua no roadmap** (fase 2) para campanhas com formulário, mas deixa de ser
   pré-requisito do kanban.
4. **Importação da planilha** entra como migração única dos 540 leads atuais, com deduplicação por
   telefone e resultado inicial derivado da coluna Feedback (mapa de texto → resultado fechado).
5. **Consentimento**: a primeira mensagem espontânea da pessoa é a base do contato (registrar data,
   texto e anúncio de origem no card), atendendo TSE e LGPD; o opt-out em 48 h fica visível no chat.

## Contrato de entrada (para o backend/front)

Evento `lead.novo` com: `telefone` (E.164), `nome_perfil`, `canal` (whatsapp | lead_ads | importacao |
manual), `origem` { `plataforma`, `conta_anuncio`, `campanha`, `anuncio`, `ctwa_clid` }, `primeira_mensagem`
{ `texto`, `data` }, `regiao` (DDD), `consentimento` { `tipo`: "mensagem_espontanea" | "formulario" |
"importacao", `data`, `evidencia` }. Deduplicação por telefone; lead existente recebe a interação em vez
de novo card.

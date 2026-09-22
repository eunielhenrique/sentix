# Sentix — Prompt do front · FASE 4: Insights de IA, coaching e gamificação

## Contexto (leia antes de tudo)

A **Sentix** é uma plataforma brasileira de vendas por telefone e WhatsApp. Já existem: shell, login,
kit, discador global, painel de gestão, kanban com drawer e linha do tempo de interações, importação,
módulo de WhatsApp. Toda ligação (gravada e transcrita) e toda conversa de WhatsApp já viram uma
`Interacao`. Esta fase entrega o que nenhum concorrente brasileiro tem junto: **análise das interações
por uma rubrica única, página de coaching por vendedor e gamificação com pódio, medalhas e diamantes**,
tudo lendo a mesma base de interações.

Regras permanentes do projeto:
- **Marca própria.** Nada copiado de Gong, PipeRun, Koee, Spinify, Ambition ou qualquer concorrente.
- **Dado real ou estado vazio.** Sem backend de IA, o módulo roda contra `src/api/insights/localAdapter.ts`
  com selo "Dados de demonstração". A nota de IA nunca aparece sem a análise real por trás.
- **Nenhuma tela chama fetch direto.** Tudo via `InsightsAdapter`; o adaptador real apontará para o
  backend da Sentix (transcrição + modelo de linguagem). O front não chama provedores de IA.
- **Stack e kit:** React 18+ com Vite e TypeScript, React Router, Context + hooks, tokens em
  `tokens.css` (claro/escuro), kit próprio em `src/kit/`. Gráficos com uma única lib leve (Recharts
  ou similar), cores vindas dos tokens, acessíveis no claro e no escuro.
- **Padrões:** skeleton e estado vazio honesto; delta com sinal e cor pelo sinal; ícones do kit;
  Drawer e Modal na raiz; acessível por teclado.
- Uma feature por branch → PR com checklist, divergências e campos reais.

## 1. Modelo de dados (`src/api/insights/types.ts`)

```ts
type Criterio = 'abertura' | 'escuta' | 'objecoes' | 'clareza' | 'fechamento' | 'proximo_passo';
interface Analise { interacaoId: string; leadId: string; vendedorId: string | 'ia'; canal: 'ligacao' | 'whatsapp' | 'ia_voz';
  em: string; resumo: string; proximosPassos: string[]; objecoes: { tipo: string; trecho: string }[];
  rubrica: Record<Criterio, { nota: 1 | 2 | 3 | 4 | 5; evidencia: string }>; notaGeral: number /* média ponderada */;
  pontosFortes: string[]; pontosAMelhorar: string[]; sentimentoLead: 'positivo' | 'neutro' | 'negativo';
  modelo: string; custoEstimado?: number }
interface PlanoCoaching { vendedorId: string; semana: string /* ISO week */; evolucao: Record<Criterio, number[]> /* últimas 8 semanas */;
  fortes: { criterio: Criterio; texto: string; trecho: string; interacaoId: string }[];
  melhorar: { criterio: Criterio; texto: string; trecho: string; interacaoId: string; sugestao: string }[];
  meta: { criterio: Criterio; alvo: number; status: 'em_andamento' | 'atingida' | 'nao_atingida' } ;
  historicoMetas: { semana: string; criterio: Criterio; alvo: number; resultado: number }[] }
interface RegraPontos { id: string; evento: 'lead_engajado' | 'entrou_no_grupo' | 'apoiador_ativo' | 'primeiro_contato_5min'
  | 'retentativa_cumprida' | 'escuta_acima_4_semana' | 'nota_geral_acima_4' | 'conversa_respondida_10min'; pontos: number; ativo: boolean }
interface Medalha { id: string; nome: string; descricao: string; criterio: string /* texto humano */; icone: string; raridade: 'bronze' | 'prata' | 'ouro' }
interface Placar { periodo: 'semana' | 'mes'; escopo: 'geral' | string /* região */; posicoes: { vendedorId: string; pontos: number; diamantes: number;
  posicao: number; variacao: number | null; streakDias: number; medalhas: string[] }[]; atualizadoEm: string }
```

Interface `InsightsAdapter`: `obterAnalise(interacaoId)`, `listarAnalises(filtros, pagina)`,
`reanalisar(interacaoId)`, `obterPlano(vendedorId, semana?)`, `definirMeta(vendedorId, criterio, alvo)`,
`placar(periodo, escopo)`, `perfilGamificacao(vendedorId)`, `regras()`, `salvarRegras(r)`, `medalhas()`,
`painelGestor(periodo)`, `assinar('analise.pronta' | 'placar.atualizado', cb)`. O `local` gera análises
plausíveis a partir do texto das interações de demonstração, sempre com o selo.

## 2. Análise por interação (dentro do drawer do lead e da tela de relatórios, já existentes)

Na linha do tempo, cada interação analisada mostra a **nota geral** (badge 1–5 com cor pelo valor) e
um botão "Ver análise" que abre um **sub-drawer** (mesma largura do drawer de baixo) com:
- Resumo em 3 linhas e próximos passos (lista com botão "Agendar" que cria o próximo passo do lead).
- Rubrica: seis linhas (Abertura, Escuta, Objeções, Clareza da proposta, Fechamento, Próximo passo),
  nota de 1 a 5 em barra, e o **trecho da conversa como evidência** (clicável: rola a transcrição ou o
  chat até o ponto).
- Objeções detectadas (tipo + trecho). Sentimento do lead.
- Pontos fortes e pontos a melhorar (3 + 3, texto curto).
- Transcrição completa com marcação de quem fala (vendedor / lead) e busca.
- Botão "Reanalisar" (gestor). Rodapé: modelo usado e custo estimado, discretos.
Estado "Analisando…" com skeleton enquanto `analise.pronta` não chega; sem análise → "Sem análise
para esta interação" com o motivo (curta demais, sem áudio, sem transcrição).

## 3. Página de coaching do vendedor (`/coaching/:vendedorId`)

Vendedor vê a própria; gestor vê qualquer uma e um seletor no topo.
- Cabeçalho: avatar, nome, equipe, nota geral média da semana com delta, número de interações analisadas.
- **Evolução por critério**: seis mini-gráficos de linha (8 semanas) num grid de 3 por linha, cada um
  com a nota atual, delta e a meta (linha tracejada) quando definida.
- **Pontos fortes** (3 cards): critério, texto, trecho real e link para a interação.
- **A melhorar** (3 cards): critério, texto, trecho real, **sugestão prática** e botão "Definir como
  meta da semana".
- **Meta da semana**: critério, alvo, progresso (barra), status. Histórico de metas em tabela.
- Objeções mais frequentes deste vendedor no período (barras horizontais) com exemplo de resposta
  boa retirada das melhores interações da equipe.

## 4. Painel do gestor (`/coaching`)

Filtros: período, equipe, região, canal. Cartões: nota geral média da equipe, interações analisadas,
% acima de 4, objeção mais frequente. **Mapa de calor vendedor × critério** (notas médias, cor por
faixa). Ranking por critério (quem é melhor em fechamento, quem precisa de escuta). Objeções mais
frequentes da semana com tendência. Lista de "melhores trechos da semana" para compartilhar com a
equipe (botão copia o trecho e o contexto).

## 5. Gamificação

### 5.1 Placar (`/placar`)
Seletor de período (**semana** / **mês**) e escopo (**geral** / por **região**), pill de canal opcional.
**Pódio** com 1–3 vendedores (1º ao centro e maior; com 1–2 pessoas o pódio ainda aparece, célula
vazia vira espaçador), avatar, nome, pontos, diamantes, medalhas recentes. Abaixo, **ranking completo**
com posição, variação vs. período anterior (ícone up/down com cor; novo no ranking sem badge),
streak de dias consecutivos com atividade, pontos, diamantes, medalhas (ícones com tooltip). Scroll
infinito. Clique abre o **perfil de gamificação**.
Regra fixa no rodapé em texto curto: "Pontos por resultado real e por comportamento; nota da IA
pesa menos que resultado". Nunca pontuar por volume de discagem.

### 5.2 Perfil de gamificação (`/placar/:vendedorId`)
Vitrine: pontos da temporada, diamantes (moeda da temporada), nível, streak, medalhas conquistadas
(com data e critério) e a conquistar (cinza com o que falta), histórico de pontos por evento (tabela:
data, evento, pontos, lead relacionado). Compartilhar conquista (gera texto para WhatsApp com o
conteúdo real).

### 5.3 Regras (`/configuracoes/gamificacao`, só gestor)
Tabela editável de `RegraPontos` (evento, pontos, ativo), com exemplos e a soma máxima por dia por
vendedor (anti-abuso). Catálogo de medalhas com critério em texto, raridade e ícone do kit. Duração
da temporada (mensal padrão) e o que acontece no fim (diamantes zeram, medalhas ficam). Prévia:
"Na semana passada, com estas regras, o pódio seria: …".

### 5.4 Notificações
Toast no shell ao ganhar pontos/medalha/subir de posição, com som opcional. Resumo semanal na
segunda-feira (card no dashboard): posição, variação, meta da semana.

## 6. Integração com o que já existe

- Dashboard e relatórios ganham colunas: nota média da IA, pontos da semana, medalhas.
- Card do kanban mostra a nota geral da última interação (badge pequeno) quando existir.
- Módulo de WhatsApp: conversa analisada mostra a nota no cabeçalho; "Ver análise" abre o mesmo sub-drawer.
- Conversas e ligações usam a **mesma rubrica e o mesmo placar**; o canal é só um filtro.

## 7. Critérios de aceite (checklist do PR)

- [ ] Sub-drawer de análise com rubrica, evidências clicáveis, objeções, transcrição e estados de espera/vazio.
- [ ] Página de coaching com evolução por critério (8 semanas), fortes, a melhorar com sugestão, meta e histórico.
- [ ] Painel do gestor com mapa de calor vendedor × critério, rankings por critério e objeções.
- [ ] Placar com pódio (1–3), ranking com variação e streak, filtros de período/escopo/canal.
- [ ] Perfil de gamificação com medalhas conquistadas/a conquistar e histórico de pontos.
- [ ] Regras editáveis com anti-abuso e prévia; temporada configurável.
- [ ] Notas e pontos aparecendo no dashboard, relatórios, kanban e WhatsApp.
- [ ] Gráficos legíveis em tema claro e escuro; nada de emoji como indicador.
- [ ] Selo "Dados de demonstração" onde o adaptador for `local`; README com o contrato do `InsightsAdapter`
      (inclusive o formato exato da rubrica) para o backend implementar.

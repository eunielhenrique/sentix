# Sentix — Prompt do front · FASE 3: Módulo de conversação WhatsApp

## Contexto (leia antes de tudo)

A **Sentix** é uma plataforma brasileira de vendas por telefone e WhatsApp. Já existem: shell, login,
kit, discador global (`openDialer`), painel de gestão, kanban de leads com drawer, importação,
conexão de WhatsApp por QR e criação automática de card em conversa nova. Esta fase entrega o
**módulo de conversação**: a experiência do WhatsApp Web dentro da Sentix, com funções a mais, ligado
ao kanban e ao discador. O vendedor usa o **próprio número**, conectado por QR (protocolo do WhatsApp
Web via motor self-hosted, Evolution API como referência); a API oficial da Meta fica prevista como
opção por organização, com o mesmo módulo de chat.

Regras permanentes do projeto:
- **Marca própria.** Proibido copiar layout, textos, ícones ou cores do WhatsApp, API4COM, Kommo,
  Digisac, Umbler, Huggy ou qualquer concorrente. A estrutura em duas colunas é convenção; o desenho é nosso.
- **Dado real ou estado vazio.** Sem backend/motor, o módulo roda contra `src/api/whatsapp/localAdapter.ts`
  (IndexedDB) com selo "Dados de demonstração" no cabeçalho. Mock nunca se apresenta como real.
- **O front nunca fala com o motor de WhatsApp direto.** Sempre via `WhatsappAdapter`; o adaptador
  real apontará para o backend da Sentix, que fala com o motor.
- **Stack e kit:** React 18+ com Vite e TypeScript, React Router, Context + hooks, tokens em
  `tokens.css` (claro/escuro), kit próprio em `src/kit/`.
- **Padrões:** skeleton e estado vazio honesto; ícones do kit (emoji só dentro de mensagens); Drawer
  e Modal na raiz; scroll infinito; erro humano; acessível por teclado.
- **Segurança:** token só em memória/`sessionStorage`; mídia servida por URL assinada do adaptador;
  nada de credencial no repositório.
- Uma feature por branch → PR com checklist, divergências e campos reais.

## 1. Modelo de dados (`src/api/whatsapp/types.ts`)

```ts
type EstadoConexao = 'desconectado' | 'aguardando_leitura' | 'conectado' | 'reconectando';
interface Conexao { vendedorId: string; numero?: string; estado: EstadoConexao; desde?: string;
  saude: { mensagensNovasHoje: number; limiteDiario: number; taxaResposta: number; bloqueios7d: number; desconexoes7d: number } }
interface Conversa { id: string; vendedorId: string; leadId?: string; contato: { telefone: string; nome?: string; fotoUrl?: string };
  ultimaMensagem: { texto: string; em: string; de: 'lead' | 'vendedor' | 'ia' | 'sistema' };
  naoLidas: number; aguardando: 'lead' | 'vendedor' | 'ninguem'; etiquetas: string[]; etapaKanban?: string;
  primeiraRespostaSeg?: number; arquivada: boolean; fixada: boolean }
interface Mensagem { id: string; conversaId: string; de: 'lead' | 'vendedor' | 'ia' | 'sistema'; autorId?: string;
  tipo: 'texto' | 'audio' | 'imagem' | 'video' | 'documento' | 'figurinha' | 'localizacao' | 'contato';
  texto?: string; midiaUrl?: string; transcricao?: string; status: 'enviando' | 'enviada' | 'entregue' | 'lida' | 'falhou';
  em: string; respondeA?: string; agendadaPara?: string; referenciaAnuncio?: { campanha?: string; anuncio?: string; ctwaClid?: string } }
interface RespostaRapida { id: string; atalho: string; titulo: string; texto: string; midiaUrl?: string; escopo: 'org' | 'pessoal' }
```

Interface `WhatsappAdapter`: `obterQr(vendedorId)`, `estado(vendedorId)`, `desconectar(vendedorId)`,
`listarConversas(filtros, pagina)`, `obterConversa(id)`, `listarMensagens(conversaId, antesDe?)`,
`enviar(conversaId, { texto | midia, respondeA?, agendadaPara? })`, `marcarLida(conversaId)`,
`transferir(conversaId, paraVendedorId, nota?)`, `etiquetar(conversaId, etiquetas)`,
`listarRespostasRapidas()`, `salvarRespostaRapida(r)`, `materiais()`, `sugerirResposta(conversaId)`,
`otimizarTexto(conversaId, rascunho)`, `assinar(evento, cb)` para `mensagem.nova`, `status.mensagem`,
`conexao.mudou`, `conversa.nova`. O `local` simula recebimento com atraso e um painel dev "Simular mensagem".

## 2. Tela do módulo (`/conversas`)

Layout em duas colunas no desktop (lista 360 px + conversa), uma coluna com navegação empilhada no
mobile. Cabeçalho do módulo com **estado da conexão** do vendedor (badge com cor, número conectado,
botão Reconectar) e o selo de demonstração quando aplicável.

### 2.1 Lista de conversas (esquerda)
Busca por nome/telefone/texto; filtros em pills: **Não respondidas**, **Aguardando lead**, **Minhas**,
por **etapa do kanban**, por **etiqueta**; ordenação por última mensagem. Item: avatar (foto ou
iniciais), nome ou telefone, prévia da última mensagem com ícone do tipo, hora, contador de não lidas,
etiquetas (chips pequenos), badge da etapa do kanban, ícone de "aguardando lead"/"aguardando você".
Fixar e arquivar por menu de contexto. Scroll infinito.

### 2.2 Conversa (direita)
Cabeçalho: contato, telefone, etapa do kanban (badge clicável → abre o **drawer do lead** já existente,
na raiz da tela), botões **Ligar** (`openDialer`), **Registrar resultado** (mesmo modal do kanban),
**Transferir**, **Etiquetas**, menu (arquivar, exportar conversa).
Corpo: mensagens em balões (lead à esquerda, vendedor/IA à direita, sistema centralizado), separador
de data, status de entrega (ícones do kit: enviando, enviada, entregue, lida, falhou com "tentar
novamente"), mídia com visualização inline (imagem, vídeo, documento com nome/tamanho), **áudio com
player e transcrição** abaixo (quando o adaptador entregar), resposta citada, mensagem vinda de
anúncio mostra o cartão do anúncio de origem. Scroll infinito para cima com âncora.
Compositor: textarea com autoexpansão, **respostas rápidas por "/"** (autocomplete), anexar (imagem,
documento, áudio gravado no navegador), **Enviar material** (lista dos materiais da campanha em um
clique), **agendar envio** (data/hora; aparece como pendente com opção de cancelar), emoji picker,
e **dois botões de IA, nunca um só**:
- **Sugerir resposta** → escreve do zero a partir da conversa (`sugerirResposta`). Estado "Gerando…".
- **Otimizar meu texto** → refina o rascunho mantendo a intenção (`otimizarTexto`). Desabilitado com
  a caixa vazia. Estado "Otimizando…".
Atalhos: Enter envia, Shift+Enter quebra linha, Ctrl/Cmd+K busca conversa.

### 2.3 Transferência de conversa
Modal: vendedor de destino, nota interna, opção "avisar o lead". A conversa some da lista de origem,
aparece na do destino com o histórico inteiro e uma mensagem de sistema registrando a transferência;
grava movimento no lead.

### 2.4 Etiquetas e respostas rápidas
Etiquetas por organização (cor + nome) geridas em `/configuracoes/etiquetas`. Respostas rápidas em
`/configuracoes/respostas-rapidas` com escopo organização/pessoal, atalho, título, texto com variáveis
(`{{nome}}`, `{{cidade}}`, `{{vendedor}}`) e mídia opcional. Materiais da campanha em
`/configuracoes/materiais` (nome, arquivo/link, descrição).

## 3. Painel de saúde do número (`/conversas/saude`, vendedor vê o seu; gestor vê todos)

Mini-cards: mensagens novas hoje / limite diário (barra), taxa de resposta 7 dias, bloqueios 7 dias,
desconexões 7 dias, tempo médio de primeira resposta. Regras (gestor): limite diário de contatos
novos por número, intervalo mínimo aleatório entre envios em sequência, aviso ao atingir 80 % do
limite, bloqueio de envio ao atingir 100 % com mensagem clara. Histórico de conexão (linha do tempo).
Aviso fixo e discreto: "Número pessoal conectado por QR está sujeito às regras da Meta; siga os limites".

## 4. Consentimento e opt-out

No drawer do lead e no cabeçalho da conversa: origem do consentimento (primeira mensagem espontânea
com data, ou formulário). Comando de opt-out: se o lead escrever "sair", "parar" ou similar, o sistema
marca `optOut` no lead, bloqueia envios (exceto confirmação) e mostra aviso na conversa. Gestor
configura as palavras-chave e o texto de confirmação em `/configuracoes/consentimento`.

## 5. Visão do gestor (`/conversas/equipe`)

Tabela por vendedor: conversas abertas, não respondidas, tempo médio de primeira resposta, mensagens
enviadas/recebidas no período, estado da conexão, saúde do número. Clique abre a lista de conversas
daquele vendedor em modo leitura, com opção de transferir. Alertas: conversa sem resposta há mais de
N minutos (configurável) aparece no topo com botão "Cutucar vendedor" (notificação no shell).

## 6. Integração com kanban e discador (já existem)

- Conversa nova de número desconhecido → card em Novo (já feito na fase 2); conversa de número
  existente → interação no lead, sem card novo.
- Toda mensagem vira `Interacao` tipo `whatsapp` na linha do tempo do drawer.
- Resultado registrado na conversa move o card pelas regras de adjacência.
- **Ligar** no cabeçalho abre o discador com número, nome e leadId.

## 7. Critérios de aceite (checklist do PR)

- [ ] Lista e conversa com todos os elementos; filtros e busca; scroll infinito nos dois painéis.
- [ ] Envio de texto, mídia e áudio gravado; status de entrega; falha com tentar novamente.
- [ ] Áudio com player e transcrição quando o adaptador entregar; mensagem de anúncio com cartão de origem.
- [ ] Respostas rápidas por "/", enviar material, agendar envio, dois botões de IA com estados distintos.
- [ ] Transferência com histórico, nota e mensagem de sistema; etiquetas; fixar/arquivar.
- [ ] Painel de saúde com limites, aviso a 80 % e bloqueio a 100 %.
- [ ] Opt-out por palavra-chave bloqueando envios; consentimento visível.
- [ ] Visão do gestor com tabela, alertas e transferência.
- [ ] Vínculo com o drawer do lead e com o discador; mensagens na linha do tempo.
- [ ] Selo "Dados de demonstração" onde o adaptador for `local`; README com o contrato do `WhatsappAdapter`
      e dos eventos, para o backend implementar sobre o motor.

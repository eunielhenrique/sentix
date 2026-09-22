# Sentix — Telas de gestão (painel administrativo), a partir do portal da API4COM em 22/09/2026

Referência funcional: portal da API4COM (Dashboard, Relatórios, Assinatura, Usuários, Integrações).
A Sentix replica a FUNÇÃO com layout, textos e ícones próprios. Na fase 1, o dado de telefonia vem
da API4COM pelo adaptador de voz; depois, do SIPPulse próprio. Dados de WhatsApp, kanban e IA vêm
do backend da Sentix e entram nas mesmas telas.

## 1. Dashboard (visão geral da operação)

Filtros no topo: usuários (multi), período (hoje / 7d / 30d / intervalo), sentido (recebidas,
efetuadas, ambas), status da chamada. Botão Atualizar com hora da última atualização.

Cartões (mini-cards padrão, com delta vs. período anterior):
- Total de chamadas · taxa de atendimento
- Chamadas atendidas · tempo falado total
- Total de ramais ativos · tempo médio de atendimento
- **Sentix acrescenta:** leads novos no período · tempo médio até o 1º contato · conversas de WhatsApp
  · leads engajados (do kanban)

Tabela "Desempenho por usuário" (ordenável, exportável em CSV/HTML): usuário · taxa de atendimento ·
total de chamadas · canceladas · espera antes de desligar (média) · rediscagens · taxa de atendimento
em rediscagens · chamadas significativas (> 30 s) · a cada 100 ligações (quantas significativas).
**Sentix acrescenta:** leads atendidos · engajados · nota média da IA · pontos da semana.

Gráficos: chamadas por usuário ao longo do tempo (agrupar por hora/dia; linha ou barras) e
distribuição por status de chamada (rosca). Skeleton no carregamento; sem dado → estado vazio.

## 2. Relatórios

Seletor de tipo: **Chamadas** | **Usuários** (| **Conversas** e **Leads**, adicionados pela Sentix).
Filtros em pills: período (padrão últimos 30 dias) · tipo de chamada (recebida/efetuada/interna) ·
usuários · número discado · motivo do desligamento · duração (mín/máx). Filtros ativos aparecem como
chips removíveis. Botão de exportar (CSV).

Tabela de chamadas (colunas ordenáveis, scroll infinito): data/hora · usuário · número discado
(mascarado no padrão brasileiro) · duração · motivo do desligamento (Atendida, Caixa postal,
Cancelada, Não foi possível completar, Ocupado, Não atendida) · tipo (sainte/entrante) · ramal ·
finalizou às · tarifa (R$/min) · custo da ligação · metadados (abre drawer com o payload) · gravação
(abre player inline + link) · **Sentix acrescenta:** lead vinculado (abre o drawer do kanban),
resultado registrado, nota da IA, transcrição.

Relatório de usuários: por usuário, totais do período (chamadas, atendidas, minutos, custo, leads,
conversas, resultados).

## 3. Assinatura e uso (planos por usuário)

Tela de revisão de assinatura: explicação de como funciona (um plano por usuário, escolha pelo perfil
de uso, valor fixo por mês), seletor de mês de referência, tabela usuário · consumo em minutos no
mês · plano (select) · mensalidade, com "Aplicar a todos", e resumo da cobrança à direita (plano ×
quantidade, total/mês, vencimento, próximas cobranças, botão de pagamento).

Na Sentix, enquanto a operadora for a API4COM, essa tela mostra o **consumo por usuário** (minutos e
custo real do período, lidos do relatório de chamadas) e uma **sugestão de plano** calculada
localmente (ver §6), sem executar cobrança. Quando existir cobrança própria, vira a tela de planos
da Sentix (Conversas / Completo / Pro) com o mesmo formato.

## 4. Usuários

Cartão com total de usuários ativos. Busca por nome/e-mail, filtro por status (Ativo, Desativado,
Convidado), botão "Convidar novo usuário" (nome, e-mail, papel, equipe/região, ramal a vincular).
Tabela: usuário (nome + e-mail, ícone de admin) · ramal · equipe · papel · status · WhatsApp
conectado (sim/não) · ações (editar, desativar/reativar, reatribuir ramal, reenviar convite).
Regra: um ramal por usuário ativo; usuário desativado libera o ramal (evita o caso atual de dois
ramais para a mesma pessoa).

## 5. Integrações

Abas: **CRM** (cards com nome, status Ativo/Inativo, toggle, engrenagem para configurar, link de
ajuda) · **Ramal** (configuração por ramal: BINA, gravação, webhook de CDR por ramal) · **Webhook**
(URL, versão, tipos de evento: fim de chamada; testar envio; histórico de entregas).
Sentix acrescenta as abas **Meta** (contas de anúncio, páginas, formulários de Lead Ads, número de
WhatsApp da campanha) · **WhatsApp** (motor por QR ou API oficial, por vendedor) · **Operadora**
(API4COM/SIPPulse: credenciais, domínio, saldo) · **IA** (modelos, rubrica, limites de custo) ·
**Agente de voz** (Retell).
CRMs: como a Sentix substitui o CRM, a lista começa vazia e integrações entram sob demanda
(Pipedrive, HubSpot, RD Station, Kommo primeiro, se algum cliente pedir).

## 6. Dados lidos da conta Snow Print que alimentam a fase 1

- **Tarifa vigente: R$ 0,41 por minuto para celular**, cobrada por **minuto iniciado** (3:13 → 4 min →
  R$ 1,64; 1:31 → 2 min → R$ 0,82; 0:10 → 1 min → R$ 0,41). Caixa postal, cancelada e não completada
  não geram custo. Fixo não apareceu no relatório ainda.
- Ponto de equilíbrio do Ilimitado (R$ 209,90): **~512 minutos/mês por usuário**. Abaixo disso, o
  pré-pago sai mais barato; Negociação (300 min por R$ 169,90) só compensa acima de ~414 min.
- Usuários: 10 ativos e 2 desativados (duplicados). Consumo de agosto = 0 para todos; setembro é o
  primeiro mês de uso real.
- Motivos de desligamento observados: Atendida, Caixa postal, Cancelada, Não foi possível completar.
- Colunas do relatório = contrato de campos para o adaptador de voz: usuário, número, duração,
  motivo, tipo, ramal, início, fim, tarifa, custo, metadados, URL da gravação.

## 7. Tokens de acesso (API)

Tabela paginada (10/25/50 por página, busca): token (mostrado inteiro só na criação; depois
mascarado com botão copiar) · criado em · expira em · ações (remover). Botão "Novo token de acesso"
abre modal com nome do token, validade (7/14/30 dias ou sem expiração) e escopo (leitura /
leitura+escrita). Na API4COM o token dura 14 dias por padrão. Sentix acrescenta "último uso" e
revogação de todos os tokens de um usuário desativado.

## 8. Recarga e créditos (enquanto o modelo for pré-pago)

Modal "Adicionar recarga": valor (mínimo R$ 250, máximo R$ 50.000) com **régua de desconto por
faixa** (0% · 5% · 15% · 30% · 45% · 65%), que recalcula na hora o preço do minuto móvel e fixo;
confirmação de até 5 e-mails do financeiro; prazos de compensação por meio de pagamento (cartão
instantâneo, PIX até 24 h, boleto até 3 dias); botões Cancelar, Gerar pagamento e link para os planos.
**Tarifa base da conta Snow Print: móvel R$ 0,41/min e fixo R$ 0,09/min** (0% de desconto).
Na Sentix esta tela lê o saldo e as tarifas da operadora pelo adaptador e, quando existir cobrança
própria, vira a tela de créditos da Sentix (mesma régua, faixas próprias).

## 9. Menu da conta (canto superior direito)

Cabeçalho com nome, organização e papel. Itens:
- **Meus dados** (nome, e-mail, telefone, foto, fuso, idioma, dispositivos de áudio padrão)
- **Alterar senha**
- **Solicitar personificação** (suporte entra como o cliente com aprovação e registro de auditoria;
  na Sentix é "Acesso do suporte": o cliente autoriza por tempo limitado e vê o histórico)
- Financeiro: **Histórico de cobranças** (tabela: data, descrição, valor, método, status, nota fiscal,
  link de pagamento) · **Recarga automática** (gatilho por saldo mínimo, valor, cartão, status) ·
  **Dados financeiros** (razão social, CNPJ/CPF, endereço, e-mails de cobrança)
- **Dados da organização** (nome, domínio de voz, telefone, logo, horário de funcionamento, política
  de gravação e texto de aviso LGPD)
- **Sair**

Também no topo: saldo disponível com botão de recarga, e a indicação "Indique e ganhe" (programa de
indicação com crédito), que a Sentix pode replicar como programa próprio mais tarde.

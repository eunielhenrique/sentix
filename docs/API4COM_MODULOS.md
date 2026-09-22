# API4COM — módulos e catálogo lidos pela API (22/09/2026)

Fonte: `GET /accounts`, `/users`, `/subscriptions`, `/organization_integrations`, `/charges`,
`/rollout?featureFlag=*`, `/terms/me`, `/about` em `api.api4com.com/api/v1` e
`GET /pricing/offers` em `billing-service.api4com.com` (chave pública embutida no portal).
Versões: API 1.77.0 · portal 2.54.64 · extensão 5.10.0.

## Catálogo de planos (Tabela de Preços set/2026, vigente desde 04/09/2026, por usuário/mês)

| Plano | Preço | Recursos | Indicado para |
|---|---|---|---|
| Gerencial | sem valor (grátis) | Não realiza ligações · Acesso básico | Gestores / administradores |
| Suporte | R$ 49,90 | 90 min · BINA dinâmica · Classificador de caixa postal | Recepção / CS passivo |
| Negociação | R$ 169,90 | 300 min · BINA · Classificador · Resumo gerencial com IA · Análise qualitativa com IA | Closers / pré-vendas |
| Ilimitado | R$ 209,90 | Minutos ilimitados · BINA · Classificador · Resumo · Análise qualitativa · Dashboard de IA | SDRs / hunters |
| Gerencial + IA4COM | R$ 129,90 | Gerencial + IA4COM | Gestores |
| Negociação + IA4COM | R$ 299,80 | Negociação + IA4COM | Closers |
| Ilimitado + IA4COM | R$ 339,80 | Ilimitado + IA4COM | SDRs |

IA4COM é um adicional de R$ 129,90 por usuário, "liberado no portal após o pagamento da cobrança".
Modelo de cobrança: por usuário (`PER_USER`), ciclo mensal, limite de minutos por plano.

## Módulos/recursos que a plataforma vende (unidades do catálogo)

- Minutos de ligação (90 / 300 / ilimitado)
- BINA dinâmica (número de saída conforme o destino)
- Classificador de caixa postal
- Resumo gerencial com IA
- Análise qualitativa com IA
- Dashboard de IA
- IA4COM (assistente SPIN para o vendedor)

## Módulos do portal (rotas) e flags de liberação gradual

Rotas: dashboard, webphone, relatório de chamadas, usuários (lista/convite), tokens de acesso,
integrações (gerenciador), assinatura, preços, recarga (manual e automática), histórico de cobranças,
dados financeiros, perfil da organização, assistente (IA4COM), impersonação de suporte, onboarding.

Feature flags consultadas pelo portal: `ia4com`, `enable-ai-dropdown` (escolha do modelo GPT/Claude/
Gemini), `copy-recordings` (cópia das gravações para bucket próprio), `google-data-studio`,
`gohighlevel-integration`, `vendfly-integration`, `extension-change`, `recharge-due-date`,
`account-impersonation`. **Na conta Snow Print todas retornam DENIED.**

## Estado da conta Snow Print (organização 17820)

- Domínio SIP `snowprint.api4com.com`, criada em 18/09/2026, migrada para o modelo novo de planos
  (`isRatePlanNew: true`, `isUnlimited: false`, `blockByPlan: true`, `isUserLimitExempt: true`).
- **Nenhuma assinatura ativa** (`/subscriptions` vazio) e nenhum usuário com plano (`planCode: null`).
  A conta opera por crédito pré-pago: recarga manual de R$ 1.250 via PIX paga em 21/09/2026
  (nota fiscal emitida via Asaas/Omie); saldo atual R$ 1.138,56.
- Integração organizacional `softswitch` com `hasDynamicTariff: true` e bônus de crédito recebido.
- 12 usuários em 12 ramais (1000 a 1011): 4 ADMIN e 8 USER; dois nomes repetidos em ramais
  diferentes (Salete Cassiano 1005/1006, Maria Eduarda Gomes 1007/1008).
- Termos do IA4COM (v2) pendentes de aceite; recarga automática não configurada.
- Financeiro: CNPJ 50.975.327/0001-57, Santana de Parnaíba/SP, pessoa jurídica.

## Leitura para a Sentix

- O que a API4COM vende como módulo de IA (resumo, análise qualitativa, dashboard, IA4COM) é
  exatamente o que a Sentix entrega dentro do assento, a custo de centavos por chamada.
- Classificador de caixa postal e BINA dinâmica são entitlements pagos lá; na Sentix entram no
  discador (itens 5 e 6 do benchmark).
- A conta hoje não tem plano: os 12 ramais consomem crédito por minuto com tarifa dinâmica. Vale
  confirmar a tarifa por minuto vigente antes de decidir se compensa migrar ramais para Ilimitado
  enquanto a Sentix usa a API4COM como operadora.

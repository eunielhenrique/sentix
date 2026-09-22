# Esquema de classificação de chamadas (v1, campanha)

Cada transcrição gera um JSON com este formato. A IA (sessão ou API) preenche só a partir do que
está na transcrição; sem evidência → `null`. Idioma: pt-BR.

```json
{
  "id": "<id da chamada>",
  "telefone": "<to>",
  "vendedor": "<first_name>",
  "duracao_s": 0,
  "tipo_chamada": "conversa | caixa_postal | engano_ou_terceiro | sem_audio_util | secretaria_eletronica",
  "falou_com_lead": true,
  "classificacao_lead": "apoiador_ativo | engajado | recebeu_material | neutro | pede_ajuda_ou_beneficio | recusou | nao_e_o_contato | retornar_depois | invalido",
  "interesse": 0,
  "sentimento_lead": "positivo | neutro | negativo",
  "aceitou_grupo": true,
  "recebeu_material": true,
  "vai_divulgar": true,
  "pediu": ["material fisico", "ajuda financeira", "emprego", "falar com o candidato"],
  "objecoes": [{"tipo": "desconfianca | nao_gosta_de_politica | apoia_outro | sem_tempo | nao_conhece", "trecho": "..."}],
  "cidade_mencionada": "…",
  "familia_votos_estimados": 0,
  "proximo_passo": "enviar_material | adicionar_grupo | ligar_novamente | enviar_link_video | nada | escalar_para_coordenador",
  "resumo": "2 a 3 frases",
  "rubrica_vendedor": {
    "abertura": {"nota": 1, "evidencia": "…"},
    "escuta": {"nota": 1, "evidencia": "…"},
    "objecoes": {"nota": 1, "evidencia": "…"},
    "clareza": {"nota": 1, "evidencia": "…"},
    "fechamento": {"nota": 1, "evidencia": "…"},
    "proximo_passo": {"nota": 1, "evidencia": "…"}
  },
  "pontos_fortes": ["…"],
  "pontos_a_melhorar": ["…"],
  "alertas": ["promessa indevida", "pedido de dinheiro", "dado sensivel", "tom inadequado"]
}
```

Regras:
- `interesse` de 0 (nenhum) a 5 (quer atuar como cabo eleitoral / já mobiliza família).
- `classificacao_lead` segue os desfechos fechados do kanban da Sentix; `retornar_depois` quando a
  pessoa pediu para ligar em outro horário; `nao_e_o_contato` quando atendeu terceiro.
- Rubrica só quando `falou_com_lead = true` e a chamada tem mais de 30 s; senão `null`.
- Consolidação por telefone: última chamada com conversa define a classificação; tentativas sem
  conversa somam no contador. Um telefone pode ter várias chamadas.
- Alertas são para o coordenador ler: a IA nunca decide sozinha sobre eles.

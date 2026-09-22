# Pipeline de gravações → transcrição → classificação por IA

Quatro passos idempotentes, pensados para rodar a cada hora (cron) ou sob demanda.

```
API4COM_TOKEN=... python3 fetch_calls.py  work/            # 1. chamadas + gravações novas
python3 transcribe.py work/audio work/transcripts          # 2. Whisper local (large-v3-turbo, CPU)
ANTHROPIC_API_KEY=... python3 classify.py work/            # 3. IA classifica (ou GEMINI_API_KEY)
python3 consolidate.py work/                               # 4. CSVs por telefone/vendedor + RELATORIO.md
```

`run.sh` executa os quatro em sequência com lock, para agendar em cron:
`0 * * * * /caminho/sentix/pipeline/run.sh /caminho/work >> /var/log/sentix-pipeline.log 2>&1`

## Requisitos
- Python 3.10+, `pip install faster-whisper` (baixa o modelo na primeira execução, ~1,6 GB).
- CPU com 4 núcleos transcreve ~5,5 min de áudio por minuto com `large-v3-turbo` int8.
- Token da API4COM (14 dias; gere um sem expiração em Tokens de acesso para o cron).
- Chave de IA para o passo 3: Anthropic (`claude-sonnet-5` padrão) ou Gemini (`gemini-2.5-flash`).

## Custos observados (22/09/2026)
- 299 gravações / 431 min de áudio: transcrição local sem custo; classificação ≈ US$ 0,01–0,03 por
  chamada com Sonnet 5 (≈ US$ 3–9 o lote), ≈ US$ 0,001 com Gemini Flash.

## Segurança
- As URLs de gravação da API4COM (`listener.api4com.com/files/listen/<uuid>.mp3`) abrem **sem
  autenticação**. Não compartilhe links; a Sentix deve copiar os áudios para storage próprio com
  URL assinada e retenção definida (LGPD).
- Nada de token no repositório: só por variável de ambiente.

## Saídas
- `work/transcripts/<id>.json` — texto e segmentos com tempo.
- `work/analises/<id>.json` — classificação no formato de `CLASSIFICACAO.md`.
- `work/leads_classificados.csv` — um telefone por linha, com classificação, interesse, próximo passo.
- `work/vendedores.csv` — rubrica média por vendedor, taxa de engajamento, pontos fortes/a melhorar.
- `work/RELATORIO.md` — resumo executivo do lote.

## Automático de verdade (próximo passo)
Trocar o cron pelo **webhook `channel-hangup`** da API4COM (Integrações → Webhook) apontando para o
backend da Sentix: cada chamada encerrada dispara download, transcrição e classificação em minutos,
e o resultado entra no card do lead e no placar.

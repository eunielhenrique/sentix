# Sentix — Concorrência real e análise de reuniões (22/09/2026)

## Concorrência: quem disputa cada módulo

| Módulo da Sentix | Quem já vende isso no Brasil | Força deles | O que não têm |
|---|---|---|---|
| WhatsApp + kanban | Kommo (100k+ clientes, US$ 20–45/usuário), Umbler Talk (R$ 99,90–219,90), Digisac, Huggy, ChatGuru, Meets (R$ 89), BotConversa, Whaticket | base instalada, marca, integrações | telefonia própria, coaching, gamificação; Kommo tirou o QR em 2026 |
| Telefonia + discador | API4COM (R$ 49,90–339,80), Nvoip (R$ 79–109), Callix (R$ 199), Directcall, Zenvia Voice | operadora e rotas próprias | kanban, WhatsApp, gamificação; API4COM é 11–50 pessoas |
| Análise de ligações por IA | PipeRun (SPIN/BANT), Exact Spotter, Meetime, IA4COM (R$ 129,90) | rubrica de vendas, base B2B | WhatsApp na mesma régua, gamificação |
| Análise de WhatsApp por IA | Koee (R$ 197/5 agentes) | barato, focado | ligação, kanban, telefonia |
| Gamificação | Gamefic (~R$ 50), Funifier; globais Spinify/Ambition | mecânicas prontas | dado de conversa; são "por cima" do CRM |
| Agente de voz IA | VulcaNet (R$ 499+), Toolzz (R$ 899+), Zenvia; globais Retell/Vapi/ElevenLabs | voz e roteiro | kanban e coaching integrados |

**Leitura:** a concorrência é grande por módulo e inexistente no conjunto. O risco real são dois
movimentos: a **Kommo** adicionar gamificação e telefonia (tem escala para isso) e a **API4COM**
adicionar kanban (tem a voz). A defesa da Sentix é velocidade, o canal da agência, coaching em
português com uma régua só para voz e texto, e preço em reais sem setup. Os quatro concorrentes que
importam de verdade para a venda: Kommo, Umbler Talk, API4COM e PipeRun.

## Transcrição de vídeo/reunião e análise do texto

Sim, é o mesmo pipeline das ligações: extrai o áudio, transcreve com identificação de quem fala,
aplica a rubrica de seis critérios e grava como `Interacao` do tipo `reuniao` no lead. Vídeo enviado
(upload ou link) entra pelo mesmo caminho.

## Conectar a IA da Sentix ao Google Meet e outras plataformas

Dois caminhos verificados em 22/09/2026:

1. **Bot de reunião (Recall.ai)** — entra na chamada como participante e devolve gravação e
   transcrição por API. Suporta Google Meet, Zoom, Microsoft Teams, Webex, GoTo Meeting e Slack
   Huddles. Preço: **US$ 0,50 por hora de gravação + US$ 0,15/h de transcrição**, cobrado por segundo,
   sem mínimo, 5 h grátis; armazenamento US$ 0,05/h após 7 dias; programa para startups a US$ 0,25/h.
   Uma reunião de 45 min custa ~US$ 0,49 (~R$ 2,60) + análise da IA (centavos). É o caminho
   **multiplataforma** e o mais rápido: a Sentix cria o bot pelo link da reunião ou pela agenda.
2. **API nativa do Google Meet** — o recurso `conferenceRecords.transcripts` entrega a transcrição
   gerada pelo próprio Meet (estados STARTED → ENDED → FILE_GENERATED, arquivo no Drive do
   organizador). Exige Google Workspace **Business Standard ou superior** (ou Individual), o
   organizador precisa ativar a transcrição, e **português está entre os 8 idiomas suportados**. Sem
   custo por minuto além da licença Workspace. Só Google Meet.

**Recomendação:** Recall.ai como padrão (funciona em qualquer plataforma e não depende do plano do
cliente) e Meet nativo como opção gratuita para quem já tem Workspace Business. Nos dois casos a
Sentix avisa os participantes que a reunião está sendo gravada e analisada (LGPD), registra o
consentimento no lead e aplica a mesma rubrica e o mesmo placar. Entra como **fase 4.1**, logo após
insights e coaching, porque reaproveita tudo.

# Sentix — Kanban de leads (especificação, decisões do Euniel em 22/09/2026)

## Colunas (etapas)

Ordem fixa. Um lead está sempre em exatamente uma coluna.

1. **Novo** — chegou (Meta, importação ou manual), ainda sem vendedor ou sem primeira tentativa.
2. **Em contato** — atribuído e com pelo menos uma tentativa registrada.
3. **Sem sucesso** — última tentativa não completou (não atendeu, caixa postal, número inválido). Mostra o contador de tentativas no card.
4. **Engajado** — lead respondeu positivamente (recebeu material, entrou no grupo, apoiador ativo).
5. **Encerrado** — recusou, sem interesse ou descartado. Guarda o motivo.

## Card

Conteúdo visível sem abrir:

- Nome (ou telefone quando não há nome) e cidade/DDD.
- Foto ou iniciais do vendedor responsável; vazio quando ainda não atribuído.
- Origem (ícone da Meta, importação, manual) e há quanto tempo está na coluna.
- Último resultado registrado (ex.: "Não atendeu · 3ª tentativa") e próximo passo agendado, se houver.
- Botões rápidos: **Ligar** (abre o discador já discando) e **WhatsApp**.

## Clique no card → Drawer lateral

Abre por cima do kanban, à direita, com três blocos:

1. **Dados do cliente** — nome, telefone(s), cidade, campos do formulário da Meta, tags, observações livres. Editável.
2. **Dados da plataforma** — origem e campanha/anúncio de origem, data de entrada, coluna atual e histórico de movimentos (quem moveu, quando, de onde para onde), linha do tempo de interações (ligações com duração/resultado/gravação/transcrição, mensagens de WhatsApp, chamadas da IA), tentativas e próximo passo.
3. **Vendedor** — quem recebeu o lead, quando foi atribuído, por qual regra (rodízio, região, manual, IA), tempo até o primeiro contato. Botão **Reatribuir** para gestor.

Rodapé do drawer: **Ligar**, **WhatsApp**, **Registrar resultado** (mesma lista fechada de desfechos usada ao desligar a chamada) e **Mover para** (mesmas regras do arrastar).

## Arrastar (drag and drop)

- O card pode ser arrastado para a **coluna seguinte** ou para a **coluna anterior**. Nunca pula colunas. Soltar em coluna não adjacente devolve o card ao lugar com aviso curto.
- Mover para **Sem sucesso** ou **Encerrado** exige escolher o motivo na lista fechada antes de confirmar; cancelar devolve o card.
- Mover para **Engajado** exige o resultado positivo correspondente.
- Todo movimento grava no histórico: quem, quando, de → para, motivo.
- Movimentos automáticos (resultado de chamada, resposta no WhatsApp, cadência de retentativa) seguem as mesmas regras de adjacência e aparecem no histórico como "sistema".
- Permissão: vendedor move apenas os próprios cards; gestor move qualquer um.

## Regras de dado

- Resultado de interação é sempre um valor da lista fechada (texto livre só em observação).
- Tudo que aparece no drawer vem de dado real; sem dado → "—". Nada de mock.
- Card e drawer leem da mesma fonte de interações que alimenta gamificação e coaching.

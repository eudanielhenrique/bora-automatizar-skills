# ClickUp — 8 Funções Prontas

## 1. Criar task a partir de um lead novo

```
Lead chegou no WhatsApp: Pedro Fulano, 5521999999999, interessado no plano premium.

Cria uma task no Space "Vendas", lista "Follow-up", título "Ligar pra Pedro Fulano",
descrição com o telefone e o interesse, data de vencimento hoje +1 dia,
atribuída pra mim, tag "lead-novo", prioridade Urgent.
```

## 2. Pipeline de SDR

```
Lista todas as tasks da lista "Follow-up" que estão "In Progress" há mais de 3 dias.
Pra cada uma, traz: título, atribuído, dias parada, último comentário.
```

## 3. Fechar venda e mover

```
Pega a task #abc123. Muda o status pra "Fechado", adiciona comentário
"Fechou em R$ 1.497 - pagamento via Stripe id ch_xyz" e move pra lista "Vendas Ganhas".
```

## 4. Comentar com contexto da conversa

```
Adiciona comentário na task #abc123 com o resumo dessa conversa:
"Cliente quer fechar até sexta, mas precisa de aprovação interna do sócio dele.
Próximo contato: terça 14h."
```

## 5. Criar template de onboarding

```
Cliente novo: ACME Ltda.

Cria no Space "Customer Success", lista "Onboarding", uma task "Onboarding ACME"
com 6 subtarefas:
1. Reunião kickoff
2. Coletar acessos
3. Configurar conta
4. Treinar usuários
5. Acompanhamento 30 dias
6. NPS pós-30-dias

Cada subtarefa com prazo +7 dias da anterior, começando hoje.
```

## 6. Limpeza semanal (revisão de pipeline)

```
Lista todas as tasks atribuídas pra mim, sem comentário há mais de 7 dias,
status diferente de "Done". Pra cada uma me pergunta:
- Avançar?
- Aguardar?
- Arquivar?

E executa o que eu responder.
```

## 7. Snapshot do time

```
Conta quantas tasks cada pessoa do meu Team tem com status "In Progress"
em todas as listas. Me devolve em tabela ordenada por volume.
```

## 8. Cronômetro com pomodoro

```
Começa cronômetro na task #abc123. Em 25min me avisa pra fazer pausa.
```

## Dica — handoff entre WhatsApp e ClickUp

Combine com a **Skill `monitoramento-equipe`** (Bônus 8) ou **`whatsapp-atendente`** (Bônus 2):

```
Roda a skill whatsapp-atendente nas conversas de hoje. Pra cada lead QUENTE
identificado, cria uma task no ClickUp na lista "Follow-up" com o resumo
da conversa, prioridade Urgent e prazo +1 dia.
```

Isso transforma o ClickUp num **CRM real**, com cada lead virando tarefa atribuída.

---


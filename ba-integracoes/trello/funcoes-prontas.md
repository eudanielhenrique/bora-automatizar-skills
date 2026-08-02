# Trello — 8 Funções Prontas

## 1. Criar card a partir de um lead

```
Lead novo: Pedro Fulano, 5521999999999.

Cria card no board "Vendas", lista "Novos leads":
- Título: "Pedro Fulano - Premium"
- Descrição: telefone + interesse
- Prazo: +1 dia
- Label: "Lead novo"
- Membro: João
```

## 2. Mover ao longo do funil

```
Move o card abc123 da lista "Novos leads" pra "Em qualificação"
e adiciona comentário "Falou ao telefone, interessado, mandar proposta".
```

## 3. Onboarding com checklist

```
Cliente novo: ACME Ltda.

Cria card "Onboarding ACME" na lista "Em andamento" com checklist:
☐ Kickoff
☐ Coleta de acessos
☐ Configuração inicial
☐ Treinamento dos usuários
☐ NPS pós-30-dias

Membro: João. Prazo: +30 dias.
```

## 4. Cards atrasados

```
Lista todos os cards do board "Operação" com:
- prazo < hoje
- não está na lista "Concluído"

Me devolve em tabela: título, lista, membro, dias de atraso.
```

## 5. Comentar conversas no card

```
Pega o card abc123 e adiciona como comentário esse trecho da conversa
de WhatsApp:

"Cliente disse que precisa de aprovação interna até 6a. Próximo contato terça."
```

## 6. Snapshot diário

```
Conta quantos cards estão em cada lista do board "Vendas".
Me devolve em tabela e adiciona o snapshot como comentário num card
"Histórico Diário" criado pra isso.
```

## 7. Limpeza de fim de semana

```
Arquiva todos os cards da lista "Concluído" do board "Vendas" que estão
parados há mais de 30 dias.
```

## 8. Migração para outra lista por filtro

```
Move todos os cards do board "Vendas" lista "Em qualificação" que tenham
label "Sem retorno >7d" pra lista "Aguardando reativação".
```

## Combo com WhatsApp

```
Roda a skill whatsapp-atendente nas conversas de hoje. Pra cada lead QUENTE,
cria um card no board "Vendas", lista "Novos leads", com nome+telefone,
label "Lead novo", e atribui pro membro responsável do dia.
```

---


# Google Sheets — 8 Funções Prontas

Comandos em PT-BR pra você colar no Claude Code depois que o MCP estiver instalado.

## 1. Registrar lead novo

```
Adiciona uma linha na planilha "CRM Leads", aba "Entrada", com:
- nome: Pedro Fulano
- telefone: 5521999999999
- origem: WhatsApp
- status: novo
- data: hoje
```

## 2. Atualizar status de um lead

```
Na planilha "CRM Leads", aba "Entrada", procura a linha onde nome = "Pedro Fulano"
e muda o status pra "qualificado".
```

## 3. Listar leads quentes da semana

```
Na planilha "CRM Leads", aba "Entrada", filtra leads com:
- status = "quente"
- data >= 7 dias atrás

E me devolve em tabela com nome, telefone e data.
```

## 4. Fechar venda (mover entre abas)

```
Na planilha "CRM", pega o lead da linha 47 da aba "Entrada", copia ele
pra aba "Fechados" e marca a linha original como concluída.
```

## 5. Relatório de vendas do mês

```
Na planilha "Vendas 2026", aba "Pedidos", soma a coluna "Valor" filtrando:
- mês = maio
- status = "pago"

Me devolve total bruto, ticket médio e quantidade de pedidos.
```

## 6. Importar lista de leads pra planilha

```
Pega o arquivo leads_novos.csv da pasta atual, abre a planilha "CRM Leads"
e adiciona cada linha do CSV na aba "Entrada", preenchendo coluna "origem"
com "Importação 24/05" e "status" com "novo".
```

## 7. Conferir duplicidade

```
Na planilha "CRM Leads", aba "Entrada", procura telefones duplicados
e me devolve a lista com a primeira e a última ocorrência de cada um.
```

## 8. Snapshot diário do funil

```
Na planilha "CRM Leads", aba "Entrada", conta quantos leads tem em cada
status (novo, qualificado, quente, fechado, perdido) e adiciona uma linha
na aba "Snapshot Diário" com a data de hoje e cada contagem.
```

## Como usar com cron (snapshot automático)

```bash
#!/bin/bash
# snapshot-diario.sh
claude -p "Roda a função 8 do meu pack google-sheets" > /tmp/snapshot.log 2>&1
```

```cron
# Todo dia útil às 23h45
45 23 * * 1-5  /caminho/snapshot-diario.sh
```

## Dica de produtividade

Ao invés de pedir "adiciona linha X" toda vez, **descreva o gatilho** ao Claude Code uma vez e ele lembra durante a sessão:

> "A partir de agora, sempre que eu mandar um JSON com nome+telefone+origem,
> você adiciona na planilha 'CRM Leads', aba 'Entrada', com status=novo
> e data=hoje."

Isso vira uma mini-automação dentro da sessão. Pra automação 24/7 use cron + claude -p.

---


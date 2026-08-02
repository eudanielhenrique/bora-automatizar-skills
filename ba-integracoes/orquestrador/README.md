# Orquestrador — combinar varias integracoes num pipeline so

Modulo que permite escrever **fluxos compostos** declarativamente, em vez de scripts shell soltos. Ex: "pega pedidos do Shopify → registra no Sheets → notifica Slack → cria task no ClickUp se valor > 5000".

## Por que existe

O resto do pack tem 1 script por integracao. Quando o fluxo combina 4-5 integracoes, voce acaba escrevendo bash bagunçado com `&&` infinitos. Este orquestrador resolve com:

- **Definicao em YAML** — fluxo legivel sem programar.
- **Retry automatico** com backoff exponencial.
- **Tratamento de erro** — uma etapa falhar nao mata o fluxo todo (configuravel).
- **Logging estruturado** — voce sabe exatamente onde travou.
- **Variaveis entre etapas** — output de uma etapa vira input da proxima.

## Estrutura do YAML

```yaml
# fluxo-pedidos.yaml
nome: Pedidos diarios
descricao: Puxa pedidos do Shopify, registra no Sheets, notifica Slack

etapas:
  - id: pedidos
    cmd: python ../shopify/shopify_cliente.py pedidos-hoje
    formato: json

  - id: registrar_planilha
    cmd: |
      claude -p "Lê o JSON em {{pedidos.json}} e adiciona cada pedido na planilha 'Pedidos 2026' aba 'Maio'"
    continuar_em_erro: true

  - id: notificar
    cmd: python ../slack-discord-telegram/notificador.py --canal slack --mensagem "Pedidos de hoje: {{pedidos.count}} | R$ {{pedidos.total}}"

  - id: alertar_grandes
    cmd: |
      python ../clickup/criar_task.py "Pedido grande #{{pedidos.maior_id}} - R$ {{pedidos.maior_valor}}" --prioridade urgent
    condicao: "{{pedidos.maior_valor}} > 5000"
```

## Uso

```bash
python orquestrador.py fluxos/pedidos-diarios.yaml
python orquestrador.py fluxos/financeiro-semanal.yaml --dry-run
python orquestrador.py fluxos/leads-hot.yaml --etapa-de notificar
```

## Conteúdo

```
orquestrador/
├── README.md
├── orquestrador.py           ← engine
└── fluxos/
    ├── pedidos-diarios.yaml
    ├── financeiro-semanal.yaml
    ├── leads-hot.yaml
    └── briefing-amanha.yaml
```

## Setup

```bash
pip install pyyaml
```

Sem isso o YAML nao parseia. Se voce nao tem PyYAML e nao quer instalar, use a versao JSON dos fluxos (`fluxos/*.json` espelhado).

---


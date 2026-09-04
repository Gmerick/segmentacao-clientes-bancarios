# Dicionário de dados

## `data/raw/customers.csv`

| Campo | Tipo | Descrição |
|---|---|---|
| `customer_id` | texto | Identificador sintético do cliente |
| `synthetic_archetype` | texto | Perfil latente, usado somente para validação do experimento |
| `age` | inteiro | Idade |
| `region` | texto | Macrorregião brasileira |
| `occupation` | texto | Ocupação simulada |
| `monthly_income` | decimal | Renda mensal estimada |
| `tenure_months` | inteiro | Meses de relacionamento |
| `checking_balance` | decimal | Saldo em conta corrente |
| `savings_balance` | decimal | Saldo em poupança |
| `investment_balance` | decimal | Saldo em investimentos |
| `credit_card_limit` | decimal | Limite do cartão |
| `credit_utilization` | decimal | Percentual utilizado do limite |
| `loan_balance` | decimal | Saldo de empréstimos |
| `delinquency_events_12m` | inteiro | Eventos de atraso em 12 meses |
| `has_*` | booleano 0/1 | Indicadores de seis produtos bancários |

## `data/raw/monthly_activity.csv`

| Campo | Tipo | Descrição |
|---|---|---|
| `customer_id` | texto | Chave do cliente |
| `month` | data | Primeiro dia do mês de referência |
| `transaction_count` | inteiro | Quantidade de transações |
| `total_inflow` | decimal | Entradas do mês |
| `total_outflow` | decimal | Saídas do mês |
| `pix_count` | inteiro | Quantidade de PIX |
| `card_spend` | decimal | Gastos no cartão |
| `cash_withdrawals` | inteiro | Saques |
| `app_logins` | inteiro | Acessos ao aplicativo |
| `branch_visits` | inteiro | Visitas à agência |
| `digital_transaction_share` | decimal | Participação digital entre 0 e 1 |

## `data/processed/customer_segments.csv`

Além dos campos anteriores, contém atributos de comportamento e:

| Campo | Tipo | Descrição |
|---|---|---|
| `product_count` | inteiro | Produtos contratados |
| `asset_total` | decimal | Conta + poupança + investimentos |
| `credit_exposure` | decimal | Empréstimos + parcela utilizada do limite |
| `savings_rate` | decimal | Diferença entre entradas e saídas / entradas |
| `avg_ticket` | decimal | Saídas / transações |
| `movement_volatility` | decimal | Desvio das saídas / média das saídas |
| `relationship_value` | decimal | Patrimônio + 25% da exposição a crédito |
| `cluster_id` | inteiro | ID técnico do cluster |
| `segment` | texto | Persona de negócio |
| `segment_description` | texto | Interpretação do segmento |

## Demais saídas

- `segment_profiles.csv`: indicadores consolidados e ação sugerida.
- `monthly_segment_activity.csv`: evolução mensal por segmento.
- `model_selection.csv`: métricas para K=2–8.


# Medidas DAX

```DAX
Total Clientes = DISTINCTCOUNT(Customers[customer_id])

Total Segmentos = DISTINCTCOUNT(Customers[segment])

Renda Média = AVERAGE(Customers[monthly_income])

Patrimônio Total = SUM(Customers[asset_total])

Patrimônio Médio = AVERAGE(Customers[asset_total])

Investimentos Totais = SUM(Customers[investment_balance])

Exposição de Crédito = SUM(Customers[credit_exposure])

Utilização Média de Crédito = AVERAGE(Customers[credit_utilization])

Produtos por Cliente = AVERAGE(Customers[product_count])

Participação Digital Média = AVERAGE(Customers[digital_transaction_share])

Clientes com Atraso =
CALCULATE(
    [Total Clientes],
    Customers[delinquency_events_12m] > 0
)

Taxa de Clientes com Atraso = DIVIDE([Clientes com Atraso], [Total Clientes])

Transações = SUM(MonthlyActivity[transactions])

Entradas = SUM(MonthlyActivity[total_inflow])

Saídas = SUM(MonthlyActivity[total_outflow])

Fluxo Líquido = [Entradas] - [Saídas]

Clientes % =
DIVIDE(
    [Total Clientes],
    CALCULATE([Total Clientes], ALL(Segments))
)

Rank Segmento por Patrimônio =
RANKX(ALL(Segments[segment]), [Patrimônio Total],, DESC, Dense)
```

Formate moeda em R$ e percentuais com uma casa decimal.


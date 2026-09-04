# Modelo de dados no Power BI

## Tabelas

### `Customers`

Fonte: `customer_segments.csv`. Granularidade: um cliente por linha. Chave: `customer_id`.

### `MonthlyActivity`

Fonte: `monthly_segment_activity.csv`. Granularidade: mês × segmento.

### `Segments`

Fonte: `segment_profiles.csv`. Granularidade: um segmento por linha. Chave: `segment`.

### `Calendar`

Crie em DAX:

```DAX
Calendar =
ADDCOLUMNS (
    CALENDAR ( DATE(2025, 1, 1), DATE(2025, 12, 31) ),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month", FORMAT([Date], "mmm"),
    "Year Month", FORMAT([Date], "yyyy-MM")
)
```

## Relacionamentos

| Origem | Destino | Cardinalidade | Filtro |
|---|---|---|---|
| `Segments[segment]` | `Customers[segment]` | 1:* | Único |
| `Segments[segment]` | `MonthlyActivity[segment]` | 1:* | Único |
| `Calendar[Date]` | `MonthlyActivity[month]` | 1:* | Único |

Não relacione diretamente as duas tabelas fato.

## Tipagem

- IDs e segmentos: texto;
- `month`: data;
- saldos e fluxos: moeda;
- shares, utilização e taxas: percentual decimal;
- contagens: número inteiro.


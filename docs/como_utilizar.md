# Como utilizar

## Requisitos

- Python 3.10 ou superior;
- 1 GB livre para ambiente e artefatos;
- Power BI Desktop opcional.

## Execução rápida

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_pipeline.py
```

Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_pipeline.py
```

## Saídas principais

| Arquivo | Uso |
|---|---|
| `customer_segments.csv` | Base detalhada para análise e Power BI |
| `segment_profiles.csv` | Comparação executiva dos cinco segmentos |
| `monthly_segment_activity.csv` | Tendências mensais |
| `model_selection.csv` | Justificativa quantitativa de K |
| `dashboard_preview.png` | Referência visual |
| `metrics.json` | Métricas auditáveis do pipeline |

## Power BI

1. Abra Power BI Desktop.
2. Selecione **Obter dados → Texto/CSV**.
3. Importe as três tabelas processadas.
4. Converta `month` para data e percentuais para decimal.
5. Crie os relacionamentos descritos em `powerbi/data_model.md`.
6. Copie as medidas de `powerbi/dax_measures.md`.
7. Importe o tema JSON em **Exibir → Temas → Procurar temas**.
8. Construa as páginas conforme o blueprint.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Usar dados próprios

1. Substitua os arquivos em `data/raw/` mantendo o dicionário ou adapte `src/features.py`.
2. Remova qualquer identificador pessoal desnecessário.
3. Revise as 18 variáveis e trate consentimento/LGPD.
4. Reavalie K e estabilidade; não mantenha cinco grupos automaticamente.
5. Reinterprete os centroides e renomeie os segmentos.
6. Valide com áreas de negócio antes de ativar campanhas.


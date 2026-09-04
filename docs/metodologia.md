# Metodologia

## 1. Objetivo

Criar grupos homogêneos de clientes bancários para apoiar personalização, relacionamento, evolução de portfólio, inclusão digital e gestão preventiva de risco.

## 2. Dados sintéticos

A base simula 8.000 clientes e 12 meses de atividade, totalizando 96.000 registros mensais. Cinco arquétipos latentes controlam distribuições de renda, idade, patrimônio, produtos, crédito, volume transacional e preferência de canal.

O gerador utiliza semente fixa (`42`). Isso permite reproduzir exatamente os mesmos dados e resultados.

O campo `synthetic_archetype` existe somente para avaliação acadêmica. Ele é removido antes de qualquer transformação ou treinamento.

## 3. Preparação com Pandas

As movimentações mensais são consolidadas por cliente. São calculados:

- médias e totais de transações, entradas e saídas;
- volatilidade relativa das saídas;
- logins no aplicativo e visitas à agência;
- participação de transações digitais;
- quantidade de produtos;
- patrimônio total;
- exposição a crédito;
- taxa de poupança e ticket médio;
- valor ampliado do relacionamento.

Campos numéricos com ausências simuladas são imputados pela mediana dentro do pipeline, evitando descarte de clientes.

## 4. Escala

K-Means é sensível à magnitude. Sem padronização, investimentos e saldos dominariam idade, produtos e proporções. Por isso, todos os 18 atributos são transformados com `StandardScaler` após imputação.

## 5. Escolha de K

São treinadas soluções de K=2 a K=8, com 20 inicializações por valor. Quatro métricas são registradas:

| Métrica | Interpretação |
|---|---|
| Inertia | Dispersão interna; menor é melhor, mas sempre cai quando K cresce |
| Silhouette | Coesão e separação; maior é melhor |
| Calinski-Harabasz | Separação relativa; maior é melhor |
| Davies-Bouldin | Similaridade entre clusters; menor é melhor |

K=5 não maximiza silhouette. A escolha preserva cinco comportamentos de negócio relevantes que seriam fundidos em soluções menores. A decisão é registrada em `model_selection.csv` e tratada como compromisso entre estatística, interpretabilidade e ação.

## 6. Treinamento

O modelo final usa:

- algoritmo: K-Means;
- `n_clusters=5`;
- `n_init=30`;
- `random_state=42`;
- distância euclidiana sobre dados padronizados.

## 7. Nomenclatura

Os IDs 0–4 não têm significado intrínseco. Um pós-processamento interpreta centroides e atribui nomes usando renda, investimentos, patrimônio, digitalização, crédito, idade e agência. Nenhum nome é passado ao modelo.

## 8. Validação sintética

O ARI compara os clusters com os arquétipos usados pelo gerador. Resultado: **0,942**. A métrica próxima de 1 indica forte correspondência, mas só é possível porque se trata de um experimento sintético.

## 9. Entregáveis

- tabela cliente × segmento;
- perfis agregados e ações sugeridas;
- atividade mensal por segmento;
- comparação de K;
- pipeline treinado localmente;
- gráficos e dashboard de referência;
- modelo, medidas DAX, tema e layout para Power BI.

## 10. Monitoramento recomendado

Em produção, acompanhar trimestralmente:

- variação no tamanho dos segmentos;
- deslocamento dos centroides;
- clientes que mudam de segmento;
- mudança na distribuição das variáveis;
- performance de campanhas por segmento;
- reclamações, exclusões e indicadores de tratamento desigual.


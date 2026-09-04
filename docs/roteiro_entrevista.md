# Roteiro para entrevista

## Pitch de 60 segundos

> Desenvolvi um projeto ponta a ponta de segmentação de clientes bancários com oito mil clientes sintéticos e 96 mil registros mensais. Usei Pandas para consolidar comportamento, renda, produtos, patrimônio, crédito e canais em 18 atributos. Depois padronizei as variáveis e comparei soluções K-Means de dois a oito clusters com quatro métricas. Selecionei cinco segmentos por equilíbrio entre qualidade estatística e utilidade de negócio. Os grupos geraram estratégias distintas para alta renda, clientes digitais, usuários intensivos de crédito, clientes tradicionais e jovens em ascensão. Também preparei tabelas, medidas DAX, tema e layout para Power BI, além de testes automatizados e GitHub Actions. Como a base é sintética, validei a recuperação dos padrões com ARI de 0,942, sem usar o perfil original no treinamento.

## Apresentação de cinco minutos

### 1. Problema — 30 segundos

Explique que uma comunicação única para toda a carteira ignora necessidades distintas. O objetivo é transformar comportamento bancário em grupos acionáveis.

### 2. Dados — 45 segundos

Mostre 8.000 clientes, 12 meses e 96.000 observações. Destaque renda, produtos, saldos, crédito, transações, app e agência. Informe que os dados são sintéticos por privacidade e reprodutibilidade.

### 3. Preparação — 60 segundos

Explique a agregação com Pandas, a criação de patrimônio, exposição a crédito, taxa de poupança e volatilidade, a imputação pela mediana e a padronização obrigatória para K-Means.

### 4. Modelo — 60 segundos

Apresente a comparação K=2–8. Diga que K=5 não foi escolhido apenas pelo maior silhouette: preservou personas diferentes e acionáveis. Mostre que o perfil sintético foi excluído do treinamento.

### 5. Resultados — 75 segundos

Percorra os cinco segmentos e associe cada um a uma ação. Priorize:

- Alta Renda: retenção e investimentos;
- Digital: cross-sell contextual;
- Crédito: prevenção e educação financeira;
- Tradicional: migração digital assistida;
- Jovem: evolução do relacionamento.

### 6. Limitações — 30 segundos

Reconheça base sintética, suposição geométrica do K-Means, necessidade de estabilidade temporal, LGPD, avaliação de viés e revisão humana.

## Perguntas prováveis

### Por que K-Means?

É rápido, conhecido, reproduzível e facilita explicar centroides. Também permite demonstrar claramente a importância da escala. Eu compararia com clustering hierárquico, GMM ou HDBSCAN em uma evolução.

### Por que padronizar?

Porque a distância euclidiana seria dominada por valores monetários. Sem escala, idade, produtos e proporções quase não influenciariam o resultado.

### Por que K=5 se K=2 tem maior silhouette?

K=2 separa principalmente alta renda do restante e perde nuances importantes. K=5 tem menor separação geométrica, mas distingue cinco comportamentos consistentes e acionáveis. A decisão combina métricas, interpretabilidade, tamanho e objetivo operacional.

### O que significa ARI de 0,942?

Como gerei a base, conheço os arquétipos ocultos. O ARI mede a concordância entre esses perfis e os clusters, sem depender do número dos rótulos. Ele não foi usado para treinar nem escolher nomes.

### Como validaria em produção?

Com estabilidade por período, análise dos centroides, taxa de migração, testes de campanhas, especialistas de negócio, fairness, LGPD e métricas posteriores como conversão, satisfação e inadimplência.

### Cluster é uma regra definitiva?

Não. É uma fotografia comportamental sujeita a mudança. Deve apoiar decisões e experimentos, não determinar tratamento automático ou restringir acesso a produtos.

## Demonstração prática

1. Abra o README e contextualize o problema.
2. Mostre `generate_data.py` e a proteção da base sintética.
3. Execute `python run_pipeline.py`.
4. Abra `model_selection.csv` e explique o trade-off de K.
5. Compare os perfis no dashboard.
6. Mostre DAX, modelo e blueprint do Power BI.
7. Encerre com limitações e próximos passos.


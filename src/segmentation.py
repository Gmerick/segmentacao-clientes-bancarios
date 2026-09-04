"""Seleção de K, clusterização e tradução dos clusters em personas de negócio."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config import CLUSTER_FEATURES, MODEL_DIR, RANDOM_SEED, SELECTED_K


SEGMENT_DESCRIPTIONS = {
    "Alta Renda Investidor": "Alta renda, patrimônio elevado, investimentos e amplo relacionamento com o banco.",
    "Digital Multirrelacionado": "Uso intenso de canais digitais, alto volume transacional e vários produtos.",
    "Crédito Intensivo": "Maior exposição a crédito, utilização elevada e maior incidência de atraso.",
    "Tradicional Essencial": "Relacionamento longo, baixa digitalização, mais visitas à agência e produtos básicos.",
    "Jovem em Ascensão": "Clientes jovens, digitais, com renda e patrimônio em fase de crescimento.",
}


def make_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    return ColumnTransformer([("numeric", numeric_pipeline, CLUSTER_FEATURES)], remainder="drop")


def evaluate_k_values(matrix: np.ndarray, k_values=range(2, 9)) -> pd.DataFrame:
    rows = []
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=RANDOM_SEED, n_init=20)
        labels = model.fit_predict(matrix)
        rows.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette": silhouette_score(matrix, labels, sample_size=min(3_000, len(matrix)), random_state=RANDOM_SEED),
            "calinski_harabasz": calinski_harabasz_score(matrix, labels),
            "davies_bouldin": davies_bouldin_score(matrix, labels),
            "selected": k == SELECTED_K,
        })
    return pd.DataFrame(rows)


def _business_names(scored: pd.DataFrame) -> dict[int, str]:
    centroids = scored.groupby("cluster_id").mean(numeric_only=True)
    z = (centroids - centroids.mean()) / centroids.std(ddof=0).replace(0, 1)
    remaining = set(centroids.index.tolist())
    mapping: dict[int, str] = {}

    def assign(name: str, score: pd.Series) -> None:
        candidates = score.loc[list(remaining)]
        cluster = int(candidates.idxmax())
        mapping[cluster] = name
        remaining.remove(cluster)

    assign("Alta Renda Investidor", z["monthly_income"] + z["investment_balance"] + z["asset_total"] + .4 * z["product_count"])
    assign("Digital Multirrelacionado", z["avg_app_logins"] + z["digital_transaction_share"] + z["avg_monthly_transactions"] + .3 * z["product_count"])
    assign("Crédito Intensivo", z["credit_utilization"] + z["credit_exposure"] + z["delinquency_events_12m"] - .3 * z["asset_total"])
    assign("Tradicional Essencial", z["avg_branch_visits"] + z["age"] + .4 * z["tenure_months"] - z["digital_transaction_share"])
    for cluster in remaining:
        mapping[int(cluster)] = "Jovem em Ascensão"
    return mapping


def segment_customers(features: pd.DataFrame, save_model: bool = True) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    preprocessor = make_preprocessor()
    matrix = preprocessor.fit_transform(features)
    evaluation = evaluate_k_values(matrix)
    model = KMeans(n_clusters=SELECTED_K, random_state=RANDOM_SEED, n_init=30)
    labels = model.fit_predict(matrix)
    scored = features.copy()
    scored["cluster_id"] = labels
    mapping = _business_names(scored)
    scored["segment"] = scored["cluster_id"].map(mapping)
    scored["segment_description"] = scored["segment"].map(SEGMENT_DESCRIPTIONS)

    metrics = {
        "selected_k": SELECTED_K,
        "silhouette": float(silhouette_score(matrix, labels, sample_size=min(3_000, len(matrix)), random_state=RANDOM_SEED)),
        "calinski_harabasz": float(calinski_harabasz_score(matrix, labels)),
        "davies_bouldin": float(davies_bouldin_score(matrix, labels)),
        "adjusted_rand_vs_synthetic_archetype": float(adjusted_rand_score(scored["synthetic_archetype"], labels)),
        "cluster_name_mapping": {str(k): v for k, v in mapping.items()},
    }
    if save_model:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump({"preprocessor": preprocessor, "model": model, "mapping": mapping}, MODEL_DIR / "customer_segmentation.joblib")
        (MODEL_DIR / "model_metadata.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    return scored, evaluation, metrics


def build_segment_profiles(scored: pd.DataFrame) -> pd.DataFrame:
    profiles = scored.groupby("segment", sort=False).agg(
        customers=("customer_id", "count"),
        avg_age=("age", "mean"),
        avg_income=("monthly_income", "mean"),
        avg_products=("product_count", "mean"),
        avg_assets=("asset_total", "mean"),
        avg_investments=("investment_balance", "mean"),
        avg_credit_exposure=("credit_exposure", "mean"),
        avg_credit_utilization=("credit_utilization", "mean"),
        avg_monthly_transactions=("avg_monthly_transactions", "mean"),
        avg_monthly_outflow=("avg_monthly_outflow", "mean"),
        avg_app_logins=("avg_app_logins", "mean"),
        avg_branch_visits=("avg_branch_visits", "mean"),
        avg_digital_share=("digital_transaction_share", "mean"),
        avg_delinquency_events=("delinquency_events_12m", "mean"),
        total_relationship_value=("relationship_value", "sum"),
    ).reset_index()
    profiles["customer_share"] = profiles["customers"] / profiles["customers"].sum()
    profiles["recommended_action"] = profiles["segment"].map({
        "Alta Renda Investidor": "Retenção premium, assessoria e diversificação de investimentos",
        "Digital Multirrelacionado": "Ofertas digitais personalizadas e cross-sell contextual",
        "Crédito Intensivo": "Gestão preventiva de risco, renegociação e educação financeira",
        "Tradicional Essencial": "Migração digital assistida e simplificação da jornada",
        "Jovem em Ascensão": "Programa de evolução financeira e produtos de entrada",
    })
    return profiles


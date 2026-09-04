"""Executa a geração, engenharia de atributos, segmentação e relatórios."""

from src.features import build_customer_features
from src.generate_data import generate_and_save
from src.reporting import create_dashboard, create_figures, export_powerbi_tables, write_metrics
from src.segmentation import build_segment_profiles, segment_customers


def run_pipeline() -> dict:
    customers, activity = generate_and_save()
    features = build_customer_features(customers, activity)
    scored, evaluation, metrics = segment_customers(features)
    profiles = build_segment_profiles(scored)
    export_powerbi_tables(scored, profiles, activity, evaluation)
    create_figures(scored, profiles, evaluation)
    create_dashboard(scored, profiles, metrics)
    final_metrics = write_metrics(metrics, scored, profiles)
    print("Pipeline concluído com sucesso.")
    print(f"Clientes: {final_metrics['customers']:,}")
    print(f"Segmentos: {final_metrics['segments']}")
    print(f"Silhouette: {final_metrics['silhouette']:.4f}")
    print(f"ARI sintético: {final_metrics['adjusted_rand_vs_synthetic_archetype']:.4f}")
    return final_metrics


if __name__ == "__main__":
    run_pipeline()


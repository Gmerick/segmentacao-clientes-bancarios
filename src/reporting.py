"""Exportações analíticas e visualizações do projeto."""

from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .config import DATA_PROCESSED_DIR, FIGURES_DIR, REPORTS_DIR, ensure_directories

SEGMENT_COLORS = {
    "Alta Renda Investidor": "#7C3AED",
    "Digital Multirrelacionado": "#10B981",
    "Crédito Intensivo": "#F59E0B",
    "Tradicional Essencial": "#1D4ED8",
    "Jovem em Ascensão": "#06B6D4",
}
PALETTE = list(SEGMENT_COLORS.values())


def export_powerbi_tables(scored: pd.DataFrame, profiles: pd.DataFrame, activity: pd.DataFrame, evaluation: pd.DataFrame) -> pd.DataFrame:
    ensure_directories()
    scored.to_csv(DATA_PROCESSED_DIR / "customer_segments.csv", index=False)
    profiles.to_csv(DATA_PROCESSED_DIR / "segment_profiles.csv", index=False)
    evaluation.to_csv(DATA_PROCESSED_DIR / "model_selection.csv", index=False)
    activity_with_segment = activity.merge(scored[["customer_id", "segment"]], on="customer_id", how="left", validate="many_to_one")
    monthly = activity_with_segment.groupby(["month", "segment"], as_index=False).agg(
        active_customers=("customer_id", "nunique"),
        transactions=("transaction_count", "sum"),
        total_inflow=("total_inflow", "sum"),
        total_outflow=("total_outflow", "sum"),
        app_logins=("app_logins", "sum"),
        branch_visits=("branch_visits", "sum"),
    )
    monthly.to_csv(DATA_PROCESSED_DIR / "monthly_segment_activity.csv", index=False)
    return monthly


def _save_figure(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIGURES_DIR / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def create_figures(scored: pd.DataFrame, profiles: pd.DataFrame, evaluation: pd.DataFrame) -> None:
    ensure_directories()
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ordered = profiles.sort_values("customers", ascending=True)
    ax.barh(ordered["segment"], ordered["customers"], color=ordered["segment"].map(SEGMENT_COLORS))
    ax.set(title="Clientes por segmento", xlabel="Clientes", ylabel="")
    for i, value in enumerate(ordered["customers"]):
        ax.text(value + 25, i, f"{value:,}".replace(",", "."), va="center", fontsize=9)
    _save_figure(fig, "segment_sizes.png")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(evaluation["k"], evaluation["silhouette"], marker="o", color=PALETTE[0], linewidth=2)
    selected = evaluation[evaluation["selected"]].iloc[0]
    ax.scatter([selected["k"]], [selected["silhouette"]], s=120, color=PALETTE[2], zorder=3, label="K selecionado")
    ax.set(title="Qualidade da segmentação por número de clusters", xlabel="Número de clusters (K)", ylabel="Silhouette")
    ax.legend()
    _save_figure(fig, "model_selection.png")

    fig, ax = plt.subplots(figsize=(10, 6))
    sample = scored.sample(min(2_500, len(scored)), random_state=42)
    sns.scatterplot(data=sample, x="monthly_income", y="investment_balance", hue="segment", palette=SEGMENT_COLORS, alpha=.62, s=35, ax=ax)
    ax.set(title="Renda e investimentos por segmento", xlabel="Renda mensal (R$)", ylabel="Investimentos (R$)")
    ax.legend(title="Segmento", bbox_to_anchor=(1.02, 1), loc="upper left")
    _save_figure(fig, "income_investments_scatter.png")


def create_dashboard(scored: pd.DataFrame, profiles: pd.DataFrame, metrics: dict) -> None:
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(16, 10), facecolor="#F4F7FB")
    gs = fig.add_gridspec(3, 4, height_ratios=[.7, 2.2, 2.2], hspace=.48, wspace=.40)
    fig.suptitle("Segmentação de Clientes Bancários", x=.055, y=.975, ha="left", fontsize=23, fontweight="bold", color="#12213A")
    fig.text(.055, .936, "Perfis comportamentais para personalização, relacionamento e gestão de risco", fontsize=11, color="#53657A")

    cards = [
        ("CLIENTES", f"{len(scored):,}".replace(",", ".")),
        ("SEGMENTOS", str(metrics["selected_k"])),
        ("SILHOUETTE", f"{metrics['silhouette']:.3f}"),
        ("PATRIMÔNIO ANALISADO", f"R$ {scored['asset_total'].sum()/1e6:.1f} mi".replace(".", ",")),
    ]
    for i, (label, value) in enumerate(cards):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor("white")
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(.06, .68, label, transform=ax.transAxes, fontsize=9, color="#607087", fontweight="bold")
        ax.text(.06, .20, value, transform=ax.transAxes, fontsize=20, color="#12213A", fontweight="bold")

    ax1 = fig.add_subplot(gs[1, :2])
    ordered = profiles.sort_values("customers")
    ax1.barh(ordered["segment"], ordered["customers"], color=ordered["segment"].map(SEGMENT_COLORS))
    ax1.set_title("Tamanho dos segmentos", loc="left", fontweight="bold")
    ax1.set_xlabel("Clientes"); ax1.set_ylabel("")

    ax2 = fig.add_subplot(gs[1, 2:])
    ax2.scatter(profiles["avg_income"], profiles["avg_investments"], s=profiles["customers"]*.20, c=profiles["segment"].map(SEGMENT_COLORS), alpha=.82, edgecolor="white", linewidth=1.5)
    short_labels = {
        "Alta Renda Investidor": "Alta Renda",
        "Digital Multirrelacionado": "Digital",
        "Crédito Intensivo": "Crédito",
        "Tradicional Essencial": "Tradicional",
        "Jovem em Ascensão": "Jovem",
    }
    offsets = {segment: (6, 6) for segment in short_labels}
    for _, row in profiles.iterrows():
        ax2.annotate(short_labels[row["segment"]], (row["avg_income"], row["avg_investments"]), xytext=offsets[row["segment"]], textcoords="offset points", fontsize=8)
    ax2.set_title("Renda × investimentos", loc="left", fontweight="bold")
    ax2.set_xlabel("Renda mensal média (R$)"); ax2.set_ylabel("Investimentos médios (R$)")
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xticks([4_000, 5_000, 10_000, 20_000], ["4 mil", "5 mil", "10 mil", "20 mil"])
    ax2.set_yticks([2_500, 5_000, 10_000, 25_000, 100_000, 250_000], ["2,5 mil", "5 mil", "10 mil", "25 mil", "100 mil", "250 mil"])

    ax3 = fig.add_subplot(gs[2, :2])
    x = np.arange(len(profiles)); width = .36
    ax3.bar(x-width/2, profiles["avg_digital_share"]*100, width, label="Transações digitais (%)", color=PALETTE[0])
    ax3.bar(x+width/2, profiles["avg_credit_utilization"]*100, width, label="Utilização de crédito (%)", color=PALETTE[2])
    ax3.set_xticks(x, [s.replace(" ", "\n", 1) for s in profiles["segment"]], fontsize=8)
    ax3.set_ylabel("Percentual"); ax3.set_title("Digitalização e uso de crédito", loc="left", fontweight="bold"); ax3.legend(fontsize=8)

    ax4 = fig.add_subplot(gs[2, 2:])
    action = profiles.sort_values("avg_products")
    ax4.barh(action["segment"], action["avg_products"], color=action["segment"].map(SEGMENT_COLORS))
    ax4.set_title("Produtos por cliente", loc="left", fontweight="bold")
    ax4.set_xlabel("Média de produtos"); ax4.set_ylabel("")
    for i, value in enumerate(action["avg_products"]): ax4.text(value+.03, i, f"{value:.1f}", va="center", fontsize=9)

    fig.text(.055, .018, "Base sintética • K-Means • Resultados para fins educacionais e de portfólio", fontsize=9, color="#6B7A90")
    fig.savefig(REPORTS_DIR / "dashboard_preview.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def write_metrics(metrics: dict, scored: pd.DataFrame, profiles: pd.DataFrame) -> dict:
    final = {
        **metrics,
        "customers": int(len(scored)),
        "segments": int(scored["segment"].nunique()),
        "total_assets": float(scored["asset_total"].sum()),
        "total_relationship_value": float(scored["relationship_value"].sum()),
        "largest_segment": str(profiles.sort_values("customers", ascending=False).iloc[0]["segment"]),
        "largest_segment_customers": int(profiles["customers"].max()),
    }
    (REPORTS_DIR / "metrics.json").write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    return final

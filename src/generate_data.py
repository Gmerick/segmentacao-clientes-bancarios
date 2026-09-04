"""Geração determinística de uma carteira bancária sintética."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import DATA_RAW_DIR, N_CUSTOMERS, N_MONTHS, PROFILE_WEIGHTS, RANDOM_SEED, ensure_directories


PROFILE_PARAMS = {
    "Alta Renda Investidor": {
        "age": (47, 9), "income": (21_000, 5_500), "tenure": (128, 48),
        "checking": (18_000, 9_000), "savings": (42_000, 25_000), "investments": (220_000, 105_000),
        "card_limit": (32_000, 9_000), "utilization": (0.24, 0.10), "loan": (36_000, 30_000),
        "tx": (58, 13), "inflow_mult": 1.08, "outflow_mult": 0.72, "app": (24, 8), "branch": (0.8, 0.7),
        "digital_share": (0.82, 0.08), "delinquency": 0.06,
        "products": {"has_credit_card": .96, "has_savings": .92, "has_investments": .98, "has_personal_loan": .22, "has_insurance": .78, "has_mortgage": .31},
    },
    "Digital Multirrelacionado": {
        "age": (35, 7), "income": (8_600, 2_300), "tenure": (62, 28),
        "checking": (6_200, 3_800), "savings": (11_000, 8_000), "investments": (21_000, 18_000),
        "card_limit": (14_000, 4_500), "utilization": (0.38, 0.14), "loan": (17_000, 16_000),
        "tx": (78, 16), "inflow_mult": 1.02, "outflow_mult": 0.83, "app": (55, 13), "branch": (0.15, 0.3),
        "digital_share": (0.96, 0.025), "delinquency": 0.12,
        "products": {"has_credit_card": .97, "has_savings": .82, "has_investments": .66, "has_personal_loan": .32, "has_insurance": .58, "has_mortgage": .18},
    },
    "Crédito Intensivo": {
        "age": (41, 10), "income": (5_100, 1_600), "tenure": (71, 34),
        "checking": (1_900, 1_600), "savings": (2_400, 2_500), "investments": (1_600, 2_500),
        "card_limit": (10_500, 3_600), "utilization": (0.81, 0.11), "loan": (42_000, 22_000),
        "tx": (51, 14), "inflow_mult": 1.00, "outflow_mult": 0.96, "app": (29, 10), "branch": (1.1, 0.8),
        "digital_share": (0.78, 0.11), "delinquency": 0.68,
        "products": {"has_credit_card": .95, "has_savings": .42, "has_investments": .12, "has_personal_loan": .87, "has_insurance": .24, "has_mortgage": .28},
    },
    "Tradicional Essencial": {
        "age": (58, 10), "income": (3_900, 1_300), "tenure": (151, 58),
        "checking": (3_800, 2_800), "savings": (9_500, 7_500), "investments": (3_000, 4_500),
        "card_limit": (5_600, 2_200), "utilization": (0.27, 0.15), "loan": (8_000, 11_000),
        "tx": (24, 8), "inflow_mult": 1.01, "outflow_mult": 0.73, "app": (6, 5), "branch": (3.5, 1.4),
        "digital_share": (0.37, 0.16), "delinquency": 0.16,
        "products": {"has_credit_card": .67, "has_savings": .88, "has_investments": .25, "has_personal_loan": .19, "has_insurance": .42, "has_mortgage": .11},
    },
    "Jovem em Ascensão": {
        "age": (27, 4), "income": (4_600, 1_500), "tenure": (24, 14),
        "checking": (2_600, 1_900), "savings": (5_800, 4_800), "investments": (5_000, 5_500),
        "card_limit": (6_800, 2_500), "utilization": (0.46, 0.16), "loan": (6_500, 8_000),
        "tx": (63, 14), "inflow_mult": 1.03, "outflow_mult": 0.78, "app": (47, 12), "branch": (0.25, 0.35),
        "digital_share": (0.94, 0.04), "delinquency": 0.20,
        "products": {"has_credit_card": .91, "has_savings": .73, "has_investments": .41, "has_personal_loan": .22, "has_insurance": .21, "has_mortgage": .03},
    },
}


def _positive_normal(rng: np.random.Generator, mean: float, sd: float, minimum: float = 0) -> float:
    return float(max(minimum, rng.normal(mean, sd)))


def generate_customers(n_customers: int = N_CUSTOMERS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    profiles = list(PROFILE_WEIGHTS)
    archetypes = rng.choice(profiles, size=n_customers, p=list(PROFILE_WEIGHTS.values()))
    regions = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    region_weights = [.48, .18, .20, .09, .05]
    occupations = ["Assalariado", "Autônomo", "Empresário", "Aposentado", "Servidor público", "Estudante"]
    rows: list[dict] = []

    for idx, profile in enumerate(archetypes, start=1):
        p = PROFILE_PARAMS[profile]
        age = int(np.clip(rng.normal(*p["age"]), 18, 82))
        income = _positive_normal(rng, *p["income"], minimum=1_200)
        products = {key: int(rng.random() < probability) for key, probability in p["products"].items()}
        employment = rng.choice(occupations, p=[.47, .18, .09, .12, .10, .04])
        if profile == "Alta Renda Investidor":
            employment = rng.choice(["Empresário", "Assalariado", "Servidor público"], p=[.42, .43, .15])
        elif profile == "Tradicional Essencial" and age >= 60:
            employment = rng.choice(["Aposentado", "Autônomo", "Assalariado"], p=[.62, .18, .20])
        elif profile == "Jovem em Ascensão":
            employment = rng.choice(["Assalariado", "Autônomo", "Estudante"], p=[.69, .22, .09])

        rows.append({
            "customer_id": f"CLI{idx:06d}",
            "synthetic_archetype": profile,
            "age": age,
            "region": rng.choice(regions, p=region_weights),
            "occupation": employment,
            "monthly_income": round(income, 2),
            "tenure_months": int(np.clip(rng.normal(*p["tenure"]), 1, 360)),
            "checking_balance": round(_positive_normal(rng, *p["checking"]), 2),
            "savings_balance": round(_positive_normal(rng, *p["savings"]), 2),
            "investment_balance": round(_positive_normal(rng, *p["investments"]), 2),
            "credit_card_limit": round(_positive_normal(rng, *p["card_limit"], minimum=500), 2),
            "credit_utilization": round(float(np.clip(rng.normal(*p["utilization"]), 0.01, 0.99)), 4),
            "loan_balance": round(_positive_normal(rng, *p["loan"]), 2),
            "delinquency_events_12m": int(min(rng.poisson(p["delinquency"]), 6)),
            **products,
        })
    customers = pd.DataFrame(rows)
    for col in ["savings_balance", "investment_balance", "credit_card_limit"]:
        missing_idx = rng.choice(customers.index, size=max(1, n_customers // 100), replace=False)
        customers.loc[missing_idx, col] = np.nan
    return customers


def generate_monthly_activity(customers: pd.DataFrame, months: int = N_MONTHS, seed: int = RANDOM_SEED + 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    month_index = pd.date_range("2025-01-01", periods=months, freq="MS")
    rows: list[dict] = []
    customer_lookup = customers.set_index("customer_id")

    for customer_id, customer in customer_lookup.iterrows():
        p = PROFILE_PARAMS[customer["synthetic_archetype"]]
        income = float(customer["monthly_income"])
        base_tx = max(5, rng.normal(*p["tx"]))
        customer_factor = rng.lognormal(0, .10)
        for month_number, month in enumerate(month_index):
            seasonality = 1 + (0.12 if month.month == 12 else 0) + (0.05 if month.month in (5, 11) else 0)
            trend = 1 + month_number * (0.006 if customer["synthetic_archetype"] in ("Jovem em Ascensão", "Digital Multirrelacionado") else 0.001)
            tx_count = int(max(1, rng.normal(base_tx * seasonality * trend, max(3, base_tx * .10))))
            inflow = _positive_normal(rng, income * p["inflow_mult"] * trend, income * .13)
            outflow = _positive_normal(rng, income * p["outflow_mult"] * seasonality, income * .12)
            digital_share = float(np.clip(rng.normal(*p["digital_share"]), 0.02, 1))
            app_logins = int(max(0, rng.normal(*p["app"])))
            branch_visits = int(max(0, round(rng.normal(*p["branch"]))))
            rows.append({
                "customer_id": customer_id,
                "month": month.strftime("%Y-%m-%d"),
                "transaction_count": tx_count,
                "total_inflow": round(inflow * customer_factor, 2),
                "total_outflow": round(outflow * customer_factor, 2),
                "pix_count": int(round(tx_count * digital_share * rng.uniform(.40, .65))),
                "card_spend": round(outflow * float(customer["credit_utilization"]) * rng.uniform(.38, .62), 2),
                "cash_withdrawals": int(max(0, round(tx_count * (1 - digital_share) * rng.uniform(.08, .20)))),
                "app_logins": app_logins,
                "branch_visits": branch_visits,
                "digital_transaction_share": round(digital_share, 4),
            })
    return pd.DataFrame(rows)


def generate_and_save(n_customers: int = N_CUSTOMERS, months: int = N_MONTHS) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_directories()
    customers = generate_customers(n_customers=n_customers)
    activity = generate_monthly_activity(customers, months=months)
    customers.to_csv(DATA_RAW_DIR / "customers.csv", index=False)
    activity.to_csv(DATA_RAW_DIR / "monthly_activity.csv", index=False)
    return customers, activity


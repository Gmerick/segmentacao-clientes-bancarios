from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MODEL_DIR = ROOT_DIR / "models"

RANDOM_SEED = 42
N_CUSTOMERS = 8_000
N_MONTHS = 12
SELECTED_K = 5

PROFILE_WEIGHTS = {
    "Alta Renda Investidor": 0.14,
    "Digital Multirrelacionado": 0.24,
    "Crédito Intensivo": 0.19,
    "Tradicional Essencial": 0.23,
    "Jovem em Ascensão": 0.20,
}

CLUSTER_FEATURES = [
    "age",
    "monthly_income",
    "tenure_months",
    "product_count",
    "checking_balance",
    "savings_balance",
    "investment_balance",
    "credit_card_limit",
    "credit_utilization",
    "loan_balance",
    "delinquency_events_12m",
    "avg_monthly_transactions",
    "avg_monthly_outflow",
    "avg_monthly_inflow",
    "avg_app_logins",
    "avg_branch_visits",
    "digital_transaction_share",
    "movement_volatility",
]


def ensure_directories() -> None:
    for path in (DATA_RAW_DIR, DATA_PROCESSED_DIR, REPORTS_DIR, FIGURES_DIR, MODEL_DIR):
        path.mkdir(parents=True, exist_ok=True)


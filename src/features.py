"""Engenharia de atributos comportamentais no nível de cliente."""

from __future__ import annotations

import numpy as np
import pandas as pd

PRODUCT_COLUMNS = [
    "has_credit_card", "has_savings", "has_investments", "has_personal_loan", "has_insurance", "has_mortgage"
]


def build_customer_features(customers: pd.DataFrame, activity: pd.DataFrame) -> pd.DataFrame:
    monthly = activity.copy()
    monthly["month"] = pd.to_datetime(monthly["month"])
    agg = monthly.groupby("customer_id").agg(
        avg_monthly_transactions=("transaction_count", "mean"),
        total_transactions_12m=("transaction_count", "sum"),
        avg_monthly_inflow=("total_inflow", "mean"),
        avg_monthly_outflow=("total_outflow", "mean"),
        total_inflow_12m=("total_inflow", "sum"),
        total_outflow_12m=("total_outflow", "sum"),
        outflow_std=("total_outflow", "std"),
        avg_card_spend=("card_spend", "mean"),
        avg_pix_count=("pix_count", "mean"),
        avg_cash_withdrawals=("cash_withdrawals", "mean"),
        avg_app_logins=("app_logins", "mean"),
        avg_branch_visits=("branch_visits", "mean"),
        digital_transaction_share=("digital_transaction_share", "mean"),
    ).reset_index()

    features = customers.merge(agg, on="customer_id", how="inner", validate="one_to_one")
    features["product_count"] = features[PRODUCT_COLUMNS].sum(axis=1)
    features["asset_total"] = features[["checking_balance", "savings_balance", "investment_balance"]].sum(axis=1, min_count=1)
    features["credit_exposure"] = features["loan_balance"] + features["credit_card_limit"].fillna(0) * features["credit_utilization"]
    features["savings_rate"] = (features["total_inflow_12m"] - features["total_outflow_12m"]) / features["total_inflow_12m"].replace(0, np.nan)
    features["avg_ticket"] = features["total_outflow_12m"] / features["total_transactions_12m"].replace(0, np.nan)
    features["movement_volatility"] = features["outflow_std"] / features["avg_monthly_outflow"].replace(0, np.nan)
    features["relationship_value"] = features["asset_total"].fillna(0) + features["credit_exposure"] * .25
    return features


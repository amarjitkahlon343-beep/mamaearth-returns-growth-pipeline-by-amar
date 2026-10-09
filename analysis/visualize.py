#!/usr/bin/env python3
# ============================================================
# Author      : Amarjit Kahlon
# Project     : Mamaearth Returns & Growth Intelligence Pipeline
# Description : Generate required visualizations
# ============================================================

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "visualizations"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    cleaned_path = DATA_DIR / "orders_cleaned.csv"
    if not cleaned_path.exists():
        raise SystemExit(f"Missing {cleaned_path}. Run analysis/clean_and_eda.py first.")

    df = pd.read_csv(cleaned_path)
    df["order_date"] = pd.to_datetime(df["order_date"])

    # Chart 1: Return rate by payment method
    rates = (
        df.groupby("payment_method")["returned"]
        .mean()
        .mul(100)
        .round(1)
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(rates.index.astype(str), rates.values, color=["#E45756", "#F58518", "#4C78A8"])
    for bar, val in zip(bars, rates.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{val}%", ha="center")
    ax.set_ylabel("Return Rate (%)")
    ax.set_xlabel("Payment Method")
    ax.set_title("COD Returns at 44.4% — Nearly 3× Higher than Card")
    ax.set_ylim(0, max(rates.values) * 1.25)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "return_rate_by_payment.png", dpi=120)
    plt.close(fig)
    print(f"Saved → {OUT_DIR / 'return_rate_by_payment.png'}")

    # Chart 2: Outlier-corrected monthly revenue trend
    df["is_outlier"] = df["is_outlier"].astype(bool)
    clean_df = df.loc[~df["is_outlier"]].copy()
    clean_df["year_month"] = clean_df["order_date"].dt.to_period("M").astype(str)
    monthly = clean_df.groupby("year_month")["order_value"].sum().round(2)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly.index, monthly.values, marker="o", color="#4C78A8", linewidth=2)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (INR)")
    ax.set_title("Outlier-Corrected Monthly Revenue — Peak Month: March 2026 (₹20,318.90)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "monthly_revenue_trend.png", dpi=120)
    plt.close(fig)
    print(f"Saved → {OUT_DIR / 'monthly_revenue_trend.png'}")


if __name__ == "__main__":
    main()

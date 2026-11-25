#!/usr/bin/env python3
"""Analyze a small retail sales dataset: monthly revenue, top products,
and category breakdown. Saves charts to ./output/.

The script generates a reproducible synthetic dataset by default so it runs
anywhere; pass --csv to analyze your own file with the same columns
(date, product, category, units, unit_price).
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_sample_data(rows: int = 1000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    products = {
        "Sensor module": ("electronics", 24.99),
        "Relay board": ("electronics", 9.50),
        "USB cable": ("accessories", 4.99),
        "Power adapter": ("accessories", 12.99),
        "Enclosure box": ("hardware", 7.25),
        "Jumper wires": ("hardware", 3.49),
    }
    names = list(products)
    dates = pd.date_range("2026-01-01", "2026-10-31", freq="D")
    df = pd.DataFrame({
        "date": rng.choice(dates, rows),
        "product": rng.choice(names, rows),
        "units": rng.integers(1, 6, rows),
    })
    df["category"] = df["product"].map(lambda p: products[p][0])
    df["unit_price"] = df["product"].map(lambda p: products[p][1])
    df["revenue"] = df["units"] * df["unit_price"]
    return df.sort_values("date").reset_index(drop=True)


def analyze(df: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(exist_ok=True)
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["revenue"] = df["units"] * df["unit_price"]

    monthly = df.set_index("date")["revenue"].resample("ME").sum()
    top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False)
    by_category = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

    print(f"rows: {len(df)}")
    print(f"total revenue: ${df['revenue'].sum():,.2f}")
    print(f"best month: {monthly.idxmax():%B %Y} (${monthly.max():,.2f})")
    print("\nrevenue by product:")
    print(top_products.to_string(float_format=lambda x: f"${x:,.2f}"))

    fig, axes = plt.subplots(3, 1, figsize=(9, 12), constrained_layout=True)
    monthly.plot(ax=axes[0], marker="o", title="Monthly revenue", ylabel="USD")
    top_products.plot.barh(ax=axes[1], title="Revenue by product")
    axes[1].invert_yaxis()
    by_category.plot.pie(ax=axes[2], title="Revenue share by category", autopct="%1.0f%%")
    fig.savefig(out_dir / "sales_summary.png", dpi=150)
    print(f"\ncharts saved to {out_dir / 'sales_summary.png'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Retail sales data analysis.")
    parser.add_argument("--csv", type=Path, help="Your own CSV (default: built-in sample data)")
    parser.add_argument("--out", type=Path, default=Path("output"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv) if args.csv else make_sample_data()
    analyze(df, args.out)


if __name__ == "__main__":
    main()

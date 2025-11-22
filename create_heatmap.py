#!/usr/bin/env python3
"""Create a heatmap image from an Excel file.

Uses the first column as the index (row labels) and the `Risk_Score` column as values.
Saves a PNG image `output_with_population_elec_risk_heatmap.png` in the same folder.

Usage:
    python create_heatmap.py --input output_with_population_elec.xlsx
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_heatmap(input_path: str, output_image: Optional[str] = None) -> str:
    if output_image is None:
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_image = f"{base}_risk_heatmap.png"

    # Read Excel
    try:
        df = pd.read_excel(input_path, engine="openpyxl")
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file: {e}")

    # Handle multiple sheets
    if isinstance(df, dict):
        df = next(iter(df.values()))

    if df.shape[1] < 1:
        raise ValueError("Input Excel must have at least one column")

    first_col = df.columns[0]

    if "Risk_Score" not in df.columns:
        raise ValueError("Input Excel does not contain a 'Risk_Score' column")

    # Prepare data: index = first column, values = Risk_Score
    heat_df = df[[first_col, "Risk_Score"]].copy()
    heat_df[first_col] = heat_df[first_col].astype(str)
    heat_df["Risk_Score"] = pd.to_numeric(heat_df["Risk_Score"], errors="coerce")

    # Sort by Risk_Score for nicer visualization
    heat_df = heat_df.sort_values(by="Risk_Score", ascending=False).set_index(first_col)

    # Convert to 2D array (n x 1) for heatmap
    data = heat_df["Risk_Score"].to_numpy().reshape(-1, 1)

    plt.figure(figsize=(6, max(6, len(heat_df) * 0.12)))
    sns.set_theme(style="whitegrid")
    ax = sns.heatmap(
        data,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        yticklabels=heat_df.index,
        cbar_kws={"label": "Risk_Score"},
        linewidths=0.5,
        linecolor="gray",
    )

    ax.set_xticks([0.5])
    ax.set_xticklabels(["Risk_Score"])
    ax.set_xlabel("")
    ax.set_ylabel("")

    plt.tight_layout()
    plt.savefig(output_image, dpi=200)
    plt.close()
    return output_image


def main():
    parser = argparse.ArgumentParser(description="Create heatmap from Excel Risk_Score column")
    parser.add_argument("--input", "-i", required=True, help="Input Excel file path")
    parser.add_argument("--output", "-o", default=None, help="Output image path (PNG)")
    args = parser.parse_args()

    out = create_heatmap(args.input, args.output)
    print(f"Wrote heatmap image: {out}")


if __name__ == "__main__":
    main()

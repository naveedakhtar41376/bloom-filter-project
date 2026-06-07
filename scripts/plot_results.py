"""Create plots from benchmark and experiment CSV files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import pandas as pd


def plot_benchmarks(results_dir: Path, figures_dir: Path) -> None:
    path = results_dir / "benchmark_results.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)

    plt.figure()
    for data_type, group in df.groupby("data_type") if "data_type" in df.columns else [("benchmark", df)]:
        plt.plot(group["n"], group["insert_time_seconds"], marker="o", label=str(data_type))
    plt.xlabel("Number of inserted items")
    plt.ylabel("Insertion time (seconds)")
    plt.title("Bloom filter insertion time")
    plt.xscale("log")
    if "data_type" in df.columns:
        plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "insert_time_plot.png", dpi=300)
    plt.close()

    plt.figure()
    plt.plot(df["n"], df["positive_search_time_seconds"], marker="o", label="Inserted items")
    plt.plot(df["n"], df["negative_search_time_seconds"], marker="o", label="Unseen items")
    plt.xlabel("Number of queried items")
    plt.ylabel("Search time (seconds)")
    plt.title("Bloom filter search time")
    plt.xscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "search_time_plot.png", dpi=300)
    plt.close()


def plot_false_positive(results_dir: Path, figures_dir: Path) -> None:
    path = results_dir / "false_positive_results.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)

    plt.figure()
    plt.plot(df["capacity_ratio"], df["empirical_fpr"], marker="o", label="Empirical FPR")
    plt.plot(df["capacity_ratio"], df["theoretical_fpr"], marker="o", label="Theoretical FPR")
    plt.axvline(1.0, linestyle="--", label="Designed capacity")
    plt.xlabel("Inserted items / expected items")
    plt.ylabel("False positive rate")
    plt.title("False positive rate as capacity is exceeded")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "false_positive_rate_plot.png", dpi=300)
    plt.close()

    plt.figure()
    plt.plot(df["capacity_ratio"], df["fill_ratio"], marker="o")
    plt.axvline(1.0, linestyle="--")
    plt.xlabel("Inserted items / expected items")
    plt.ylabel("Fraction of bits set to 1")
    plt.title("Bloom filter fill ratio")
    plt.tight_layout()
    plt.savefig(figures_dir / "fill_ratio_plot.png", dpi=300)
    plt.close()


def plot_compression(results_dir: Path, figures_dir: Path) -> None:
    path = results_dir / "compression_results.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)

    plt.figure()
    for fpr, group in df.groupby("target_fpr"):
        plt.plot(group["expected_items"], group["compression_rate"], marker="o", label=f"FPR={fpr}")
    plt.xlabel("Expected number of items")
    plt.ylabel("Compression rate: Python set bytes / Bloom filter bytes")
    plt.title("Compression rate by capacity and target FPR")
    plt.xscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "compression_rate_plot.png", dpi=300)
    plt.close()


def plot_hash_distribution(results_dir: Path, figures_dir: Path) -> None:
    path = results_dir / "hash_distribution_results.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)

    plt.figure()
    plt.bar(df["data_type"], df["mean_absolute_relative_deviation"])
    plt.xlabel("Data type")
    plt.ylabel("Mean absolute relative bucket deviation")
    plt.title("Hash-position distribution diagnostic")
    plt.tight_layout()
    plt.savefig(figures_dir / "hash_distribution_plot.png", dpi=300)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=str, default="results")
    parser.add_argument("--figures-dir", type=str, default="figures")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    figures_dir = Path(args.figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    plot_benchmarks(results_dir, figures_dir)
    plot_false_positive(results_dir, figures_dir)
    plot_compression(results_dir, figures_dir)
    plot_hash_distribution(results_dir, figures_dir)
    print(f"Wrote figures to {figures_dir}")


if __name__ == "__main__":
    main()

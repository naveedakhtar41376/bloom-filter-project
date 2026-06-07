"""Validate that expected experiment output files and columns exist.

This script is useful before final submission. It does not judge the scientific
quality of the results; it checks that the reproducible output files have the
expected structure.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "benchmark_results.csv": {
        "data_type",
        "n",
        "false_positive_rate_target",
        "size_bits",
        "num_hashes",
        "memory_bytes",
        "insert_time_seconds",
        "positive_search_time_seconds",
        "negative_search_time_seconds",
        "insert_time_per_item",
        "positive_search_time_per_item",
        "negative_search_time_per_item",
    },
    "false_positive_results.csv": {
        "data_type",
        "expected_items",
        "inserted_items",
        "capacity_ratio",
        "target_fpr",
        "query_count",
        "false_positive_count",
        "empirical_fpr",
        "theoretical_fpr",
        "fill_ratio",
        "size_bits",
        "num_hashes",
    },
    "compression_results.csv": {
        "expected_items",
        "target_fpr",
        "bloom_size_bits",
        "bloom_memory_bytes",
        "bits_per_expected_item",
        "approx_python_set_bytes",
        "compression_rate",
        "num_hashes",
    },
    "hash_distribution_results.csv": {
        "data_type",
        "sample_size",
        "size_bits",
        "num_hashes",
        "buckets",
        "total_positions",
        "expected_per_bucket",
        "mean_absolute_relative_deviation",
        "max_absolute_relative_deviation",
        "empty_buckets",
    },
}


def validate_file(results_dir: Path, filename: str, required_columns: set[str]) -> list[str]:
    errors: list[str] = []
    path = results_dir / filename
    if not path.exists():
        return [f"Missing file: {path}"]

    df = pd.read_csv(path)
    missing = required_columns - set(df.columns)
    if missing:
        errors.append(f"{filename}: missing columns {sorted(missing)}")
    if df.empty:
        errors.append(f"{filename}: file has no rows")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=str, default="results")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    all_errors: list[str] = []
    for filename, required_columns in REQUIRED_COLUMNS.items():
        all_errors.extend(validate_file(results_dir, filename, required_columns))

    if all_errors:
        print("Validation failed:")
        for error in all_errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("All expected result files and columns are present.")


if __name__ == "__main__":
    main()

"""Evaluate whether the hash-family positions are reasonably distributed.

The assignment explicitly asks that the hash functions be tested, and that they
be tested on at least two data types. This script summarizes the distribution of
hash positions for word-like strings, DNA strings, and random strings.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bloomfilter.hash_functions import hash_positions
from scripts.data_generation import generate_dataset


def bucket_summary(items: list[str], *, size: int, num_hashes: int, buckets: int) -> dict:
    counts = Counter()
    total_positions = 0
    duplicate_position_items = 0

    for item in items:
        positions = hash_positions(item, num_hashes=num_hashes, size=size)
        total_positions += len(positions)
        if len(set(positions)) < len(positions):
            duplicate_position_items += 1
        for pos in positions:
            bucket = min((pos * buckets) // size, buckets - 1)
            counts[bucket] += 1

    expected_per_bucket = total_positions / buckets
    bucket_counts = [counts[bucket] for bucket in range(buckets)]
    max_bucket_count = max(bucket_counts) if bucket_counts else 0
    min_bucket_count = min(bucket_counts) if bucket_counts else 0
    empty_buckets = sum(1 for value in bucket_counts if value == 0)
    relative_deviations = [
        abs(value - expected_per_bucket) / expected_per_bucket for value in bucket_counts
    ]
    mean_absolute_relative_deviation = sum(relative_deviations) / buckets
    max_absolute_relative_deviation = max(relative_deviations) if relative_deviations else 0

    return {
        "sample_size": len(items),
        "size_bits": size,
        "num_hashes": num_hashes,
        "buckets": buckets,
        "total_positions": total_positions,
        "unique_positions": len(set().union(*(set(hash_positions(item, num_hashes, size)) for item in items))),
        "items_with_duplicate_positions": duplicate_position_items,
        "min_bucket_count": min_bucket_count,
        "max_bucket_count": max_bucket_count,
        "expected_per_bucket": expected_per_bucket,
        "empty_buckets": empty_buckets,
        "mean_absolute_relative_deviation": mean_absolute_relative_deviation,
        "max_absolute_relative_deviation": max_absolute_relative_deviation,
    }


def run_experiment(output: str, sample_size: int, size: int, num_hashes: int, buckets: int) -> None:
    rows = []
    for data_type in ["words", "dna", "random"]:
        items = generate_dataset(data_type, sample_size, seed=42, prefix="hash_test")
        row = bucket_summary(items, size=size, num_hashes=num_hashes, buckets=buckets)
        row["data_type"] = data_type
        rows.append(row)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        fieldnames = ["data_type"] + [key for key in rows[0] if key != "data_type"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote hash distribution results to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=10000)
    parser.add_argument("--size", type=int, default=100000)
    parser.add_argument("--num-hashes", type=int, default=7)
    parser.add_argument("--buckets", type=int, default=100)
    parser.add_argument("--output", type=str, default="results/hash_distribution_results.csv")
    args = parser.parse_args()
    run_experiment(args.output, args.sample_size, args.size, args.num_hashes, args.buckets)


if __name__ == "__main__":
    main()

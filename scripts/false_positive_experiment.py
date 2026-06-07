"""Measure empirical false-positive rate as inserted items increase.

This script directly addresses the project requirement to study how the false
positive rate changes as the Bloom filter is filled and overfilled.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bloomfilter import BloomFilter
from scripts.data_generation import generate_dataset


def empirical_false_positive_rate(bf: BloomFilter, unseen_items: list[str]) -> tuple[float, int]:
    false_positives = sum(1 for item in unseen_items if item in bf)
    return false_positives / len(unseen_items), false_positives


def run_experiment(
    expected_items: int,
    target_fpr: float,
    output: str,
    data_type: str,
    query_count: int,
) -> None:
    if expected_items <= 0:
        raise ValueError("expected_items must be positive")
    if not 0 < target_fpr < 1:
        raise ValueError("target_fpr must be between 0 and 1")
    if query_count <= 0:
        raise ValueError("query_count must be positive")

    max_capacity_factor = 3.0
    inserted_pool = generate_dataset(data_type, int(expected_items * max_capacity_factor), seed=42, prefix="inserted")
    unseen_items = generate_dataset(data_type, query_count, seed=12345, prefix="unseen")

    inserted_counts = [
        int(expected_items * factor)
        for factor in [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]
    ]

    rows = []
    for count in inserted_counts:
        bf = BloomFilter(expected_items=expected_items, false_positive_rate=target_fpr)
        for item in inserted_pool[:count]:
            bf.add(item)

        empirical_fpr, false_positive_count = empirical_false_positive_rate(bf, unseen_items)
        rows.append(
            {
                "data_type": data_type,
                "expected_items": expected_items,
                "inserted_items": count,
                "capacity_ratio": count / expected_items,
                "target_fpr": target_fpr,
                "query_count": query_count,
                "false_positive_count": false_positive_count,
                "empirical_fpr": empirical_fpr,
                "theoretical_fpr": bf.theoretical_false_positive_rate(),
                "fill_ratio": bf.fill_ratio(),
                "size_bits": bf.size,
                "num_hashes": bf.num_hashes,
            }
        )

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote false positive results to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-items", type=int, default=100000)
    parser.add_argument("--fpr", type=float, default=0.01)
    parser.add_argument("--data-type", choices=["words", "dna", "random"], default="words")
    parser.add_argument("--query-count", type=int, default=50000)
    parser.add_argument("--output", type=str, default="results/false_positive_results.csv")
    args = parser.parse_args()
    run_experiment(args.expected_items, args.fpr, args.output, args.data_type, args.query_count)


if __name__ == "__main__":
    main()

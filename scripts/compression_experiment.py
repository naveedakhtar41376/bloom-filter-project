"""Compute Bloom filter compression rates for several design choices."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from bloomfilter import BloomFilter
from scripts.data_generation import generate_words


def approximate_python_set_size(items) -> int:
    """Approximate memory used by a Python set and its string elements."""
    item_set = set(items)
    return sys.getsizeof(item_set) + sum(sys.getsizeof(item) for item in item_set)


def run_experiment(output: str) -> None:
    expected_items_values = [10000, 50000, 100000, 500000, 1000000]
    fpr_values = [0.1, 0.05, 0.01, 0.001]

    rows = []
    for expected_items in expected_items_values:
        sample_items = generate_words(expected_items)
        original_size_bytes = approximate_python_set_size(sample_items)

        for target_fpr in fpr_values:
            bf = BloomFilter(expected_items=expected_items, false_positive_rate=target_fpr)
            rows.append(
                {
                    "expected_items": expected_items,
                    "target_fpr": target_fpr,
                    "bloom_size_bits": bf.size,
                    "bloom_memory_bytes": bf.memory_bytes,
                    "bits_per_expected_item": bf.size / expected_items,
                    "approx_python_set_bytes": original_size_bytes,
                    "compression_rate": original_size_bytes / bf.memory_bytes,
                    "num_hashes": bf.num_hashes,
                }
            )

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote compression results to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="results/compression_results.csv")
    args = parser.parse_args()
    run_experiment(args.output)


if __name__ == "__main__":
    main()

"""Benchmark insertion and search time for the Bloom filter.

Example:
    python scripts/benchmark_bloom_filter.py --max-n 100000 --data-type words \
        --output results/benchmark_results.csv
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bloomfilter import BloomFilter
from scripts.data_generation import generate_dataset


def _time_operation(operation, repeats: int) -> float:
    timings = []
    for _ in range(repeats):
        start = time.perf_counter()
        operation()
        timings.append(time.perf_counter() - start)
    return statistics.median(timings)


def benchmark(sizes: list[int], false_positive_rate: float, data_type: str, repeats: int) -> list[dict]:
    rows = []
    for n in sizes:
        inserted = generate_dataset(data_type, n, seed=42, prefix="inserted")
        unseen = generate_dataset(data_type, n, seed=12345, prefix="unseen")

        bf = BloomFilter(expected_items=n, false_positive_rate=false_positive_rate)

        # Insertion modifies the filter, so it must be timed on a fresh object for
        # each repeat. The median is more stable than a single timing.
        insert_timings = []
        for _ in range(repeats):
            trial_bf = BloomFilter(expected_items=n, false_positive_rate=false_positive_rate)
            start = time.perf_counter()
            for item in inserted:
                trial_bf.add(item)
            insert_timings.append(time.perf_counter() - start)
        insert_time = statistics.median(insert_timings)

        for item in inserted:
            bf.add(item)

        positive_search_time = _time_operation(lambda: sum(1 for item in inserted if item in bf), repeats)
        negative_search_time = _time_operation(lambda: sum(1 for item in unseen if item in bf), repeats)

        rows.append(
            {
                "data_type": data_type,
                "n": n,
                "false_positive_rate_target": false_positive_rate,
                "size_bits": bf.size,
                "num_hashes": bf.num_hashes,
                "memory_bytes": bf.memory_bytes,
                "insert_time_seconds": insert_time,
                "positive_search_time_seconds": positive_search_time,
                "negative_search_time_seconds": negative_search_time,
                "insert_time_per_item": insert_time / n,
                "positive_search_time_per_item": positive_search_time / n,
                "negative_search_time_per_item": negative_search_time / n,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=100000)
    parser.add_argument("--sizes", type=str, default=None, help="Optional comma-separated benchmark sizes, e.g. 1000,5000,10000")
    parser.add_argument("--fpr", type=float, default=0.01)
    parser.add_argument("--data-type", choices=["words", "dna", "random"], default="words")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=str, default="results/benchmark_results.csv")
    args = parser.parse_args()

    if args.repeats <= 0:
        raise ValueError("--repeats must be positive")

    if args.sizes:
        sizes = [int(value.strip()) for value in args.sizes.split(",") if value.strip()]
        if any(n <= 0 for n in sizes):
            raise ValueError("--sizes must contain positive integers")
    else:
        candidate_sizes = [1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
        sizes = [n for n in candidate_sizes if n <= args.max_n]
    if not sizes:
        raise ValueError("--max-n is smaller than the smallest benchmark size of 1000")

    rows = benchmark(sizes, args.fpr, args.data_type, args.repeats)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote benchmark results to {output_path}")


if __name__ == "__main__":
    main()

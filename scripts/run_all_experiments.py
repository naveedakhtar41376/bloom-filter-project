"""Run the full local experiment pipeline.

This convenience script is useful before submission because it regenerates all
CSV files, recreates the figures, and validates that the expected outputs exist.
For the final project, the same commands should also be run on HPC with larger
settings through ``hpc/benchmark_job.sh``.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_command(command: list[str]) -> None:
    print("\n$ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=100000)
    parser.add_argument("--expected-items", type=int, default=100000)
    parser.add_argument("--query-count", type=int, default=50000)
    parser.add_argument("--data-type", choices=["words", "dna", "random"], default="words")
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()

    py = sys.executable
    run_command([py, "scripts/benchmark_bloom_filter.py", "--max-n", str(args.max_n), "--data-type", args.data_type, "--repeats", str(args.repeats), "--output", "results/benchmark_results.csv"])
    run_command([py, "scripts/hash_distribution_experiment.py", "--sample-size", "10000", "--output", "results/hash_distribution_results.csv"])
    run_command([py, "scripts/false_positive_experiment.py", "--expected-items", str(args.expected_items), "--data-type", args.data_type, "--query-count", str(args.query_count), "--output", "results/false_positive_results.csv"])
    run_command([py, "scripts/compression_experiment.py", "--output", "results/compression_results.csv"])
    run_command([py, "scripts/plot_results.py", "--results-dir", "results", "--figures-dir", "figures"])
    run_command([py, "scripts/validate_results.py", "--results-dir", "results"])


if __name__ == "__main__":
    main()

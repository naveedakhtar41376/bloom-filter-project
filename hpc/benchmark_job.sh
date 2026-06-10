#!/bin/bash
#SBATCH --job-name=bloom_filter_benchmark
#SBATCH --output=results/hpc_benchmark_%j.out
#SBATCH --error=results/hpc_benchmark_%j.err
#SBATCH --time=00:45:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1

source "$VSC_DATA"/miniconda3/etc/profile.d/conda.sh
conda activate bloom-filter-project

set -euo pipefail

mkdir -p results figures

python scripts/benchmark_bloom_filter.py --max-n 1000000 --data-type words --repeats 3 --output results/benchmark_results.csv
python scripts/hash_distribution_experiment.py --sample-size 10000 --output results/hash_distribution_results.csv
python scripts/false_positive_experiment.py --expected-items 100000 --fpr 0.01 --data-type words --query-count 50000 --output results/false_positive_results.csv
python scripts/compression_experiment.py --output results/compression_results.csv
python scripts/plot_results.py --results-dir results --figures-dir figures
python scripts/validate_results.py --results-dir results

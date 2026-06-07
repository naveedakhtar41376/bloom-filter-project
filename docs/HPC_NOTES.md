# HPC execution notes

The project requires performance benchmarks on HPC. The repository includes `hpc/benchmark_job.sh`, but the conda/module commands may need to be adapted to the exact university cluster.

## Recommended workflow

1. Push the repository to GitHub.
2. Clone it on the HPC login node.
3. Create or activate the conda environment.
4. Run a short test interactively if allowed:

```bash
python scripts/benchmark_bloom_filter.py --max-n 10000 --repeats 1
```

5. Submit the batch job:

```bash
sbatch hpc/benchmark_job.sh
```

6. After completion, check:

```bash
ls results
ls figures
```

7. Commit the final CSV outputs, plots, job script, and HPC log files if the course expects output evidence in the repository.

## Files that should exist after a full HPC run

```text
results/benchmark_results.csv
results/hash_distribution_results.csv
results/false_positive_results.csv
results/compression_results.csv
results/hpc_benchmark_<jobid>.out
results/hpc_benchmark_<jobid>.err
figures/insert_time_plot.png
figures/search_time_plot.png
figures/false_positive_rate_plot.png
figures/fill_ratio_plot.png
figures/compression_rate_plot.png
figures/hash_distribution_plot.png
```

## What to mention in the final README

Mention the actual maximum input size used on HPC, the data type used for the main benchmark, and whether the job completed successfully. If the HPC system required specific module commands, record them in the README.

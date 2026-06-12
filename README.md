# Bloom Filter Project

## Team members

- Team member 1: NIZAR ALI ARTAS
- Team member 2: NAVEED AKHTAR

## Project overview

This repository contains a Python implementation and empirical study of a Bloom filter for the Concepts of Data Science project. A Bloom filter is a probabilistic membership data structure: it can return false positives, but it should not return false negatives for items that have actually been inserted.

The repository is designed to satisfy the main project requirements:

- reusable Python module,
- clearly documented implementation,
- correctness tests,
- hash-function tests on multiple data types,
- insertion and search benchmarks,
- false-positive-rate experiment, including over-capacity behaviour,
- compression-rate experiment,
- HPC job script,
- reproducible CSV outputs and plots,
- README summary and GitHub collaboration evidence.

Additional guidance files are included in `docs/`, especially the experiment design, report template, interpretation notes, HPC notes, and final submission checklist.

## Repository structure

```text
bloomfilter/      Python package containing the BloomFilter implementation
scripts/          Benchmarking, experiment, plotting, validation, and data-generation scripts
tests/            Pytest-based correctness and validation tests
hpc/              HPC batch job script
docs/             Experiment-design notes, HPC notes, and report-writing template
results/          CSV results and HPC output files
figures/          Generated plots
notebooks/        Analysis notebook
```

## Installation

Using conda:

```bash
conda env create -f environment.yml
conda activate bloom-filter-project
```

Using pip:

```bash
pip install -r requirements.txt
```

## Basic usage

```python
from bloomfilter import BloomFilter

bf = BloomFilter(expected_items=100000, false_positive_rate=0.01)
bf.add("apple")

print("apple" in bf)   # True: inserted item is found
print("banana" in bf)  # False, unless it is a false positive
```

## Implementation summary

The implementation uses an object-oriented design. The main class is:

```python
BloomFilter(expected_items, false_positive_rate)
```

The bit-array size is computed as:

```text
m = -n ln(p) / (ln 2)^2
```

where `n` is the expected number of inserted items and `p` is the desired false-positive rate.

The number of hash functions is computed as:

```text
k = (m / n) ln(2)
```

The hash-function family uses double hashing:

```text
h_i(x) = (h1(x) + i h2(x)) mod m
```

where `h1` and `h2` are deterministic BLAKE2b-based hashes. Python's built-in `hash()` is intentionally not used because it is randomized across interpreter sessions.

## Running tests

From the repository root:

```bash
pytest
```

The tests check that:

- inserted items are found,
- no false negatives occur for tested inserted examples,
- words, DNA strings, random strings, integers, and tuples are accepted,
- hash positions are deterministic,
- hash positions are valid indices,
- invalid constructor and hash parameters are rejected,
- Bloom filter size matches the standard formula,
- memory usage is calculated consistently,
- data generators are reproducible.

Current local validation status should be regenerated before submission using:

```bash
pytest
```

## Running experiments locally

### 1. Insertion and search timing

```bash
python scripts/benchmark_bloom_filter.py \
  --max-n 100000 \
  --data-type words \
  --repeats 3 \
  --output results/benchmark_results.csv
```

### 2. Hash-distribution diagnostic

```bash
python scripts/hash_distribution_experiment.py \
  --sample-size 10000 \
  --output results/hash_distribution_results.csv
```

This tests the hash-position distribution for word-like strings, DNA strings, and random strings.

### 3. False-positive-rate experiment

```bash
python scripts/false_positive_experiment.py \
  --expected-items 100000 \
  --fpr 0.01 \
  --data-type words \
  --query-count 50000 \
  --output results/false_positive_results.csv
```

This experiment tests both normal capacity and over-capacity cases.

### 4. Compression-rate experiment

```bash
python scripts/compression_experiment.py \
  --output results/compression_results.csv
```

### 5. Run the full local pipeline

```bash
python scripts/run_all_experiments.py \
  --max-n 100000 \
  --expected-items 100000 \
  --query-count 50000 \
  --data-type words \
  --repeats 3
```

This command regenerates benchmark results, hash diagnostics, false-positive results, compression results, figures, and then validates the result files.

### 6. Generate plots only

```bash
python scripts/plot_results.py \
  --results-dir results \
  --figures-dir figures
```

### 7. Validate result files before submission

```bash
python scripts/validate_results.py --results-dir results
```

This checks that the expected CSV files exist and contain the required columns.

## Important interpretation notes

The Bloom filter stores membership information approximately. A positive query result means that the item is possibly present; a negative query result means that the item is definitely absent, assuming the same encoding and hashing procedure is used.

The false-positive experiment intentionally includes over-capacity cases. The expected pattern is that empirical false positives remain near the target rate around the design capacity, but increase once the filter is substantially overfilled.

The compression experiment compares the memory used by the Bloom filter's bytearray with an approximate Python set representation. This gives a practical memory-saving comparison, not a universal compression ratio for all possible storage systems.

See `docs/LIMITATIONS_AND_INTERPRETATION.md` for more details.

## Running on HPC

Submit the job script from the repository root:

```bash
sbatch hpc/benchmark_job.sh
```

The exact conda activation commands may need to be adapted to the VSC/HPC system. The job script is intentionally separated from the Python scripts so that the same experiments can be run locally and on HPC.

For the final submission, local results are useful for development, but the main benchmark evidence should come from the HPC run because the project description explicitly asks for HPC benchmarking.

Expected HPC outputs:

```text
results/hpc_benchmark_<jobid>.out
results/hpc_benchmark_<jobid>.err
results/benchmark_results.csv
results/hash_distribution_results.csv
results/false_positive_results.csv
results/compression_results.csv
figures/*.png
```

## Complexity discussion

Let:

- `n` be the expected number of inserted items,
- `m` be the number of bits in the Bloom filter,
- `k` be the number of hash functions.

Insertion computes `k` hash positions and sets `k` bits, so insertion time is `O(k)`. Search computes the same `k` hash positions and checks `k` bits, so search time is also `O(k)`.

For a fixed configured Bloom filter, `k` is fixed and usually small. Therefore, insertion and search behave as approximately constant-time operations in practice, while the total time for inserting or querying many items scales linearly with the number of operations.

The space complexity is `O(m)`. Since:

```text
m = -n ln(p) / (ln 2)^2
```

space grows linearly with the expected number of inserted items for a fixed target false-positive rate.


## Conclusions

### False-positive-rate experiment
In the false positive rate experiment, the bloom filter has shown its anticipated behavior. For the filter, it was configured for 100000 expected items and the false positive target rate was 0.01, with every measurement using 50000 membership queries. It was observed that the empirical false-positive rate stayed pretty low as long as the number of inserted items were lower than designed capacity. For a capacity of 50%, the empirical false positive rate just around 0.00024, and at 75% capacity it was 0.00226. When the inserted items approached the designed capacity, the empirical false-positive rate was very close to the target value of 0.01, i.e. 0.00976. This justifies the expected behavior of bloom filter when it is used inside its proposed capacity.
When we increase the number of inserted items and exceed the design capacity, it is significantly effecting the reliability. Going from 1.00x to 1.25x capacity, the empirical false-positive rate increased to 0.02684; at 1.5x capacity, it increased to 0.05746; at 2x capacity, it increased to 0.15722; and at 3x capacity, it reached 0.43724. Another aspect which shows that the implementation follows the expected Bloom filter formula strictly is the behavior of empirical and theoretical curves which remain nearly identical during the experiment. As we inserted more items, the fill ratio also increased. It was 0.070 when the capacity was 10% and approximately 0.889 when the capacity was increased to 3x. From this pattern we can understand the rapid rise in false-positive rate once the filter becomes overfilled. Since majority bits are set to 1, so the unseen items are more likely to pass all hash checks. Therefore, the experiment shows that a Bloom filter must be sized according to the expected number of inserted items. If the filter is used far beyond its intended capacity, the false-positive rate becomes much higher than the target value. From the experiment it can be concluded that a bloom filter must be designed keeping in mind the expected number of items to be inserted. When the filter is overloaded beyond its actual capacity, the false-positive rate exceeds the target value. 

### Compression-rate experiment
In the compression rate experiment we compared the memory used by the Bloom filter with the estimated memory used by a Python set for different expected capacities ranging from 10,000 to 1,000,000 items, and tested target false-positive rates are 0.1, 0.05, 0.01, and 0.001. The compression rate experiment results show that the target false-positive rate has a direct effect on the size of the Bloom filter with higher target false-positive rate consuming fewer bits, while a lower target false-positive rate demanding more bits. For example, for a target false-positive rate of 0.1 the number of bits per expected item is about 4.79, for 0.05 it’s about 6.24, for 0.01 it’s about 9.59, and for 0.001 it’s about 14.38. Same pattern is observed for hash functions, as the target false-positive rate becomes stricter number of hash functions also increase: 3 hash functions for 0.1, 4 for 0.05, 7 for 0.01, and 10 for 0.001. The largest number of tested capacity of expected item was 1000000 for which the bloom filter consumed approximately 599,067 bytes at target false positive rate of 0.1, 779,404 bytes at target false positive rate of 0.05, 1,198,133 bytes at target false positive rate of 0.01, and 1,797,199 bytes at target false positive rate of 0.001. Compared to the Python set memory, the memory consumed was nearly 93,443,538 bytes for equal number of items. The compression rates are found to be approximately 156x, 120x, 78x, and 52x, respectively. 
From the above findings, we can see that the main advantage of bloom filter is that it can represent membership information using much less memory than an exact Python set. However, this compression comes with a trade-off. Low false-positive rate means the filter needs more memory and consequently more hash functions. A higher false-positive rate means the filter becomes smaller and faster to store, but at the expense of accuracy. What configuration we want to choose depends on the application.  Applications that operate under limited memory may prefer a higher false-positive rate, whereas critical-software applications should use a lower false-positive rate.


## Additional documentation

The `docs/` folder contains supporting material for the final submission:

- `EXPERIMENT_DESIGN.md`: explains what each experiment measures and how to interpret it.
- `REPORT_TEMPLATE.md`: gives a structured template for writing the final conclusions after the HPC run.
- `HPC_NOTES.md`: records practical notes for running and documenting the HPC benchmark.

The repository also includes `CONTRIBUTING.md` with commit-message and branch guidance.

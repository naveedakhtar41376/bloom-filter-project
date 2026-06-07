# Final submission checklist

Use this checklist before submitting the GitHub repository.

## Repository metadata

- [ ] The repository is visible to the lecturer, or access has been granted if private.
- [ ] Both team members are named in `README.md`.
- [ ] Both team members have meaningful commits.
- [ ] Commit messages describe real work, not only vague messages such as "update" or "final".

## Code quality

- [ ] The Bloom filter is implemented as an importable Python module.
- [ ] The core implementation is not hidden inside a notebook.
- [ ] Function and class names are readable.
- [ ] Invalid parameters raise clear errors.
- [ ] The code does not rely on Python's randomized built-in `hash()`.

## Testing

- [ ] `pytest` passes locally.
- [ ] Tests cover inserted items, absent items, invalid inputs, and edge cases.
- [ ] Tests cover the hash-function family.
- [ ] At least two data types are tested; this repository uses words, DNA strings, and random strings.

## Experiments

- [ ] Insert timing has been run for increasing input sizes.
- [ ] Search timing has been run for increasing input sizes.
- [ ] False-positive rate has been measured below, at, and above the designed capacity.
- [ ] Compression rate has been measured for multiple expected capacities and target false-positive rates.
- [ ] Hash-distribution diagnostics have been generated for multiple data types.

## HPC evidence

- [ ] The HPC job script is included.
- [ ] The benchmark was run on HPC, not only locally.
- [ ] HPC output files are included in `results/` or clearly referenced.
- [ ] The README explains how the HPC job was run.

## Results and interpretation

- [ ] CSV result files are included.
- [ ] Figures are included.
- [ ] The README summarizes the main conclusions.
- [ ] The analysis explains why false positives increase when the filter is overfilled.
- [ ] The analysis explains the trade-off between memory usage and false-positive probability.

## Reproducibility

- [ ] `requirements.txt` or `environment.yml` is included.
- [ ] Commands for tests and experiments are documented.
- [ ] `scripts/validate_results.py` passes.
- [ ] Temporary caches such as `__pycache__` and `.pytest_cache` are not committed.

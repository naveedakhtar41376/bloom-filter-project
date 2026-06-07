# Final review notes

This document summarizes the checks that were performed while preparing the repository for submission.

## Requirement coverage

| Project requirement | Repository evidence |
|---|---|
| Implement a Bloom filter | `bloomfilter/bloom_filter.py` |
| Use an object-oriented or functional approach | Object-oriented `BloomFilter` class |
| Make implementation usable as a module | `bloomfilter/` package with `__init__.py` |
| Test correctness thoroughly | `tests/` directory with pytest tests |
| Define and test a hash-function family | `bloomfilter/hash_functions.py`, `tests/test_hash_functions.py`, `scripts/hash_distribution_experiment.py` |
| Test at least two data types | Words, DNA strings, and random strings are supported |
| Discuss time and space complexity | `README.md` and `docs/REPORT_TEMPLATE.md` |
| Time insert and search functions for increasing input sizes | `scripts/benchmark_bloom_filter.py` |
| Create benchmark plots | `scripts/plot_results.py`, `figures/` |
| Run benchmarks on HPC | `hpc/benchmark_job.sh` |
| Include HPC job script and output | Job script included; final HPC outputs should be added after running on VSC/HPC |
| Study false positive rate as inserted items increase | `scripts/false_positive_experiment.py` |
| Study over-capacity behaviour | Same false-positive script includes capacity ratios above 1 |
| Study compression rate | `scripts/compression_experiment.py` |
| Document repository and conclusions | `README.md`; final conclusions should be updated after real HPC runs |
| Show GitHub collaboration | Requires actual commit history from both team members |

## Remaining manual work before final submission

1. Replace the placeholder team-member names in `README.md`.
2. Push the repository to GitHub.
3. Make sure both team members contribute visible commits.
4. Run the benchmark job on the HPC infrastructure.
5. Add the HPC output files to `results/`.
6. Replace sample/local conclusions with conclusions based on the HPC output.
7. Re-run:

```bash
pytest
python scripts/validate_results.py --results-dir results
```

8. Confirm that figures in `figures/` match the final CSV files.

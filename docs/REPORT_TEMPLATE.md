# Final report / README conclusion template

Use this template after running the full experiments on the HPC infrastructure.

## 1. Aim

The aim of this project was to implement, test, and benchmark a Bloom filter in Python. The implementation was designed as a reusable module and evaluated using correctness tests, hash-function diagnostics, timing benchmarks, false-positive-rate experiments, and compression-rate analysis.

## 2. Implementation summary

The Bloom filter was implemented using an object-oriented design. The filter computes the bit-array size from the expected number of inserted items and the target false-positive rate. The number of hash functions is also computed from the standard Bloom filter formula.

The implementation uses a compact `bytearray` for bit storage. The hash-function family is generated through double hashing using deterministic BLAKE2b-based base hashes. Python's built-in `hash()` was avoided because it is randomized across interpreter sessions.

## 3. Correctness results

The implementation passed the automated test suite. The most important correctness property is that inserted items are always found. The tests covered natural-language-style words, DNA strings, random strings, integers, and tuples.

Report the final test command and result here:

```text
pytest
...
```

## 4. Hash-function results

The hash-function diagnostics were run on word-like strings, DNA sequences, and random strings. The results should be summarized using `hash_distribution_results.csv` and `hash_distribution_plot.png`.

Suggested wording:

> The hash-position diagnostics did not show strong concentration for any of the tested data types. The results were broadly similar for word-like strings, DNA strings, and random strings, suggesting that the hash family is suitable for the tested inputs.

Adapt this wording if the final results show a visible difference.

## 5. Performance results

Use `benchmark_results.csv`, `insert_time_plot.png`, and `search_time_plot.png`.

Suggested wording:

> Total insertion and search time increased approximately linearly with the number of processed items. This agrees with the theoretical complexity: each operation uses a fixed number of hash functions for a configured Bloom filter, so processing many items scales approximately linearly in the number of operations.

## 6. False-positive-rate results

Use `false_positive_results.csv`, `false_positive_rate_plot.png`, and `fill_ratio_plot.png`.

Suggested wording:

> The empirical false-positive rate increased as more items were inserted. Around the designed capacity, the empirical rate was close to the theoretical value. When the filter was filled beyond its designed capacity, the false-positive rate increased substantially, confirming that the design capacity is an important practical parameter.

## 7. Compression-rate results

Use `compression_results.csv` and `compression_rate_plot.png`.

Suggested wording:

> The Bloom filter required substantially less memory than an approximate Python set representation. However, lower target false-positive rates required larger bit arrays. This confirms the expected trade-off: better accuracy requires more memory.

## 8. Limitations

The Bloom filter can return false positives. It also cannot recover the stored items and does not support ordinary deletion. Therefore, it is appropriate when memory-efficient approximate membership testing is needed, but not when exact membership or item retrieval is required.

## 9. Final conclusion

The project demonstrates that a Bloom filter provides memory-efficient approximate membership testing with predictable theoretical behaviour. The experiments confirmed the main trade-off between memory usage and false-positive probability, and showed why exceeding the designed capacity leads to degraded accuracy.

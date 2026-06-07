# Experiment design and interpretation notes

This document explains the reasoning behind the experiments in the repository. It is intended to make the final submission easier to defend academically.

## 1. Correctness experiments

The Bloom filter is probabilistic only for negative queries. Therefore, correctness is judged mainly by checking that inserted items are always reported as present. In other words, the implementation should have no false negatives for items that have been inserted.

The test suite checks:

- inserted words are found,
- inserted DNA strings are found,
- inserted random strings are found,
- duplicate insertions do not corrupt the filter,
- invalid constructor arguments are rejected,
- hash positions are deterministic and valid,
- the data generators are reproducible.

## 2. Hash-function diagnostics

The project requires a family of hash functions and asks that these hash functions are tested on at least two data types. This repository tests three data types:

- word-like tokens,
- DNA sequences,
- random alphanumeric strings.

The diagnostic script does not prove perfect uniformity. Instead, it gives an empirical check that the generated hash positions do not concentrate strongly in a small part of the bit array. The script divides the bit array into buckets and compares the number of assigned hash positions per bucket with the expected bucket count.

Important columns in `hash_distribution_results.csv`:

- `mean_absolute_relative_deviation`: average relative deviation from the expected bucket count.
- `max_absolute_relative_deviation`: largest relative bucket deviation.
- `empty_buckets`: number of buckets that received no hash positions.

For a reasonable hash family and enough samples, the three data types should show broadly similar diagnostics.

## 3. Timing benchmarks

The benchmark script measures insertion time and search time for increasing values of `n`. For each `n`, the Bloom filter is created with capacity `n`, then `n` items are inserted and queried.

The expected result is approximately linear growth in total time as `n` increases, because each individual insertion or query uses a fixed number of hash functions for that configured filter.

The script reports both total time and per-item time:

- `insert_time_seconds`
- `positive_search_time_seconds`
- `negative_search_time_seconds`
- `insert_time_per_item`
- `positive_search_time_per_item`
- `negative_search_time_per_item`

Median timing over repeated runs is used to reduce the influence of random short-term system noise.

## 4. False-positive-rate experiment

The false-positive experiment measures empirical false positives by inserting known items and querying separate unseen items.

The key comparison is between:

- `empirical_fpr`: measured from unseen queries,
- `theoretical_fpr`: calculated from the Bloom filter formula after the observed number of insertions.

The experiment includes capacity ratios below, equal to, and above 1.0. The over-capacity part is important because the project explicitly asks what happens when the number of inserted words exceeds the expected number of words.

Expected conclusion:

- near the designed capacity, the empirical false-positive rate should be close to the design target, allowing for sampling variability;
- above the designed capacity, the false-positive rate should increase because more bits are set to 1.

## 5. Compression experiment

The compression experiment compares approximate Python set memory with Bloom filter memory. This is not an exact universal memory comparison because Python object overhead depends on implementation details, but it is useful for showing the practical motivation of Bloom filters.

Expected conclusion:

- a Bloom filter uses much less memory than an exact Python set;
- a lower target false-positive rate requires more bits;
- increasing expected capacity increases Bloom filter memory approximately linearly.

## 6. Limitations to mention in the final README or report

A Bloom filter does not store the original items. It cannot list its contents and does not support exact deletion without using a different design such as a counting Bloom filter. The compression advantage comes at the cost of false positives.

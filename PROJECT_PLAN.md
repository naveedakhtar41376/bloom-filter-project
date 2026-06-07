# Detailed implementation plan

## Objective

Build, test, benchmark, and analyse a Bloom filter implementation in Python. The final repository should show both software-engineering quality and data-science experimentation.

## Phase 1: Core implementation

- Implement a reusable `BloomFilter` class.
- Compute optimal bit-array size from expected capacity and target false-positive rate.
- Compute optimal number of hash functions.
- Store bits compactly using `bytearray`.
- Implement `add`, `check`, and `__contains__`.
- Add theoretical false-positive-rate and fill-ratio methods.

## Phase 2: Hash-function family

- Use deterministic BLAKE2b hashes.
- Generate a family of hash positions by double hashing.
- Avoid Python's built-in `hash()` because it changes between interpreter sessions.
- Test hash positions for words, DNA strings, random strings, integers, and tuples.
- Add a hash-distribution experiment for words, DNA, and random strings.

## Phase 3: Correctness tests

- Test that inserted items are always found.
- Test that no false negatives occur in controlled examples.
- Test invalid input handling.
- Test deterministic hash positions.
- Test reproducible data generation.
- Run tests with `pytest` before every major commit.

## Phase 4: Experiments

### Benchmarking

Measure insertion and search time for increasing input sizes. Use median timing over repeated runs.

### False-positive rate

Measure empirical false-positive rate as a function of inserted item count. Include cases below, at, and above designed capacity.

### Compression rate

Compare approximate Python set memory with Bloom filter memory for several expected item counts and false-positive rates.

### Hash diagnostics

Compare hash-position distribution across words, DNA sequences, and random strings.

## Phase 5: HPC

- Use `hpc/benchmark_job.sh` to run full-scale experiments.
- Store output logs and CSV results in `results/`.
- Store generated plots in `figures/`.
- Mention any HPC-specific environment commands in the README.

## Phase 6: Final write-up

The README should include:

- project overview,
- team-member names,
- installation instructions,
- usage example,
- testing instructions,
- HPC instructions,
- complexity discussion,
- experiment conclusions,
- final submission checklist.

## Phase 7: GitHub collaboration

Each team member should commit meaningful parts of the project. The commit history should make contributions visible.

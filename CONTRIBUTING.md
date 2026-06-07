# Collaboration and commit guidance

Version control is part of the project grade, so both team members should make meaningful commits.

## Recommended branch workflow

```text
main
feature/core-bloom-filter
feature/hash-functions
feature/tests
feature/benchmarks
feature/hpc
feature/readme-analysis
```

## Good commit messages

```text
Implement BloomFilter bit-array storage
Add deterministic double-hashing utility
Add correctness tests for DNA sequences
Add false-positive-rate experiment script
Add HPC benchmark job script
Summarize compression-rate results in README
```

## Weak commit messages to avoid

```text
update
changes
fix
final
new stuff
```

## Practical rule

Each commit should describe one meaningful change. Avoid doing the whole project in one final commit because that makes collaboration invisible.

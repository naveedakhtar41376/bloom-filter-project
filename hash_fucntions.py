"""
Hash functions for the Bloom Filter project.

This module defines a family of hash functions using SHA_256 with different values of seed.
The goal is to generate k different hash positions for each input item.
"""


import hashlib

def _hash_with_seed(item: str, seed: int) -> int:
  combined = f"{seed}-{item}".encode("utf-8")
  digest = hashlib.sha256(combined).hexdigest()
  return int(digest, 16)


def generate_hashes(item: str, num_hashes: int, filter_size: int) -> list[int]:
  
    if num_hashes <= 0:
        raise ValueError("num_hashes must be greeter than zero.")

    if filter_size <= 0:
        raise ValueError("filter_zise must be greater than zero.")

    positions = []

    for seed in range(num_hashes):
        hash_value = _hash_with_seed(item, seed)
        position = hash_value % filter_size
        positions.append(position)

    return positions

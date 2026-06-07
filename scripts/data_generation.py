"""Utility functions for generating deterministic benchmark data.

The project requires testing with at least two data types. These utilities create
repeatable word-like strings, DNA sequences, and general random strings so that
benchmark runs can be reproduced locally and on HPC.
"""

from __future__ import annotations

import random
import string
from typing import Literal

DataType = Literal["words", "dna", "random"]


def generate_words(n: int, prefix: str = "word") -> list[str]:
    """Generate n deterministic word-like tokens."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return [f"{prefix}_{i}" for i in range(n)]


def generate_dna(n: int, length: int = 30, seed: int = 42) -> list[str]:
    """Generate n pseudo-random DNA sequences of fixed length."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if length <= 0:
        raise ValueError("length must be positive")
    rng = random.Random(seed)
    alphabet = "ACGT"
    return ["".join(rng.choice(alphabet) for _ in range(length)) for _ in range(n)]


def generate_random_strings(n: int, length: int = 20, seed: int = 42) -> list[str]:
    """Generate n pseudo-random alphanumeric strings."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if length <= 0:
        raise ValueError("length must be positive")
    rng = random.Random(seed)
    alphabet = string.ascii_letters + string.digits
    return ["".join(rng.choice(alphabet) for _ in range(length)) for _ in range(n)]


def generate_dataset(data_type: DataType, n: int, *, seed: int = 42, prefix: str = "item") -> list[str]:
    """Generate a named deterministic dataset.

    Parameters
    ----------
    data_type:
        One of "words", "dna", or "random".
    n:
        Number of items to generate.
    seed:
        Seed used for pseudo-random datasets.
    prefix:
        Prefix used only for word-like data.
    """
    if data_type == "words":
        return generate_words(n, prefix=prefix)
    if data_type == "dna":
        return generate_dna(n, seed=seed)
    if data_type == "random":
        return generate_random_strings(n, seed=seed)
    raise ValueError(f"unsupported data_type: {data_type}")

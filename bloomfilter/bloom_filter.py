"""Bloom filter implementation for the Concepts of Data Science project."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from bloomfilter.hash_functions import hash_positions


@dataclass(frozen=True)
class BloomFilterConfig:
    """Configuration parameters for a Bloom filter."""

    expected_items: int
    false_positive_rate: float
    size: int
    num_hashes: int


class BloomFilter:
    """A probabilistic membership data structure.

    A Bloom filter can return false positives, but it should never return false
    negatives for items that have actually been inserted.
    """

    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("false_positive_rate must be between 0 and 1")

        size = self._optimal_size(expected_items, false_positive_rate)
        num_hashes = self._optimal_num_hashes(size, expected_items)

        self.config = BloomFilterConfig(
            expected_items=expected_items,
            false_positive_rate=false_positive_rate,
            size=size,
            num_hashes=num_hashes,
        )
        self._bits = bytearray(math.ceil(size / 8))
        self.items_added = 0

    @staticmethod
    def _optimal_size(expected_items: int, false_positive_rate: float) -> int:
        """Return optimal number of bits for target capacity and error rate."""
        m = -(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)
        return max(1, math.ceil(m))

    @staticmethod
    def _optimal_num_hashes(size: int, expected_items: int) -> int:
        """Return optimal number of hash functions."""
        k = (size / expected_items) * math.log(2)
        return max(1, round(k))

    @property
    def size(self) -> int:
        """Number of bits in the Bloom filter."""
        return self.config.size

    @property
    def num_hashes(self) -> int:
        """Number of hash functions used by the Bloom filter."""
        return self.config.num_hashes

    @property
    def memory_bytes(self) -> int:
        """Memory used by the underlying bit array in bytes."""
        return len(self._bits)

    @property
    def bits_set(self) -> int:
        """Number of active bits currently set to 1.

        The bytearray may contain unused padding bits in the final byte, but
        those bits are never set by the Bloom filter because every hash position
        is reduced modulo ``self.size``.
        """
        return sum(byte.bit_count() for byte in self._bits)

    @property
    def load_factor(self) -> float:
        """Alias for the proportion of bits currently set to 1."""
        return self.fill_ratio()

    def _set_bit(self, position: int) -> None:
        byte_index, bit_index = divmod(position, 8)
        self._bits[byte_index] |= 1 << bit_index

    def _get_bit(self, position: int) -> bool:
        byte_index, bit_index = divmod(position, 8)
        return bool(self._bits[byte_index] & (1 << bit_index))

    def add(self, item: Any) -> None:
        """Insert an item into the Bloom filter."""
        for position in hash_positions(item, self.num_hashes, self.size):
            self._set_bit(position)
        self.items_added += 1

    def check(self, item: Any) -> bool:
        """Return True if item may be present and False if definitely absent."""
        return all(
            self._get_bit(position)
            for position in hash_positions(item, self.num_hashes, self.size)
        )

    def __contains__(self, item: Any) -> bool:
        return self.check(item)

    def theoretical_false_positive_rate(self) -> float:
        """Estimate false positive probability after current insertions."""
        k = self.num_hashes
        m = self.size
        n = self.items_added
        return (1 - math.exp(-(k * n) / m)) ** k

    def fill_ratio(self) -> float:
        """Return the proportion of bits currently set to 1."""
        return self.bits_set / self.size

    def compression_rate(self, original_size_bytes: int) -> float:
        """Return original_size_bytes divided by Bloom filter memory use."""
        if original_size_bytes <= 0:
            raise ValueError("original_size_bytes must be positive")
        return original_size_bytes / self.memory_bytes

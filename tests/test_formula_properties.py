import math

import pytest

from bloomfilter import BloomFilter


def test_optimal_size_matches_standard_formula():
    expected_items = 1000
    target_fpr = 0.01
    bf = BloomFilter(expected_items=expected_items, false_positive_rate=target_fpr)
    expected_size = math.ceil(-(expected_items * math.log(target_fpr)) / (math.log(2) ** 2))
    assert bf.size == expected_size


def test_memory_bytes_is_ceiling_of_bits_divided_by_eight():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    assert bf.memory_bytes == math.ceil(bf.size / 8)


def test_compression_rate_rejects_non_positive_original_size():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    with pytest.raises(ValueError):
        bf.compression_rate(0)

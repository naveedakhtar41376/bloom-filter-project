import pytest

from bloomfilter import BloomFilter


def test_bits_set_and_fill_ratio_start_at_zero():
    bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
    assert bf.bits_set == 0
    assert bf.fill_ratio() == 0
    assert bf.load_factor == 0


def test_bits_set_increases_after_insertion():
    bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
    before = bf.bits_set
    bf.add("apple")
    assert bf.bits_set > before
    assert 0 < bf.fill_ratio() <= 1
    assert bf.load_factor == bf.fill_ratio()


def test_theoretical_false_positive_rate_starts_at_zero():
    bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
    assert bf.theoretical_false_positive_rate() == pytest.approx(0.0)

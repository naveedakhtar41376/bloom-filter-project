import pytest

from bloomfilter import BloomFilter


def test_inserted_items_are_found():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    words = ["apple", "banana", "orange", "pear"]
    for word in words:
        bf.add(word)
    for word in words:
        assert word in bf


def test_no_false_negatives_for_dna_strings():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    dna_sequences = ["ACGTACGT", "TTCGGAAT", "GGGCCCATA", "ATATCGCG"]
    for seq in dna_sequences:
        bf.add(seq)
    assert all(seq in bf for seq in dna_sequences)


def test_empty_filter_returns_false_for_unseen_item():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    assert "not_inserted" not in bf


def test_duplicate_insertions_are_safe():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    bf.add("apple")
    bf.add("apple")
    assert "apple" in bf
    assert bf.items_added == 2


def test_invalid_constructor_arguments():
    with pytest.raises(ValueError):
        BloomFilter(expected_items=0, false_positive_rate=0.01)
    with pytest.raises(ValueError):
        BloomFilter(expected_items=100, false_positive_rate=0)
    with pytest.raises(ValueError):
        BloomFilter(expected_items=100, false_positive_rate=1)


def test_theoretical_false_positive_rate_increases_after_insertions():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    before = bf.theoretical_false_positive_rate()
    for i in range(200):
        bf.add(f"item_{i}")
    after = bf.theoretical_false_positive_rate()
    assert after > before


def test_fill_ratio_between_zero_and_one():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    for i in range(100):
        bf.add(f"item_{i}")
    assert 0 <= bf.fill_ratio() <= 1


def test_no_false_negatives_for_random_strings():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    random_strings = ["xQ91aa", "P0mm2z", "abc123", "ZZZ999"]
    for item in random_strings:
        bf.add(item)
    assert all(item in bf for item in random_strings)

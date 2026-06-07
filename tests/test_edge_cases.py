from bloomfilter import BloomFilter


def test_integer_items_can_be_inserted():
    bf = BloomFilter(expected_items=100, false_positive_rate=0.05)
    bf.add(123)
    assert 123 in bf


def test_tuple_items_can_be_inserted():
    bf = BloomFilter(expected_items=100, false_positive_rate=0.05)
    item = ("sample", 1)
    bf.add(item)
    assert item in bf

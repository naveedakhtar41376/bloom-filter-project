import pytest

from bloomfilter.hash_functions import hash_positions


def test_hash_positions_are_valid_indices():
    positions = hash_positions("apple", num_hashes=7, size=1000)
    assert len(positions) == 7
    assert all(0 <= pos < 1000 for pos in positions)


def test_hash_positions_are_deterministic():
    first = hash_positions("ACGTACGT", num_hashes=5, size=500)
    second = hash_positions("ACGTACGT", num_hashes=5, size=500)
    assert first == second


def test_hash_positions_work_for_multiple_data_types():
    examples = ["word", "ACGTACGT", 12345, ("gene", 7)]
    for item in examples:
        positions = hash_positions(item, num_hashes=4, size=256)
        assert len(positions) == 4
        assert all(0 <= pos < 256 for pos in positions)


@pytest.mark.parametrize("num_hashes,size", [(0, 100), (3, 0), (-1, 100), (3, -10)])
def test_hash_positions_reject_invalid_parameters(num_hashes, size):
    with pytest.raises(ValueError):
        hash_positions("x", num_hashes=num_hashes, size=size)

import pytest

from scripts.data_generation import generate_dataset, generate_dna, generate_random_strings, generate_words


def test_generate_words_is_deterministic():
    assert generate_words(3, prefix="x") == ["x_0", "x_1", "x_2"]


def test_random_generators_are_reproducible():
    assert generate_dna(5, seed=10) == generate_dna(5, seed=10)
    assert generate_random_strings(5, seed=10) == generate_random_strings(5, seed=10)


def test_generate_dataset_rejects_unknown_type():
    with pytest.raises(ValueError):
        generate_dataset("unknown", 10)

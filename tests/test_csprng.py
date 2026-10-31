import pytest

from cryptocore.csprng import generate_random_bytes


def test_generate_random_bytes_length():
    data = generate_random_bytes(16)

    assert isinstance(data, bytes)
    assert len(data) == 16


def test_generate_random_bytes_different_values():
    first = generate_random_bytes(16)
    second = generate_random_bytes(16)

    assert first != second


def test_generate_random_bytes_invalid_size():
    with pytest.raises(ValueError):
        generate_random_bytes(0)

    with pytest.raises(ValueError):
        generate_random_bytes(-1)


def test_key_uniqueness():
    keys = set()

    for _ in range(1000):
        key = generate_random_bytes(16)

        assert key not in keys

        keys.add(key)

    assert len(keys) == 1000


def test_basic_bit_distribution():
    data = generate_random_bytes(100_000)

    total_bits = len(data) * 8

    ones = sum(
        byte.bit_count()
        for byte in data
    )

    ratio = ones / total_bits

    assert 0.45 <= ratio <= 0.55
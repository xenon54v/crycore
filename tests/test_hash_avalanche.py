from cryptocore.hash.sha256 import SHA256
from cryptocore.hash.sha3_256 import SHA3_256


def count_different_bits(hash1: str, hash2: str) -> int:
    value1 = int(hash1, 16)
    value2 = int(hash2, 16)

    difference = value1 ^ value2

    return difference.bit_count()


def test_sha256_avalanche_effect():
    original = bytearray(b"CryptoCore avalanche test")
    modified = original.copy()

    modified[0] ^= 0b00000001

    hash1 = SHA256.hash(bytes(original))
    hash2 = SHA256.hash(bytes(modified))

    different_bits = count_different_bits(
        hash1,
        hash2
    )

    print(
        f"SHA-256 changed bits: "
        f"{different_bits}/256"
    )

    assert 100 < different_bits < 156


def test_sha3_256_avalanche_effect():
    original = bytearray(b"CryptoCore avalanche test")
    modified = original.copy()

    modified[0] ^= 0b00000001

    hash1 = SHA3_256.hash(bytes(original))
    hash2 = SHA3_256.hash(bytes(modified))

    different_bits = count_different_bits(
        hash1,
        hash2
    )

    print(
        f"SHA3-256 changed bits: "
        f"{different_bits}/256"
    )

    assert 100 < different_bits < 156
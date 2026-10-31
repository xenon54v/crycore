from cryptocore.hash.sha3_256 import SHA3_256


def test_sha3_256_empty():
    assert SHA3_256.hash(b"") == (
        "a7ffc6f8bf1ed76651c14756a061d662"
        "f580ff4de43b49fa82d80a4b80f8434a"
    )


def test_sha3_256_abc():
    assert SHA3_256.hash(b"abc") == (
        "3a985da74fe225b2045c172d6bd390bd"
        "855f086e3e9d525b46bfe24511431532"
    )


def test_sha3_256_multiple_updates():
    sha3 = SHA3_256()

    sha3.update(b"abc")
    sha3.update(b"def")
    sha3.update(b"ghi")

    assert sha3.hexdigest() == SHA3_256.hash(
        b"abcdefghi"
    )


def test_sha3_256_empty_updates():
    sha3 = SHA3_256()

    sha3.update(b"")
    sha3.update(b"")

    assert sha3.hexdigest() == SHA3_256.hash(b"")


def test_sha3_256_binary_data():
    data = bytes(range(256))

    result = SHA3_256.hash(data)

    assert len(result) == 64
    assert result == result.lower()


def test_sha3_256_partial_block():
    data = b"A" * 135

    result = SHA3_256.hash(data)

    assert len(result) == 64


def test_sha3_256_exact_rate_block():
    data = b"A" * 136

    result = SHA3_256.hash(data)

    assert len(result) == 64


def test_sha3_256_multiple_rate_blocks():
    data = b"A" * 500

    result = SHA3_256.hash(data)

    assert len(result) == 64
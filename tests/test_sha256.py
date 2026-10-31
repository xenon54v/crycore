from cryptocore.hash.sha256 import SHA256


def test_sha256_empty():
    assert SHA256.hash(b"") == (
        "e3b0c44298fc1c149afbf4c8996fb924"
        "27ae41e4649b934ca495991b7852b855"
    )


def test_sha256_abc():
    assert SHA256.hash(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )


def test_sha256_long_nist_vector():
    data = (
        b"abcdbcdecdefdefgefghfghighijhijk"
        b"ijkljklmklmnlmnomnopnopq"
    )

    assert SHA256.hash(data) == (
        "248d6a61d20638b8e5c026930c3e6039"
        "a33ce45964ff2167f6ecedd419db06c1"
    )


def test_sha256_multiple_updates():
    sha = SHA256()

    sha.update(b"abc")
    sha.update(b"def")
    sha.update(b"ghi")

    assert sha.hexdigest() == SHA256.hash(b"abcdefghi")


def test_sha256_binary_data():
    data = bytes(range(256))

    result = SHA256.hash(data)

    assert len(result) == 64
    assert result == result.lower()
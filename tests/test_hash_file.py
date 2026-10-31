import hashlib

import pytest

from cryptocore.hash.file_hash import hash_file


def test_hash_file_sha256(tmp_path):
    file_path = tmp_path / "test.bin"
    data = b"CryptoCore hash file test"

    file_path.write_bytes(data)

    result = hash_file(
        str(file_path),
        "sha256"
    )

    expected = hashlib.sha256(data).hexdigest()

    assert result == expected


def test_hash_file_sha3_256(tmp_path):
    file_path = tmp_path / "test.bin"
    data = b"CryptoCore SHA3 file test"

    file_path.write_bytes(data)

    result = hash_file(
        str(file_path),
        "sha3-256"
    )

    expected = hashlib.sha3_256(data).hexdigest()

    assert result == expected


def test_hash_file_empty(tmp_path):
    file_path = tmp_path / "empty.bin"
    file_path.write_bytes(b"")

    assert hash_file(
        str(file_path),
        "sha256"
    ) == hashlib.sha256(b"").hexdigest()

    assert hash_file(
        str(file_path),
        "sha3-256"
    ) == hashlib.sha3_256(b"").hexdigest()


def test_hash_file_multiple_chunks(tmp_path):
    file_path = tmp_path / "large.bin"

    data = bytes(range(256)) * 1000
    file_path.write_bytes(data)

    assert hash_file(
        str(file_path),
        "sha256"
    ) == hashlib.sha256(data).hexdigest()

    assert hash_file(
        str(file_path),
        "sha3-256"
    ) == hashlib.sha3_256(data).hexdigest()


def test_hash_file_missing():
    with pytest.raises(FileNotFoundError):
        hash_file(
            "missing-file.bin",
            "sha256"
        )


def test_hash_file_unsupported_algorithm(tmp_path):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(b"test")

    with pytest.raises(ValueError):
        hash_file(
            str(file_path),
            "md5"
        )
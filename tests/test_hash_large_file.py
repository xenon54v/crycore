import hashlib
import os

import pytest

from cryptocore.hash.file_hash import hash_file


LARGE_SHA256_SIZE = 1024 * 1024 * 1024 + 1
SHA3_STREAM_SIZE = 20 * 1024 * 1024


@pytest.mark.skipif(
    os.environ.get("RUN_LARGE_HASH_TEST") != "1",
    reason="Large SHA-256 test is disabled by default"
)
def test_sha256_file_larger_than_1gb(tmp_path):
    file_path = tmp_path / "large_1gb.bin"

    with open(file_path, "wb") as file:
        file.seek(LARGE_SHA256_SIZE - 1)
        file.write(b"\0")

    assert file_path.stat().st_size > 1024 * 1024 * 1024

    our_hash = hash_file(
        str(file_path),
        "sha256"
    )

    reference = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(8192)

            if not chunk:
                break

            reference.update(chunk)

    assert our_hash == reference.hexdigest()


def test_sha3_256_streaming_large_file(tmp_path):
    file_path = tmp_path / "sha3_stream.bin"

    chunk = bytes(range(256)) * 32

    with open(file_path, "wb") as file:
        remaining = SHA3_STREAM_SIZE

        while remaining > 0:
            part = chunk[:min(len(chunk), remaining)]
            file.write(part)
            remaining -= len(part)

    our_hash = hash_file(
        str(file_path),
        "sha3-256"
    )

    reference = hashlib.sha3_256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(8192)

            if not data:
                break

            reference.update(data)

    assert our_hash == reference.hexdigest()
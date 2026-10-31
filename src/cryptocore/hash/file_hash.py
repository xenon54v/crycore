from pathlib import Path
from typing import BinaryIO

from cryptocore.hash.sha256 import SHA256
from cryptocore.hash.sha3_256 import SHA3_256


CHUNK_SIZE = 8192


def create_hasher(algorithm: str):
    if algorithm == "sha256":
        return SHA256()

    if algorithm == "sha3-256":
        return SHA3_256()

    raise ValueError(
        f"Unsupported hash algorithm: {algorithm}"
    )


def hash_stream(
    stream: BinaryIO,
    algorithm: str
) -> str:
    hasher = create_hasher(algorithm)

    while True:
        chunk = stream.read(CHUNK_SIZE)

        if not chunk:
            break

        hasher.update(chunk)

    return hasher.hexdigest()


def hash_file(
    file_path: str,
    algorithm: str
) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Input path is not a file: {file_path}"
        )

    try:
        with path.open("rb") as file:
            return hash_stream(
                file,
                algorithm
            )

    except OSError as error:
        raise OSError(
            f"Could not read input file: {file_path}"
        ) from error
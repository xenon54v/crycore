import os


def generate_random_bytes(num_bytes: int) -> bytes:
    if num_bytes <= 0:
        raise ValueError("Number of bytes must be greater than zero")

    try:
        return os.urandom(num_bytes)
    except OSError as error:
        raise RuntimeError(
            "Failed to generate cryptographically secure random bytes"
        ) from error
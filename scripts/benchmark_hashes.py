import hashlib
import time

from cryptocore.hash.sha256 import SHA256
from cryptocore.hash.sha3_256 import SHA3_256


TEST_SIZES = [
    1_024,          # 1 KB
    1_048_576,      # 1 MB
    10_485_760,     # 10 MB
]


def measure(function, data: bytes) -> float:
    start = time.perf_counter()

    function(data)

    end = time.perf_counter()

    return end - start


def our_sha256(data: bytes) -> str:
    return SHA256.hash(data)


def our_sha3_256(data: bytes) -> str:
    return SHA3_256.hash(data)


def hashlib_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hashlib_sha3_256(data: bytes) -> str:
    return hashlib.sha3_256(data).hexdigest()


def format_size(size: int) -> str:
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.0f} MB"

    return f"{size / 1024:.0f} KB"


def main() -> None:
    print("CryptoCore hash benchmark")
    print()

    print(
        f"{'Size':<10}"
        f"{'Our SHA-256':<18}"
        f"{'hashlib SHA-256':<20}"
        f"{'Our SHA3-256':<18}"
        f"{'hashlib SHA3-256':<20}"
    )

    print("-" * 86)

    for size in TEST_SIZES:
        data = bytes(
            index % 256
            for index in range(size)
        )

        our_sha256_time = measure(
            our_sha256,
            data
        )

        hashlib_sha256_time = measure(
            hashlib_sha256,
            data
        )

        our_sha3_time = measure(
            our_sha3_256,
            data
        )

        hashlib_sha3_time = measure(
            hashlib_sha3_256,
            data
        )

        print(
            f"{format_size(size):<10}"
            f"{our_sha256_time:<18.6f}"
            f"{hashlib_sha256_time:<20.6f}"
            f"{our_sha3_time:<18.6f}"
            f"{hashlib_sha3_time:<20.6f}"
        )


if __name__ == "__main__":
    main()
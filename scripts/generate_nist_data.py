from cryptocore.csprng import generate_random_bytes


OUTPUT_FILE = "nist_test_data.bin"
TOTAL_SIZE = 10_000_000
CHUNK_SIZE = 4096


def main() -> None:
    bytes_written = 0

    with open(OUTPUT_FILE, "wb") as file:
        while bytes_written < TOTAL_SIZE:
            chunk_size = min(
                CHUNK_SIZE,
                TOTAL_SIZE - bytes_written
            )

            data = generate_random_bytes(chunk_size)
            file.write(data)

            bytes_written += chunk_size

    print(
        f"Generated {bytes_written} bytes "
        f"in {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
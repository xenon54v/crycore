import argparse
import sys

from cryptocore.file_io import read_file, write_file
from cryptocore.modes.ecb import encrypt, decrypt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptocore",
        description="CryptoCore cryptographic command-line tool"
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        choices=["aes"],
        help="Encryption algorithm"
    )

    parser.add_argument(
        "--mode",
        required=True,
        choices=["ecb"],
        help="Cipher mode"
    )

    operation = parser.add_mutually_exclusive_group(required=True)

    operation.add_argument(
        "--encrypt",
        action="store_true",
        help="Encrypt input file"
    )

    operation.add_argument(
        "--decrypt",
        action="store_true",
        help="Decrypt input file"
    )

    parser.add_argument(
        "--key",
        required=True,
        help="AES-128 key as a hexadecimal string"
    )

    parser.add_argument(
        "--input",
        dest="input_file",
        required=True,
        help="Input file path"
    )

    parser.add_argument(
        "--output",
        dest="output_file",
        required=True,
        help="Output file path"
    )

    return parser


def parse_key(key_hex: str) -> bytes:
    try:
        key = bytes.fromhex(key_hex)
    except ValueError as error:
        raise ValueError("Key must be a valid hexadecimal string") from error

    if len(key) != 16:
        raise ValueError("AES-128 key must be exactly 16 bytes")

    return key


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        key = parse_key(args.key)
        data = read_file(args.input_file)

        if args.encrypt:
            result = encrypt(data, key)
        else:
            result = decrypt(data, key)

        write_file(args.output_file, result)

    except (ValueError, FileNotFoundError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
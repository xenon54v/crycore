import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptocore",
        description="CryptoCore cryptographic command-line tool"
    )

    parser.add_argument(
        "--algorithm",
        choices=["aes"],
        help="Encryption algorithm"
    )

    parser.add_argument(
        "--mode",
        choices=["ecb"],
        help="Cipher mode"
    )

    operation = parser.add_mutually_exclusive_group()

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
        help="Encryption key as hexadecimal string"
    )

    parser.add_argument(
        "--input",
        dest="input_file",
        help="Input file path"
    )

    parser.add_argument(
        "--output",
        dest="output_file",
        help="Output file path"
    )

    return parser


def main() -> None:
    parser = build_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()
import argparse
import sys

from cryptocore.file_io import read_file, write_file
from cryptocore.iv import generate_iv, parse_iv

from cryptocore.modes import ecb
from cryptocore.modes import cbc
from cryptocore.modes import cfb
from cryptocore.modes import ofb
from cryptocore.modes import ctr

IV_SIZE = 16

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
        choices=["ecb", "cbc", "cfb", "ofb", "ctr"],
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
        "--iv",
        help="Initialization vector as a hexadecimal string"
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

def encrypt_data(
    mode: str,
    data: bytes,
    key: bytes,
    iv_hex: str | None
) -> bytes:
    if iv_hex is not None:
        raise ValueError("--iv must not be provided during encryption")

    if mode == "ecb":
        return ecb.encrypt(data, key)

    iv = generate_iv()

    if mode == "cbc":
        ciphertext = cbc.encrypt(data, key, iv)
    elif mode == "cfb":
        ciphertext = cfb.encrypt(data, key, iv)
    elif mode == "ofb":
        ciphertext = ofb.encrypt(data, key, iv)
    elif mode == "ctr":
        ciphertext = ctr.encrypt(data, key, iv)
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    # для новых режимов формат файла:
    # 16-byte IV ciphertext
    return iv + ciphertext

def decrypt_data(
    mode: str,
    data: bytes,
    key: bytes,
    iv_hex: str | None
) -> bytes:
    if mode == "ecb":
        if iv_hex is not None:
            raise ValueError("ECB mode does not use an IV")

        return ecb.decrypt(data, key)

    if iv_hex is not None:
        iv = parse_iv(iv_hex)
        ciphertext = data
    else:
        if len(data) < IV_SIZE:
            raise ValueError(
                "Input file is too short to contain a 16-byte IV"
            )

        iv = data[:IV_SIZE]
        ciphertext = data[IV_SIZE:]

    if mode == "cbc":
        return cbc.decrypt(ciphertext, key, iv)
    elif mode == "cfb":
        return cfb.decrypt(ciphertext, key, iv)
    elif mode == "ofb":
        return ofb.decrypt(ciphertext, key, iv)
    elif mode == "ctr":
        return ctr.decrypt(ciphertext, key, iv)

    raise ValueError(f"Unsupported mode: {mode}")

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        key = parse_key(args.key)
        data = read_file(args.input_file)

        if args.encrypt:
            result = encrypt_data(
                args.mode,
                data,
                key,
                args.iv
            )
        else:
            result = decrypt_data(
                args.mode,
                data,
                key,
                args.iv
            )

        write_file(args.output_file, result)

    except (ValueError, FileNotFoundError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
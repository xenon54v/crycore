import argparse
import sys

from cryptocore.file_io import read_file, write_file
from cryptocore.iv import generate_iv, parse_iv

from cryptocore.modes import ecb
from cryptocore.modes import cbc
from cryptocore.modes import cfb
from cryptocore.modes import ofb
from cryptocore.modes import ctr
from cryptocore.csprng import generate_random_bytes
from cryptocore.hash.file_hash import hash_file, hash_stream

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

def get_key(key_hex: str | None, encrypting: bool) -> bytes:
    if key_hex is not None:
        key = parse_key(key_hex)

        if is_weak_key(key):
            print(
                "[WARNING] The provided key appears to be weak",
                file=sys.stderr
            )

        return key

    if not encrypting:
        raise ValueError("--key is required for decryption")

    key = generate_random_bytes(16)

    print(f"[INFO] Generated random key: {key.hex()}")

    return key

def is_weak_key(key: bytes) -> bool:
    if key == bytes(16):
        return True

    if key == bytes(range(16)):
        return True

    if key == bytes(range(1, 17)):
        return True

    if len(set(key)) == 1:
        return True

    return False

def handle_dgst(args: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog="cryptocore dgst",
        description="Compute file message digest"
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        choices=["sha256", "sha3-256"],
        help="Hash algorithm"
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
        help="Write digest result to a file"
    )

    parsed = parser.parse_args(args)

    if parsed.input_file == "-":
        digest = hash_stream(
            sys.stdin.buffer,
            parsed.algorithm
        )
    else:
        digest = hash_file(
            parsed.input_file,
            parsed.algorithm
        )

    result = f"{digest}  {parsed.input_file}"

    if parsed.output_file:
        try:
            with open(
                parsed.output_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(result + "\n")
        except OSError as error:
            raise OSError(
                f"Could not write output file: {parsed.output_file}"
            ) from error
    else:
        print(result)

def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "dgst":
        try:
            handle_dgst(sys.argv[2:])
        except (
            ValueError,
            FileNotFoundError,
            OSError
        ) as error:
            print(
                f"Error: {error}",
                file=sys.stderr
            )
            sys.exit(1)

        return

    parser = build_parser()
    args = parser.parse_args()

    try:
        key = get_key(args.key, args.encrypt)
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
        output_file = args.output_file

        if output_file is None:
            if args.encrypt:
                output_file = "encrypted.bin"
            else:
                output_file = "decrypted.bin"
        write_file(output_file, result)

    except (ValueError, FileNotFoundError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
import os

IV_SIZE = 16

def generate_iv() -> bytes:
    return os.urandom(IV_SIZE)

def validate_iv(iv: bytes) -> None:
    if len(iv) != IV_SIZE:
        raise ValueError("IV must be exactly 16 bytes")

def parse_iv(iv_hex: str) -> bytes:
    try:
        iv = bytes.fromhex(iv_hex)
    except ValueError as error:
        raise ValueError("IV must be a valid hexadecimal string") from error

    validate_iv(iv)

    return iv
from Crypto.Cipher import AES


BLOCK_SIZE = 16
KEY_SIZE = 16


def validate_key(key: bytes) -> None:
    if len(key) != KEY_SIZE:
        raise ValueError("AES-128 key must be exactly 16 bytes")


def encrypt_block(block: bytes, key: bytes) -> bytes:
    validate_key(key)

    if len(block) != BLOCK_SIZE:
        raise ValueError("AES block must be exactly 16 bytes")

    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)


def decrypt_block(block: bytes, key: bytes) -> bytes:
    validate_key(key)

    if len(block) != BLOCK_SIZE:
        raise ValueError("AES block must be exactly 16 bytes")

    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)
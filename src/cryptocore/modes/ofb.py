from cryptocore.crypto.aes import BLOCK_SIZE, encrypt_block
from cryptocore.iv import validate_iv

def xor_bytes(first: bytes, second: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(first, second))

def encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_iv(iv)

    result = bytearray()
    feedback = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset:offset + BLOCK_SIZE]

        feedback = encrypt_block(feedback, key)
        encrypted_block = xor_bytes(block, feedback[:len(block)])

        result.extend(encrypted_block)

    return bytes(result)

def decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return encrypt(data, key, iv)
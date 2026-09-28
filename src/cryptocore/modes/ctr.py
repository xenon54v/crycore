from cryptocore.crypto.aes import BLOCK_SIZE, encrypt_block
from cryptocore.iv import validate_iv

def xor_bytes(first: bytes, second: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(first, second))

def increment_counter(counter: bytes) -> bytes:
    value = int.from_bytes(counter, byteorder="big")
    value = (value + 1) % (1 << (BLOCK_SIZE * 8))
    return value.to_bytes(BLOCK_SIZE, byteorder="big")

def encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_iv(iv)

    result = bytearray()
    counter = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset:offset + BLOCK_SIZE]

        keystream = encrypt_block(counter, key)
        encrypted_block = xor_bytes(block, keystream[:len(block)])

        result.extend(encrypted_block)
        counter = increment_counter(counter)

    return bytes(result)

def decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return encrypt(data, key, iv)
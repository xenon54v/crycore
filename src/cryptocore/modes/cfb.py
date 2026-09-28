from cryptocore.crypto.aes import BLOCK_SIZE, encrypt_block
from cryptocore.iv import validate_iv

def xor_bytes(first: bytes, second: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(first, second))

def encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_iv(iv)

    result = bytearray()
    previous_block = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset:offset + BLOCK_SIZE]

        keystream = encrypt_block(previous_block, key)
        encrypted_block = xor_bytes(block, keystream[:len(block)])

        result.extend(encrypted_block)

        if len(block) == BLOCK_SIZE:
            previous_block = encrypted_block

    return bytes(result)

def decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_iv(iv)

    result = bytearray()
    previous_block = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset:offset + BLOCK_SIZE]

        keystream = encrypt_block(previous_block, key)
        decrypted_block = xor_bytes(block, keystream[:len(block)])

        result.extend(decrypted_block)

        if len(block) == BLOCK_SIZE:
            previous_block = block

    return bytes(result)
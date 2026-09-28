from cryptocore.crypto.aes import BLOCK_SIZE, encrypt_block, decrypt_block
from cryptocore.iv import validate_iv
from cryptocore.modes.ecb import pad, unpad

def xor_bytes(first: bytes, second: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(first, second))

def encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_iv(iv)

    padded_data = pad(data)
    result = bytearray()

    previous_block = iv

    for offset in range(0, len(padded_data), BLOCK_SIZE):
        block = padded_data[offset:offset + BLOCK_SIZE]

        xored_block = xor_bytes(block, previous_block)
        encrypted_block = encrypt_block(xored_block, key)

        result.extend(encrypted_block)
        previous_block = encrypted_block

    return bytes(result)

def decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_iv(iv)

    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("CBC ciphertext length must be a multiple of 16 bytes")

    result = bytearray()
    previous_block = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset:offset + BLOCK_SIZE]

        decrypted_block = decrypt_block(block, key)
        plaintext_block = xor_bytes(decrypted_block, previous_block)

        result.extend(plaintext_block)
        previous_block = block

    return unpad(bytes(result))
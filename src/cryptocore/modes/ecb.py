from cryptocore.crypto.aes import BLOCK_SIZE, encrypt_block, decrypt_block


def pad(data: bytes) -> bytes:
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    padding = bytes([padding_length]) * padding_length
    return data + padding


def unpad(data: bytes) -> bytes:
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padded data length")

    padding_length = data[-1]

    if padding_length < 1 or padding_length > BLOCK_SIZE:
        raise ValueError("Invalid PKCS#7 padding")

    expected_padding = bytes([padding_length]) * padding_length

    if data[-padding_length:] != expected_padding:
        raise ValueError("Invalid PKCS#7 padding")

    return data[:-padding_length]


def encrypt(data: bytes, key: bytes) -> bytes:
    padded_data = pad(data)
    result = bytearray()

    for offset in range(0, len(padded_data), BLOCK_SIZE):
        block = padded_data[offset:offset + BLOCK_SIZE]
        result.extend(encrypt_block(block, key))

    return bytes(result)


def decrypt(data: bytes, key: bytes) -> bytes:
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Encrypted data length must be a multiple of 16 bytes")

    result = bytearray()

    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset:offset + BLOCK_SIZE]
        result.extend(decrypt_block(block, key))

    return unpad(bytes(result))
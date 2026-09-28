import pytest

from cryptocore.modes.cbc import encrypt, decrypt

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
IV = bytes.fromhex("AABBCCDDEEFF00112233445566778899")

def test_cbc_encrypt_decrypt_text():
    data = b"Hello CBC mode!"

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert encrypted != data

def test_cbc_multiple_blocks():
    data = b"This message contains more than one AES block."

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) % 16 == 0

def test_cbc_exact_block():
    data = b"1234567890abcdef"

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data

    # CBC использует PKCS#7, поэтому добавится ещё один блок
    assert len(encrypted) == 32

def test_cbc_empty_data():
    data = b""

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == 16

def test_cbc_binary_data():
    data = bytes(range(256))

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data

def test_cbc_invalid_iv_length():
    invalid_iv = b"short"

    with pytest.raises(ValueError):
        encrypt(b"Hello", KEY, invalid_iv)

def test_cbc_invalid_ciphertext_length():
    with pytest.raises(ValueError):
        decrypt(b"not-a-full-block", KEY, IV)

def test_cbc_empty_ciphertext():
    with pytest.raises(ValueError):
        decrypt(b"", KEY, IV)

def test_cbc_corrupted_padding():
    data = b"Hello CBC!"

    encrypted = bytearray(encrypt(data, KEY, IV))
    encrypted[-1] ^= 1

    with pytest.raises(ValueError):
        decrypt(bytes(encrypted), KEY, IV)
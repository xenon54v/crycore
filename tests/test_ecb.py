import pytest

from cryptocore.modes.ecb import encrypt, decrypt


KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")


def test_encrypt_decrypt_text():
    data = b"Hello CryptoCore!"

    encrypted = encrypt(data, KEY)
    decrypted = decrypt(encrypted, KEY)

    assert decrypted == data
    assert encrypted != data


def test_encrypt_decrypt_multiple_blocks():
    data = b"This message is longer than one AES block."

    encrypted = encrypt(data, KEY)
    decrypted = decrypt(encrypted, KEY)

    assert decrypted == data
    assert len(encrypted) % 16 == 0


def test_encrypt_decrypt_exact_block():
    data = b"1234567890abcdef"

    encrypted = encrypt(data, KEY)
    decrypted = decrypt(encrypted, KEY)

    assert decrypted == data

    # PKCS#7 должен добавить дополнительный блок padding.
    assert len(encrypted) == 32


def test_encrypt_decrypt_empty_data():
    data = b""

    encrypted = encrypt(data, KEY)
    decrypted = decrypt(encrypted, KEY)

    assert decrypted == data
    assert len(encrypted) == 16


def test_encrypt_decrypt_binary_data():
    data = bytes(range(256))

    encrypted = encrypt(data, KEY)
    decrypted = decrypt(encrypted, KEY)

    assert decrypted == data


def test_invalid_key_length():
    invalid_key = b"short-key"

    with pytest.raises(ValueError):
        encrypt(b"Hello", invalid_key)


def test_invalid_ciphertext_length():
    invalid_data = b"not-16-bytes"

    with pytest.raises(ValueError):
        decrypt(invalid_data, KEY)


def test_decrypt_empty_ciphertext():
    with pytest.raises(ValueError):
        decrypt(b"", KEY)


def test_corrupted_ciphertext_padding():
    data = b"Hello CryptoCore!"

    encrypted = bytearray(encrypt(data, KEY))

    # Повреждаем последний байт зашифрованного блока.
    encrypted[-1] ^= 1

    with pytest.raises(ValueError):
        decrypt(bytes(encrypted), KEY)
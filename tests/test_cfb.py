import pytest

from cryptocore.modes.cfb import encrypt, decrypt

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
IV = bytes.fromhex("AABBCCDDEEFF00112233445566778899")

def test_cfb_encrypt_decrypt_text():
    data = b"Hello CFB mode!"

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert encrypted != data

def test_cfb_multiple_blocks():
    data = b"This message contains more than one AES block."

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)

def test_cfb_partial_final_block():
    data = b"1234567890abcdefXYZ"

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)

def test_cfb_empty_data():
    data = b""

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert encrypted == b""
    assert decrypted == b""

def test_cfb_binary_data():
    data = bytes(range(256))

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)

def test_cfb_invalid_iv_length():
    invalid_iv = b"short"

    with pytest.raises(ValueError):
        encrypt(b"Hello", KEY, invalid_iv)

def test_cfb_wrong_key_length():
    invalid_key = b"short-key"

    with pytest.raises(ValueError):
        encrypt(b"Hello", invalid_key, IV)
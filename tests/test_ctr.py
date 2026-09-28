import pytest

from cryptocore.modes.ctr import encrypt, decrypt, increment_counter

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
IV = bytes.fromhex("AABBCCDDEEFF00112233445566778899")

def test_ctr_encrypt_decrypt_text():
    data = b"Hello CTR mode!"

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert encrypted != data

def test_ctr_multiple_blocks():
    data = b"This message contains more than one AES block."

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)

def test_ctr_partial_final_block():
    data = b"1234567890abcdefXYZ"

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)

def test_ctr_empty_data():
    data = b""

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert encrypted == b""
    assert decrypted == b""

def test_ctr_binary_data():
    data = bytes(range(256))

    encrypted = encrypt(data, KEY, IV)
    decrypted = decrypt(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)

def test_ctr_invalid_iv_length():
    invalid_iv = b"short"

    with pytest.raises(ValueError):
        encrypt(b"Hello", KEY, invalid_iv)

def test_ctr_wrong_key_length():
    invalid_key = b"short-key"

    with pytest.raises(ValueError):
        encrypt(b"Hello", invalid_key, IV)

def test_increment_counter():
    counter = bytes.fromhex(
        "00000000000000000000000000000001"
    )

    result = increment_counter(counter)

    assert result == bytes.fromhex(
        "00000000000000000000000000000002"
    )

def test_increment_counter_overflow():
    counter = bytes.fromhex(
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    )

    result = increment_counter(counter)

    assert result == bytes(16)
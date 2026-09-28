import pytest

from cryptocore.iv import generate_iv, validate_iv, parse_iv

VALID_IV_HEX = "AABBCCDDEEFF00112233445566778899"

def test_generate_iv_length():
    iv = generate_iv()

    assert isinstance(iv, bytes)
    assert len(iv) == 16

def test_generate_iv_is_random():
    iv1 = generate_iv()
    iv2 = generate_iv()

    assert iv1 != iv2

def test_validate_correct_iv():
    iv = bytes.fromhex(VALID_IV_HEX)

    validate_iv(iv)

def test_validate_short_iv():
    with pytest.raises(ValueError):
        validate_iv(b"short")

def test_parse_valid_iv():
    iv = parse_iv(VALID_IV_HEX)

    assert isinstance(iv, bytes)
    assert len(iv) == 16
    assert iv == bytes.fromhex(VALID_IV_HEX)

def test_parse_invalid_hex_iv():
    with pytest.raises(ValueError):
        parse_iv("not-valid-hex")

def test_parse_wrong_length_iv():
    with pytest.raises(ValueError):
        parse_iv("00112233")
import pytest

from cryptocore.modes.ecb import pad, unpad


def test_pad_short_data():
    data = b"hello"

    padded = pad(data)

    assert len(padded) == 16
    assert padded[-1] == 11
    assert padded[-11:] == bytes([11]) * 11


def test_pad_exact_block():
    data = b"1234567890abcdef"

    padded = pad(data)

    assert len(padded) == 32
    assert padded[-16:] == bytes([16]) * 16


def test_pad_empty_data():
    padded = pad(b"")

    assert len(padded) == 16
    assert padded == bytes([16]) * 16


def test_unpad():
    original = b"hello"
    padded = pad(original)

    assert unpad(padded) == original


def test_unpad_exact_block():
    original = b"1234567890abcdef"
    padded = pad(original)

    assert unpad(padded) == original


def test_unpad_invalid_padding_value():
    data = b"1234567890abcde\x00"

    with pytest.raises(ValueError):
        unpad(data)


def test_unpad_invalid_padding_bytes():
    data = b"1234567890ab\x04\x04\x03\x04"

    with pytest.raises(ValueError):
        unpad(data)


def test_unpad_empty_data():
    with pytest.raises(ValueError):
        unpad(b"")
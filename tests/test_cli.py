import pytest

from cryptocore.cli import (
    build_parser,
    parse_key,
    encrypt_data,
    decrypt_data,
    main,
)

VALID_KEY_HEX = "000102030405060708090a0b0c0d0e0f"
VALID_KEY = bytes.fromhex(VALID_KEY_HEX)
VALID_IV_HEX = "AABBCCDDEEFF00112233445566778899"

def test_parse_valid_key():
    key = parse_key(VALID_KEY_HEX)

    assert isinstance(key, bytes)
    assert len(key) == 16

def test_parse_invalid_hex_key():
    with pytest.raises(ValueError):
        parse_key("this-is-not-hex")

def test_parse_short_key():
    with pytest.raises(ValueError):
        parse_key("00112233")

@pytest.mark.parametrize("mode", ["cbc", "cfb", "ofb", "ctr"])
def test_encrypt_decrypt_with_embedded_iv(mode):
    data = b"CryptoCore Sprint 2 test data\x00\x01\x02\xff"

    encrypted = encrypt_data(
        mode,
        data,
        VALID_KEY,
        None
    )

    assert len(encrypted) >= 16

    decrypted = decrypt_data(
        mode,
        encrypted,
        VALID_KEY,
        None
    )

    assert decrypted == data

@pytest.mark.parametrize("mode", ["cbc", "cfb", "ofb", "ctr"])
def test_decrypt_with_explicit_iv(mode):
    data = b"Explicit IV test"

    iv = bytes.fromhex(VALID_IV_HEX)

    if mode == "cbc":
        from cryptocore.modes.cbc import encrypt
    elif mode == "cfb":
        from cryptocore.modes.cfb import encrypt
    elif mode == "ofb":
        from cryptocore.modes.ofb import encrypt
    else:
        from cryptocore.modes.ctr import encrypt

    ciphertext = encrypt(data, VALID_KEY, iv)

    decrypted = decrypt_data(
        mode,
        ciphertext,
        VALID_KEY,
        VALID_IV_HEX
    )

    assert decrypted == data

def test_iv_not_allowed_during_encryption():
    with pytest.raises(ValueError):
        encrypt_data(
            "cbc",
            b"Hello",
            VALID_KEY,
            VALID_IV_HEX
        )

def test_ecb_does_not_use_iv():
    with pytest.raises(ValueError):
        decrypt_data(
            "ecb",
            b"1234567890abcdef",
            VALID_KEY,
            VALID_IV_HEX
        )

def test_input_too_short_for_iv():
    with pytest.raises(ValueError):
        decrypt_data(
            "cbc",
            b"short",
            VALID_KEY,
            None
        )

def test_encrypt_and_decrypt_file(tmp_path, monkeypatch):
    input_file = tmp_path / "input.bin"
    encrypted_file = tmp_path / "encrypted.bin"
    decrypted_file = tmp_path / "decrypted.bin"

    original_data = b"CryptoCore Sprint 2 file test\x00\x01\xff"
    input_file.write_bytes(original_data)

    encrypt_args = [
        "cryptocore",
        "--algorithm", "aes",
        "--mode", "cbc",
        "--encrypt",
        "--key", VALID_KEY_HEX,
        "--input", str(input_file),
        "--output", str(encrypted_file),
    ]

    monkeypatch.setattr("sys.argv", encrypt_args)
    main()

    assert encrypted_file.exists()

    encrypted_data = encrypted_file.read_bytes()

    # первые 16 байт должны содержать автоматически
    # сгенерированный IV.
    assert len(encrypted_data) >= 32

    decrypt_args = [
        "cryptocore",
        "--algorithm", "aes",
        "--mode", "cbc",
        "--decrypt",
        "--key", VALID_KEY_HEX,
        "--input", str(encrypted_file),
        "--output", str(decrypted_file),
    ]

    monkeypatch.setattr("sys.argv", decrypt_args)
    main()

    assert decrypted_file.exists()
    assert decrypted_file.read_bytes() == original_data

def test_missing_input_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.txt"
    output_file = tmp_path / "output.bin"

    args = [
        "cryptocore",
        "--algorithm", "aes",
        "--mode", "cbc",
        "--encrypt",
        "--key", VALID_KEY_HEX,
        "--input", str(missing_file),
        "--output", str(output_file),
    ]

    monkeypatch.setattr("sys.argv", args)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 1

def test_invalid_key_in_cli(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.bin"

    input_file.write_bytes(b"Hello")

    args = [
        "cryptocore",
        "--algorithm", "aes",
        "--mode", "cbc",
        "--encrypt",
        "--key", "1234",
        "--input", str(input_file),
        "--output", str(output_file),
    ]

    monkeypatch.setattr("sys.argv", args)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 1

def test_encrypt_and_decrypt_are_mutually_exclusive():
    parser = build_parser()

    args = [
        "--algorithm", "aes",
        "--mode", "cbc",
        "--encrypt",
        "--decrypt",
        "--key", VALID_KEY_HEX,
        "--input", "input.txt",
        "--output", "output.bin",
    ]

    with pytest.raises(SystemExit):
        parser.parse_args(args)

def test_operation_is_required():
    parser = build_parser()

    args = [
        "--algorithm", "aes",
        "--mode", "cbc",
        "--key", VALID_KEY_HEX,
        "--input", "input.txt",
        "--output", "output.bin",
    ]

    with pytest.raises(SystemExit):
        parser.parse_args(args)
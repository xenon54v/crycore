import pytest

from cryptocore.cli import build_parser, parse_key, main


VALID_KEY = "000102030405060708090a0b0c0d0e0f"


def test_parse_valid_key():
    key = parse_key(VALID_KEY)

    assert isinstance(key, bytes)
    assert len(key) == 16


def test_parse_invalid_hex_key():
    with pytest.raises(ValueError):
        parse_key("this-is-not-hex")


def test_parse_short_key():
    with pytest.raises(ValueError):
        parse_key("00112233")


def test_encrypt_and_decrypt_file(tmp_path, monkeypatch):
    input_file = tmp_path / "input.bin"
    encrypted_file = tmp_path / "encrypted.bin"
    decrypted_file = tmp_path / "decrypted.bin"

    original_data = b"CryptoCore Sprint 1 test data\x00\x01\x02\xff"
    input_file.write_bytes(original_data)

    encrypt_args = [
        "cryptocore",
        "--algorithm", "aes",
        "--mode", "ecb",
        "--encrypt",
        "--key", VALID_KEY,
        "--input", str(input_file),
        "--output", str(encrypted_file),
    ]

    monkeypatch.setattr("sys.argv", encrypt_args)
    main()

    assert encrypted_file.exists()
    assert encrypted_file.read_bytes() != original_data

    decrypt_args = [
        "cryptocore",
        "--algorithm", "aes",
        "--mode", "ecb",
        "--decrypt",
        "--key", VALID_KEY,
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
        "--mode", "ecb",
        "--encrypt",
        "--key", VALID_KEY,
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
        "--mode", "ecb",
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
        "--mode", "ecb",
        "--encrypt",
        "--decrypt",
        "--key", VALID_KEY,
        "--input", "input.txt",
        "--output", "output.bin",
    ]

    with pytest.raises(SystemExit):
        parser.parse_args(args)


def test_operation_is_required():
    parser = build_parser()

    args = [
        "--algorithm", "aes",
        "--mode", "ecb",
        "--key", VALID_KEY,
        "--input", "input.txt",
        "--output", "output.bin",
    ]

    with pytest.raises(SystemExit):
        parser.parse_args(args)
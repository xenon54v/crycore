import shutil
import subprocess

import pytest

from cryptocore.cli import encrypt_data, decrypt_data

KEY_HEX = "000102030405060708090a0b0c0d0e0f"
KEY = bytes.fromhex(KEY_HEX)

IV_HEX = "AABBCCDDEEFF00112233445566778899"

MODES = ["cbc", "cfb", "ofb", "ctr"]

def get_openssl():
    openssl = shutil.which("openssl")

    if openssl is None:
        pytest.skip("OpenSSL is not available in PATH")

    return openssl

@pytest.mark.parametrize("mode", MODES)
def test_cryptocore_to_openssl(tmp_path, mode):
    openssl = get_openssl()

    original_data = b"CryptoCore to OpenSSL interoperability test\x00\x01\xff"

    encrypted = encrypt_data(
        mode,
        original_data,
        KEY,
        None
    )

    # CryptoCore хранит IV в первых 16 байтах файла.
    iv = encrypted[:16]
    ciphertext = encrypted[16:]

    cipher_file = tmp_path / "cipher.bin"
    decrypted_file = tmp_path / "decrypted.bin"

    cipher_file.write_bytes(ciphertext)

    iv_hex = iv.hex()

    command = [
        openssl,
        "enc",
        f"-aes-128-{mode}",
        "-d",
        "-K", KEY_HEX,
        "-iv", iv_hex,
        "-in", str(cipher_file),
        "-out", str(decrypted_file),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, result.stderr
    assert decrypted_file.read_bytes() == original_data

@pytest.mark.parametrize("mode", MODES)
def test_openssl_to_cryptocore(tmp_path, mode):
    openssl = get_openssl()

    original_data = b"OpenSSL to CryptoCore interoperability test\x00\x01\xff"

    plain_file = tmp_path / "plain.bin"
    cipher_file = tmp_path / "cipher.bin"

    plain_file.write_bytes(original_data)

    command = [
        openssl,
        "enc",
        f"-aes-128-{mode}",
        "-K", KEY_HEX,
        "-iv", IV_HEX,
        "-in", str(plain_file),
        "-out", str(cipher_file),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, result.stderr

    ciphertext = cipher_file.read_bytes()

    decrypted = decrypt_data(
        mode,
        ciphertext,
        KEY,
        IV_HEX
    )

    assert decrypted == original_data
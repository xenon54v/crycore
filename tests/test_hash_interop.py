import shutil
import subprocess
from pathlib import PureWindowsPath

import pytest

from cryptocore.hash.file_hash import hash_file


def windows_to_wsl_path(path: str) -> str:
    windows_path = PureWindowsPath(path)

    drive = windows_path.drive.rstrip(":").lower()

    parts = windows_path.parts[1:]

    linux_path = "/".join(parts)

    return f"/mnt/{drive}/{linux_path}"


def test_sha256_matches_system_sha256sum(tmp_path):
    if shutil.which("wsl") is None:
        pytest.skip("WSL is not available")

    input_file = tmp_path / "interop.bin"

    input_file.write_bytes(
        b"CryptoCore SHA-256 interoperability test\x00\x01\xff"
    )

    our_hash = hash_file(
        str(input_file),
        "sha256"
    )

    linux_path = windows_to_wsl_path(
        str(input_file)
    )

    result = subprocess.run(
        [
            "wsl",
            "sha256sum",
            linux_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    system_hash = result.stdout.split()[0]

    assert our_hash == system_hash


def test_sha3_256_matches_openssl(tmp_path):
    if shutil.which("wsl") is None:
        pytest.skip("WSL is not available")

    input_file = tmp_path / "interop.bin"

    input_file.write_bytes(
        b"CryptoCore SHA3-256 interoperability test\x00\x01\xff"
    )

    our_hash = hash_file(
        str(input_file),
        "sha3-256"
    )

    linux_path = windows_to_wsl_path(
        str(input_file)
    )

    result = subprocess.run(
        [
            "wsl",
            "openssl",
            "dgst",
            "-sha3-256",
            linux_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    system_hash = (
        result.stdout
        .strip()
        .split("=")[-1]
        .strip()
    )

    assert our_hash == system_hash
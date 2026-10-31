import sys

import pytest

import io

from cryptocore.cli import main


def test_dgst_sha256_stdout(tmp_path, monkeypatch, capsys):
    input_file = tmp_path / "test.txt"
    input_file.write_bytes(b"abc")

    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", str(input_file),
    ]

    monkeypatch.setattr(sys, "argv", args)

    main()

    captured = capsys.readouterr()

    assert (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    ) in captured.out

    assert str(input_file) in captured.out


def test_dgst_sha3_stdout(tmp_path, monkeypatch, capsys):
    input_file = tmp_path / "test.txt"
    input_file.write_bytes(b"abc")

    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha3-256",
        "--input", str(input_file),
    ]

    monkeypatch.setattr(sys, "argv", args)

    main()

    captured = capsys.readouterr()

    assert (
        "3a985da74fe225b2045c172d6bd390bd"
        "855f086e3e9d525b46bfe24511431532"
    ) in captured.out


def test_dgst_output_file(tmp_path, monkeypatch, capsys):
    input_file = tmp_path / "test.txt"
    output_file = tmp_path / "hash.txt"

    input_file.write_bytes(b"abc")

    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", str(input_file),
        "--output", str(output_file),
    ]

    monkeypatch.setattr(sys, "argv", args)

    main()

    captured = capsys.readouterr()

    assert captured.out == ""

    content = output_file.read_text(
        encoding="utf-8"
    )

    assert content.startswith(
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )

    assert str(input_file) in content


def test_dgst_missing_file(monkeypatch, capsys):
    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", "missing-file.txt",
    ]

    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as error:
        main()

    captured = capsys.readouterr()

    assert error.value.code == 1
    assert "Error:" in captured.err


def test_dgst_rejects_key(monkeypatch):
    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", "test.txt",
        "--key", "000102030405060708090a0b0c0d0e0f",
    ]

    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2


def test_dgst_rejects_mode(monkeypatch):
    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", "test.txt",
        "--mode", "cbc",
    ]

    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2


def test_dgst_rejects_encrypt(monkeypatch):
    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", "test.txt",
        "--encrypt",
    ]

    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2


def test_dgst_rejects_iv(monkeypatch):
    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", "test.txt",
        "--iv", "000102030405060708090a0b0c0d0e0f",
    ]

    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2

def test_dgst_sha256_stdin(monkeypatch, capsys):
    data = b"abc"

    fake_stdin = io.TextIOWrapper(
        io.BytesIO(data)
    )

    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha256",
        "--input", "-",
    ]

    monkeypatch.setattr(
        sys,
        "argv",
        args
    )

    monkeypatch.setattr(
        sys,
        "stdin",
        fake_stdin
    )

    main()

    captured = capsys.readouterr()

    assert captured.out == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad  -\n"
    )


def test_dgst_sha3_stdin(monkeypatch, capsys):
    data = b"abc"

    fake_stdin = io.TextIOWrapper(
        io.BytesIO(data)
    )

    args = [
        "cryptocore",
        "dgst",
        "--algorithm", "sha3-256",
        "--input", "-",
    ]

    monkeypatch.setattr(
        sys,
        "argv",
        args
    )

    monkeypatch.setattr(
        sys,
        "stdin",
        fake_stdin
    )

    main()

    captured = capsys.readouterr()

    assert captured.out == (
        "3a985da74fe225b2045c172d6bd390bd"
        "855f086e3e9d525b46bfe24511431532  -\n"
    )
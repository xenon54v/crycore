from pathlib import Path


def read_file(file_path: str) -> bytes:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Input path is not a file: {file_path}")

    try:
        return path.read_bytes()
    except OSError as error:
        raise OSError(f"Could not read input file: {file_path}") from error


def write_file(file_path: str, data: bytes) -> None:
    path = Path(file_path)

    try:
        path.write_bytes(data)
    except OSError as error:
        raise OSError(f"Could not write output file: {file_path}") from error
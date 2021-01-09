from pathlib import Path


def read_file(file_address: Path) -> str:
    """load file (enc windows-1251) from specified path as string"""
    with open(file_address, 'r', encoding='windows-1251') as f:
        return f.read()

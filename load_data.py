
def read_file(file_address: str) -> str:
    with open(file_address, 'r', encoding='windows-1251') as f:
        return f.read()

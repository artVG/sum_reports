from striprtf import striprtf



def read_file(file_address :str) -> list:
    file =[]
    with open(file_address, 'r', encoding='windows-1251') as f:
        for line in f.readlines():
            l = striprtf(line.encode('utf-8'))
            if l:
                file.append(l)
    return file
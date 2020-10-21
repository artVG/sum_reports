from striprtf import strip_rtf
import re
from typing import List, Dict


def parse_tn(file: str) -> List[Dict]:
    file: List[str] = strip_rtf(file).split('\n')
    result: list = []
    for line in file:
        line = line.replace('\xa0', '')
        if re.findall(r"\|[0-9]+\|[0-9]{2}\.[0-9]{2}\.[0-9]+\|[0-9]+", line):
            line_list: list = line.split('|')
            doc: dict = {
                'series': line_list[0],
                'number': line_list[1],
                'date': line_list[2],
                'sum': line_list[3],
                'contract': line_list[4]
            }
            result.append(doc)
    return result


def parse_transaction(file: str) -> List[Dict]:
    file: List[str] = strip_rtf(file).split('\n')
    result: list = []
    for line in file:
        line = line.replace('\xa0', '')
        print(line)
        if re.findall(r"[0-9]+\|[0-9]{2}\.[0-9]{2}\.[0-9]+\|*\|[0-9]+", line):
            line_list: list = line.split('|')
            doc: dict = {
                'number': line_list[0],
                'product': line_list[2],
                'amount': line_list[3],
                'price': line_list[4],
            }
            result.append(doc)
    return result

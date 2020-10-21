from striprtf import strip_rtf
import re
from copy import deepcopy
from typing import List, Dict


def parse_tn(file: str) -> List[Dict]:
    file: List[str] = strip_rtf(file).split('\n')
    result: list = []
    for line in file:
        line = line.replace('\xa0', '')
        if re.findall(r'[0-9]*\|[0-9]{2}\.[0-9]{2}\.[0-9]+\|[0-9]*', line):
            line_list: list = line.split('|')
            doc: dict = {
                'series': line_list[0],
                'number': line_list[1],
                'date': line_list[2],
                'sum': line_list[3],
                'contract': line_list[4]
            }
            result.append(doc)
    print('parse_tn', len(result))
    return result


def parse_transaction(file: str) -> List[Dict]:
    file: List[str] = strip_rtf(file).split('\n')
    result: list = []
    i = 0
    for line in file:
        line = line.replace('\xa0', '')
        if re.findall(r'[0-9]*\|[0-9]{2}\.[0-9]{2}\.[0-9]+\|', line):
            line_list: list = line.split('|')
            doc: dict = {
                'number': line_list[0],
                'product': line_list[2],
                'amount': line_list[3],
                'price': line_list[4],
            }
            result.append(doc)
    print('parse_transaction', len(result))
    return result


def add_tn_to_transaction(transactions: List[Dict], tns: List[Dict]) -> List[Dict]:
    result: List[Dict] = deepcopy(transactions)
    for tr in result:
        for tn in tns:
            if tr['number'] == tn['number']:
                tr['series'] = tn['series']
                tr['date'] = tn['date']
                tr['sum'] = tn['sum']
                tr['contract'] = tn['contract']
                break
    print('add_tn_to_transaction', len(result))
    return result

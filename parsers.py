from striprtf import strip_rtf
import re
from copy import deepcopy
from typing import List, Dict


def parse_tn(file: str) -> List[Dict]:
    """parse raw tn list"""
    # gwt list of strings from rff file
    file: List[str] = strip_rtf(file).split('\n')
    result: list = []   # list to return
    for line in file:
        # delete from line all spaces in money sums
        line = line.replace('\xa0', '')
        # if line matches tn_number(7 digits)|date(dd.dd.dd or dd.dd.dddd)|sum(ddddd...)
        if re.findall(r'[0-9]*\|[0-9]{2}\.[0-9]{2}\.[0-9]+\|[0-9]*', line):
            # split line by divider '|'
            line_list: list = line.split('|')
            doc: dict = {
                'series': line_list[0],
                'number': line_list[1],
                'date': line_list[2],
                'sum': line_list[3],
                'contract': line_list[4]
            }
            # add parsed line to result list
            result.append(doc)
    return result


def parse_transaction(file: str) -> List[Dict]:
    """parse raw report from Профит"""
    # gwt list of strings from rff file
    file: List[str] = strip_rtf(file).split('\n')
    result: list = []   # list to return
    for line in file:
        # delete from line all spaces in money sums
        line = line.replace('\xa0', '')
        # if line matches tn_number(dddd...)|date(dd.dd.dd or dd.dd.dddd)|
        if re.findall(r'[0-9]*\|[0-9]{2}\.[0-9]{2}\.[0-9]+\|', line):
            # split line by divider '|'
            line_list: list = line.split('|')
            doc: dict = {
                'number': line_list[0],
                'product': line_list[2],
                'amount': int(line_list[3]),
                'price': line_list[4],
            }
            # add parsed line to result list
            result.append(doc)
    return result


def add_tn_to_transaction(transactions: List[Dict], tns: List[Dict]) -> List[Dict]:
    """add tn series, date, sum, contract number to transaction"""
    result: List[Dict] = deepcopy(transactions)
    for tr in result:
        for tn in tns:
            # if tn has the same number as transaction add data from tn to transaction
            if tr['number'] == tn['number']:
                tr['series'] = tn['series']
                tr['date'] = tn['date']
                tr['sum'] = tn['sum']
                tr['contract'] = tn['contract']
                break
    return result

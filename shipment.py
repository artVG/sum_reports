import re
import decimal
from datetime import date 
from tn import TN



class Shipment:
    def __init__(self, tn :TN, contract :str, rub_amount :decimal.Decimal):
        self.tn = tn
        self.contract = contract
        self.rub_amount = rub_amount

    def __repr__(self):
        return f'{self.tn}\t{self.contract}\t{self.rub_amount}'


def shipments(lines :list) -> list:
    shipments = []
    check = [None, None, None]
    for line in lines:
        line = line.strip('| \t\n').replace('\xa0', '')
        if check[0] and check[1] and check[2]:
            shipments.append(Shipment(TN(check[0], check[1]), str(line), check[2]))
            check = [None, None, None]
        else:
            if re.match("^[0-9]{7}", line):
                check[0] = int(line)
            elif re.match("^[0-9]{2}\.[0-9]{2}\.[0-9]{4}", line):
                dt = line.split('.')
                check[1] = date(int(dt[2]), int(dt[1]), int(dt[0]))
            elif re.match("^[0-9]*,[0-9]{2}", line):
                check[2] = decimal.Decimal(line.replace(',','.'))
            else:
                check = [None, None, None]
    return shipments
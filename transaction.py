import re
import decimal
from datetime import date 
from tn import TN



class Transaction:
    def __init__(self, tn :TN, name :str, amount :int, price :decimal.Decimal, contract=''):
        self.tn = tn
        self.name = name
        self.amount = amount
        self.price = price
        self.contract = contract

    def __repr__(self):
        return f'{self.tn}\t{self.name}\t{self.amount}\t{self.price}\t{self.contract}'

    def __lt__(self, other):
        return self.tn < other.tn


def filter_transaction_lines(lines :list) -> list:
    transaction_lines = []
    for line in lines:
        if re.match("^[0-9]{7}\|[0-9]{2}\.[0-9]{2}\.[0-9]{2}", line):
            transaction_lines.append(line.replace('\xa0', ''))
    return transaction_lines

def transactions(lines :list) -> list:
    transaction_lines = filter_transaction_lines(lines)
    transactions = []
    for i in transaction_lines:
        item = i.split('|')
        dt = list(map(lambda x: int(x), item[1].split('.')))
        transaction = Transaction(TN(int(item[0]), date(dt[2]+2000, dt[1], dt[0])),
                        str(item[2]),
                        int(item[3]),
                        decimal.Decimal(item[4].replace(',','.')))
        transactions.append(transaction)
    return transactions

def transactions_add_contract(transactions :list, shipments :list) -> None:
    for transaction in transactions:
        for shipment in shipments:
            if transaction.tn == shipment.tn:
                transaction.contract = shipment.contract
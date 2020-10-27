from typing import List
from tn import TN
from transaction import Transaction
from dataclasses import dataclass


def sort_tn_by_contract(tns: List[TN]) -> List[List[TN]]:
    contract_sorted = []
    for tn in tns:
        found = False
        for sublist in contract_sorted:
            if found:
                break
            elif sublist:
                if sublist[0].contract == tn.contract:
                    sublist.append(tn)
                    found = True
        if not found:
            contract_sorted.append([tn, ])
    return contract_sorted


def sum_by_transaction(tns: List[TN]) -> List[Transaction]:
    sum_transactions = []
    for tn in tns:
        for transaction in tn.transactions:
            found = False
            for summed_transaction in sum_transactions:
                if found:
                    break
                # elif summed_transaction:
                else:
                    if summed_transaction.check_eq_except_amount(transaction):
                        summed_transaction.amount += transaction.amount
                        found = True
            if not found:
                sum_transactions.append(transaction)
    return sum_transactions


@dataclass
class Report:
    tns: List[Transaction]
    contract: str


def report_sorted_by_contract_sum_by_transaction(tns: List[TN]) -> List[Report]:
    contract_sorted = sort_tn_by_contract(tns)
    report = []
    for contract in contract_sorted:
        summed_transactions = sum_by_transaction(contract)
        report.append(
            Report(
                tns=summed_transactions,
                contract=contract[0].contract
            )
        )
    return report


def report_sorted_by_contract(tn: List[TN]) -> List[List[TN]]:
    report = sort_tn_by_contract(tn)
    for contract in report:
        contract.sort(key=lambda x: x.date)
    return report


def report_sum_by_transaction(tns: List[TN]) -> List[Transaction]:
    return sum_by_transaction(tns)


def report_list_tn(tns: List[TN]) -> List[TN]:
    return tns

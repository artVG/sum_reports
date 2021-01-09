from typing import List
from tn import TN
from transaction import Transaction
from dataclasses import dataclass


def sort_tn_by_contract(tns: List[TN]) -> List[List[TN]]:
    """sort TNs by contract returns list of list TNs with the same contract"""
    contract_sorted = []
    for tn in tns:
        found = False
        # look for tn with the same contract in result list
        for sublist in contract_sorted:
            if found:
                # if TN with the same contract was found
                # in previous iteration there in no need to
                # look further
                break
            elif sublist:
                if sublist[0].contract == tn.contract:
                    # if this is the list with TNs with the same contract
                    # add this tn to the list
                    sublist.append(tn)
                    found = True
        # if TN with the same contract was not found
        # add new list with this tn to result list
        if not found:
            contract_sorted.append([tn, ])
    return contract_sorted


def sum_by_transaction(tns: List[TN]) -> List[Transaction]:
    """sums all transactions with the same name and price in list"""
    sum_transactions = []
    for tn in tns:
        # look for transaction with the same name and price in result list
        for transaction in tn.transactions:
            found = False
            for summed_transaction in sum_transactions:
                if found:
                    # if transaction with the same name and price was found
                    # in previous iteration there in no need to
                    # look further
                    break
                # elif summed_transaction:
                else:
                    # if this is transaction with the same name and price
                    # add amount from iterated transaction
                    if summed_transaction.check_eq_except_amount(transaction):
                        summed_transaction.amount += transaction.amount
                        found = True
            # if transaction with the same name and price was not found
            # add new transaction to result list
            if not found:
                sum_transactions.append(transaction)
    return sum_transactions


@dataclass
class TransactionsOfContract:
    """helper struct for transactions of a contract"""
    tns: List[Transaction]
    contract: str


def report_sorted_by_contract_sum_by_transaction(tns: List[TN]) -> List[TransactionsOfContract]:
    """REPORT sort TN by contracts and sum transactions of each contract"""
    contract_sorted = sort_tn_by_contract(tns)
    report = []
    for contract in contract_sorted:
        summed_transactions = sum_by_transaction(contract)
        report.append(
            TransactionsOfContract(
                tns=summed_transactions,
                contract=contract[0].contract
            )
        )
    return report


def report_sorted_by_contract(tn: List[TN]) -> List[List[TN]]:
    """REPORT sort TN by contracts"""
    report = sort_tn_by_contract(tn)
    for contract in report:
        contract.sort(key=lambda x: x.document.date)
    return report


def report_sum_by_transaction(tns: List[TN]) -> List[Transaction]:
    """REPORT sum all transactions with same name and price"""
    return sum_by_transaction(tns)


def report_list_tn(tns: List[TN]) -> List[TN]:
    """REPORT list of all TNs"""
    return tns

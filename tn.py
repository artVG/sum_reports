from document import Document
from transaction import Transaction
from typing import List, Dict, Union


class TN:
    """includes tn number, date, sunm, contract and list of transactions"""
    def __init__(self,
                 document: Document = Document(),
                 transactions_sum: str = '',
                 contract: str = '',
                 transactions: Union[List[Transaction], None] = None
                 ) -> None:
        self.document = document
        self.transactions_sum = transactions_sum
        self.contract = contract
        self.transactions = transactions

    def __repr__(self) -> str:
        return f'{self.document} {self.contract} {self.transactions_sum}{self.transactions}'

    def check_eq_except_transactions(self, other) -> bool:
        """check if all tn data the same to other except transactions"""
        return (
            self.document == other.document and
            self.transactions_sum == other.transactions_sum and
            self.contract == other.contract
        )

    def add_transactions_from(self, other) -> None:
        """add all transactons from another tn"""
        for transaction in other.transactions:
            self.transactions.append(transaction)


def from_dict(tn_dict_list: List[Dict]) -> List[TN]:
    """create list of tn from list transactions dicts"""
    result: List[TN] = []
    for tn_data in tn_dict_list:
        # create new TN from tn data
        new_tn: TN = TN(
            document=Document(
                number=tn_data['number'],
                series=tn_data['series'],
                date=tn_data['date']
            ),
            transactions_sum=tn_data['sum'],
            contract=tn_data['contract'],
            transactions=[
                Transaction(
                    product=tn_data['product'],
                    amount=tn_data['amount'],
                    price=tn_data['price']
                ),
            ]
        )
        # check if the same tn exists in result list
        found: bool = False
        for tn in result:
            # if tn exists add transactions data to existing tn
            if new_tn.check_eq_except_transactions(tn):
                tn.add_transactions_from(new_tn)
                found = True
        # if there is no such tn in result list add new tn
        if not found:
            result.append(new_tn)
    return result

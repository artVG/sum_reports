from document import Document
from transaction import Transaction
from typing import List


class TN:
    def __init__(self,
                 document: Document = Document(),
                 transactions_sum: str = '',
                 contract: str = '',
                 transactions: List[Transaction] = []
                 ) -> None:
        self.document = document
        self.transactions_sum = transactions_sum
        self.contract = contract
        self.transactions = transactions

    def __repr__(self) -> str:
        return f'{self.document} {self.contract} {self.transactions_sum}{self.transactions}'

    def check_eq_except_transactions(self, other) -> bool:
        return (
            self.document == other.document and
            self.transactions_sum == other.transactions_sum and
            self.contract == other.contract
        )

    def add_transactions_from(self, other) -> None:
        pass


def from_dict(tn_dict: dict) -> List[TN]:
    result: List[TN] = []
    for tn_data in tn_dict:
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
        found: bool = False
        for tn in result:
            if new_tn.check_eq_except_transactions(tn):
                tn.add_transactions_from(new_tn)
                found = True
        if not found:
            result.append(new_tn)
    return result

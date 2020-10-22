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

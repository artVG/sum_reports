
class Transaction:
    def __init__(self, product: str = '', amount: str = '', price: str = '') -> None:
        self.product = product
        self.amount = amount
        self.price = price

    def __repr__(self) -> str:
        return f'\t-> {self.product} -{self.amount}- {self.price}'



class Transaction:
    def __init__(self, product: str = '', amount: int = 0, price: str = '') -> None:
        self.product = product
        self.amount = amount
        self.price = price

    def __repr__(self) -> str:
        return f'\n\t-> {self.product} -{self.amount}- {self.price}'

    def check_eq_except_amount(self, other) -> bool:
        return (
            self.product == other.product and
            self.price == other.price
        )

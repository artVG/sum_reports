
class Document:
    def __init__(self, number: str = '', series: str = '', date: str = '') -> None:
        self.number = number
        self.series = series
        self.date = date

    def __repr__(self) -> str:
        return f'{self.series}{self.number} {self.date}'


class Document:
    def __init__(self, number: str = '', series: str = '', date: str = '') -> None:
        self.number = number
        self.series = series
        self.date = date

    def __repr__(self) -> str:
        return f'{self.series}{self.number} {self.date}'

    def __eq__(self, other) -> bool:
        return (
            self.number == other.number and
            self.series == other.series and
            self.date == other.date
        )

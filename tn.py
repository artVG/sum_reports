from settings import TN_NUMBER_LEN
from datetime import date


class TN:
    def __init__(self, number :int, date :date) -> None:
        self.number = number
        self.date = date
        
    def __repr__(self):
        str_number = str(self.number)
        number_len = len(str_number)
        if number_len < TN_NUMBER_LEN:
            str_number = ('0'* (TN_NUMBER_LEN - number_len)) + str_number
        return str_number + ' \\ ' + str(self.date)

    def __eq__(self, other):
        return (self.number == other.number and
                self.date == other.date)

    def __lt__(self, other):
        return (self.date < other.date or
            (self.date == other.date and self.number < other.number))
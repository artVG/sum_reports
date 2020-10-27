import openpyxl
import datetime
from transaction import Transaction
from tn import TN
from pathlib import Path
from document import Document
from typing import Tuple, List


def replace_special(s: str) -> str:
    result = s
    special = '\/*?:[].'
    for letter in special:
        result = result.replace(letter, ' ')
    return result


def write_transaction(
        sheet: openpyxl.Worksheet,
        start_row: int,
        start_column: int,
        transaction: Transaction
) -> Tuple[int, int]:
    sheet.cell(
        row=start_row,
        column=start_column,
        value=transaction.product
    )
    sheet.cell(
        row=start_row,
        column=start_column + 1,
        value=transaction.amount
    )
    sheet.cell(
        row=start_row,
        column=start_column + 2,
        value=transaction.price
    )
    next_row = start_row + 1
    next_column = start_column + 3
    return tuple(next_row, next_column)


def write_document(
        sheet: openpyxl.Worksheet,
        start_row: int,
        start_column: int,
        document: Document
) -> Tuple[int, int]:
    sheet.cell(
        row=start_row,
        column=start_column,
        value=document.series
    )
    sheet.cell(
        row=start_row,
        column=start_column + 1,
        value=document.number
    )
    sheet.cell(
        row=start_row,
        column=start_column + 2,
        value=document.date
    )
    next_row = start_row + 1
    next_column = start_column + 3
    return tuple(next_row, next_column)


def write_tn(
        sheet: openpyxl.Worksheet,
        start_row: int,
        start_column: int,
        tn: TN
) -> Tuple[int, int]:
    end = Tuple[int, int] = write_document(
        sheet=sheet,
        start_row=start_row,
        start_column=start_column,
        document=tn.document
    )
    sheet.cell(
        row=start_row,
        column=end[2],
        value=tn.contract
    )
    sheet.cell(
        row=start_row,
        column=end[2] + 1,
        value=tn.transactions_sum
    )
    for transaction in tn.transactions:
        end = write_transaction(
            sheet=sheet,
            start_row=end[1],
            start_column=start_column + 1,
            transaction=transaction
        )
    return end


def write_report_sorted_by_contract_sum_by_transaction(
        report: List[List[Transaction]],
        save_dir: Path
) -> None:
    excel_file = openpyxl.Workbook()
    for contract in report:
        sheet = excel_file.create_sheet(replace_special(contract[0].contract))
        start: Tuple[int, int] = (1, 1)
        for transaction in contract:
            start = write_transaction(
                sheet=sheet,
                start_row=start[0],
                start_column=start[1],
                tn=transaction
            )
    excel_file.save(filename=((save_dir / f'сортировка_по_контрактам_сумма_по_позициям_{datetime.now()}.xlsx'
                               ).replace(':', '-')))


def write_report_sorted_by_contract(report: List[List[TN]], save_dir: Path) -> None:
    excel_file = openpyxl.Workbook()
    for contract in report:
        sheet = excel_file.create_sheet(replace_special(contract[0].contract))
        start: Tuple[int, int] = (1, 1)
        for tn in contract:
            start = write_tn(
                sheet=sheet,
                start_row=start[0],
                start_column=start[1],
                tn=tn
            )
    excel_file.save(filename=((save_dir / f'сортировка_по_контрактам_{datetime.now()}.xlsx'
                               ).replace(':', '-')))


def write_report_sum_by_transaction(report: List[Transaction], save_dir: Path) -> None:
    excel_file = openpyxl.Workbook()
    sheet = excel_file.active
    start: Tuple[int, int] = (1, 1)
    for transaction in report:
        start = write_transaction(
            sheet=sheet,
            start_row=start[0],
            start_column=start[1],
            tn=transaction
        )
    excel_file.save(filename=((save_dir / f'сумма_по_позициям_{datetime.now()}.xlsx'
                               ).replace(':', '-')))


def write_report_list_tn(report: List[TN], save_dir: Path) -> None:
    excel_file = openpyxl.Workbook()
    sheet = excel_file.active
    start: Tuple[int, int] = (1, 1)
    for tn in report:
        start = write_tn(
            sheet=sheet,
            start_row=start[0],
            start_column=start[1],
            tn=tn
        )
    excel_file.save(filename=((save_dir / f'список_накладных_{datetime.now()}.xlsx'
                               ).replace(':', '-')))

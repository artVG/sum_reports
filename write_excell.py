import openpyxl
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


def write_report_sorted_by_contract_sum_by_transaction(report: List[List[Transaction]], save_dir: Path) -> None:
    excell_file = openpyxl.Workbook()
    for contract in report:
        sheet = excell_file.create_sheet(replace_special(contract[0].contract))
        row_n = 1
        for transaction in contract:
            sheet.cell(row=row_n, column=1, value=transaction.name)
            sheet.cell(row=row_n, column=2, value=transaction.amount)
            row_n += 1
    excell_file.save(
        filename=(save_dir / f'report_sorted_contract_sum_transactions_name{datetime.now()}.xlsx'.replace(':', '-')))


def write_report_sorted_contract(report: list, save_dir: Path) -> None:
    excell_file = openpyxl.Workbook()
    for contract in report:
        sheet = excell_file.create_sheet(replace_special(contract[0].contract))
        row_n = 1
        for transaction in contract:
            sheet.cell(row=row_n, column=1, value=transaction.name)
            sheet.cell(row=row_n, column=2, value=transaction.amount)
            sheet.cell(row=row_n, column=3, value=transaction.price)
            sheet.cell(row=row_n, column=4, value=transaction.contract)
            sheet.cell(row=row_n, column=5, value=transaction.tn.number)
            sheet.cell(row=row_n, column=6, value=transaction.tn.date)
            row_n += 1
    excell_file.save(filename=(save_dir / f'report_sorted_contract{datetime.now()}.xlsx'.replace(':', '-')))


def write_report_sum_transactions_name(report: list, save_dir: Path) -> None:
    excell_file = openpyxl.Workbook()
    sheet = excell_file.active
    row_n = 1
    for transaction in report:
        sheet.cell(row=row_n, column=1, value=transaction.name)
        sheet.cell(row=row_n, column=2, value=transaction.amount)
        row_n += 1
    excell_file.save(filename=(save_dir / f'report_sum_transactions_name{datetime.now()}.xlsx'.replace(':', '-')))


def write_report_list_tn(report: list, save_dir: Path) -> None:
    excell_file = openpyxl.Workbook()
    sheet = excell_file.active
    row_n = 1
    for tn in report:
        first = True
        for transaction in tn:
            if first:
                sheet.cell(row=row_n, column=1, value=transaction.contract)
                sheet.cell(row=row_n, column=2, value=transaction.tn.number)
                sheet.cell(row=row_n, column=3, value=transaction.tn.date)
                first = False
            sheet.cell(row=row_n, column=4, value=transaction.name)
            sheet.cell(row=row_n, column=5, value=transaction.amount)
            sheet.cell(row=row_n, column=6, value=transaction.price)
            row_n += 1
    excell_file.save(filename=(save_dir / f'report_list_tn{datetime.now()}.xlsx'.replace(':', '-')))

import openpyxl
from pathlib import Path
from datetime import datetime
 


def replace_special(s :str) -> str:
    result = s
    special='\/*?:[].'
    for l in special:
        result = result.replace(l, ' ')
    return result


def write_report_sorted_contract_sum_transactions_name(report :list, save_dir :Path) -> None:
    excell_file = openpyxl.Workbook()
    for contract in report:
        sheet = excell_file.create_sheet(replace_special(contract[0].contract))
        row_n = 1
        for transaction in contract:
            sheet.cell(row=row_n, column=1, value=transaction.name)
            sheet.cell(row=row_n, column=2, value=transaction.amount)
            row_n+=1
    excell_file.save(filename=(save_dir/f'report_sorted_contract_sum_transactions_name{datetime.now()}.xlsx'.replace(':','-')))

def write_report_sorted_contract(report :list, save_dir :Path) -> None:
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
            row_n+=1
    excell_file.save(filename=(save_dir/f'report_sorted_contract{datetime.now()}.xlsx'.replace(':','-')))


def write_report_sum_transactions_name(report :list, save_dir :Path) -> None:
    excell_file = openpyxl.Workbook()
    sheet = excell_file.active
    row_n = 1
    for transaction in report:
        sheet.cell(row=row_n, column=1, value=transaction.name)
        sheet.cell(row=row_n, column=2, value=transaction.amount)
        row_n+=1
    excell_file.save(filename=(save_dir/f'report_sum_transactions_name{datetime.now()}.xlsx'.replace(':','-')))


def write_report_list_tn(report :list, save_dir :Path) -> None:
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
            row_n+=1
    excell_file.save(filename=(save_dir/f'report_list_tn{datetime.now()}.xlsx'.replace(':','-')))
    
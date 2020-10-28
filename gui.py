from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Entry, Button, Frame, Label
from tkinter import StringVar
from tkinter import constants as tk_const

from pathlib import Path

from reports import (report_sorted_by_contract_sum_by_transaction,
                     report_sorted_by_contract,
                     report_sum_by_transaction,
                     report_list_tn)
from write_excell import (write_report_sorted_by_contract_sum_by_transaction,
                          write_report_sorted_by_contract,
                          write_report_sum_by_transaction,
                          write_report_list_tn)
from workdata import WorkData

import copy
from dataclasses import dataclass


@dataclass(frozen=True)
class WidgetNames:
    choose_report: str = 'Отчет БЦК'
    choose_ttn: str = 'Список ТН'
    out_dir: str = 'Сохранить'
    create_report: str = 'Создать'

    report_list_tn: str = 'Сортировка по ТН'
    report_sum_by_transaction: str = 'Сумма по позициям'
    report_sorted_by_contract: str = 'Сортировка по контрактам'
    report_sorted_by_contract_sum_by_transaction: str = 'Сортировка по контрактам сумма по позициям'


class ChooseFile(Frame):

    def __init__(self, name, width):
        Frame.__init__(self)
        self.file_entry = Entry(self, width=width)
        self.file_entry.grid(row=0, column=0, sticky=tk_const.W)

        self.choose_file_btn = Button(self, text='...', command=lambda: self.choose_file())
        self.choose_file_btn.grid(row=0, column=1, sticky=tk_const.W)

        self.name = StringVar()
        self.label = Label(self, textvariable=self.name)
        self.name.set(name)
        self.label.grid(row=0, column=2, sticky=tk_const.W)

        self.file = str()

    def choose_file(self):
        self.file = askopenfilename()
        self.file_entry.insert(0, self.file)

    def get_address(self):
        return self.file_entry.get()


class ChooseOutDir(Frame):

    def __init__(self, name, width):
        Frame.__init__(self)
        self.file_entry = Entry(self, width=width)
        self.file_entry.grid(row=0, column=0, sticky=tk_const.W)

        self.choose_file_btn = Button(self, text='...', command=lambda: self.choose_file())
        self.choose_file_btn.grid(row=0, column=1, sticky=tk_const.W)

        self.name = StringVar()
        self.label = Label(self, textvariable=self.name)
        self.name.set(name)
        self.label.grid(row=0, column=2, sticky=tk_const.W)

        self.dir = str()

    def choose_file(self):
        self.dir = askdirectory()
        self.file_entry.insert(0, self.dir)

    def get_address(self):
        return self.file_entry.get()


class WorkingDirs(Frame):

    def __init__(self, width):
        Frame.__init__(self)

        self.report = ChooseFile(WidgetNames.choose_report, width)
        self.report.grid(row=0, column=0, sticky=tk_const.W)

        self.ttn = ChooseFile(WidgetNames.choose_ttn, width)
        self.ttn.grid(row=1, column=0, sticky=tk_const.W)

        self.out_dir = ChooseOutDir(WidgetNames.out_dir, width)
        self.out_dir.grid(row=2, column=0, sticky=tk_const.W)

    def get_report_file(self):
        return self.report.get_address()

    def get_ttn_file(self):
        return self.ttn.get_address()

    def get_out_dir(self):
        return self.out_dir.get_address()


class Report(Frame):

    def __init__(self, name, command):
        Frame.__init__(self)
        self.description_label_text = StringVar()
        self.description_label = Label(self, textvariable=self.description_label_text)
        self.description_label_text.set(name)
        self.description_label.grid(row=0, column=1, sticky=tk_const.W)

        self.create_report_btn = Button(self, text=WidgetNames.create_report, command=command)
        self.create_report_btn.grid(row=0, column=0, sticky=tk_const.W)


class ReportsPanel(Frame):

    def __init__(self, working_dirs):
        Frame.__init__(self)

        self.data = None
        self.working_dirs = working_dirs

        self.wjt_sorted_by_contract_sum_by_transaction = Report(
            name=WidgetNames.report_sorted_by_contract_sum_by_transaction,
            command=lambda: write_report_sorted_by_contract_sum_by_transaction(
                report=report_sorted_by_contract_sum_by_transaction(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
            )
        )
        self.wjt_sorted_by_contract_sum_by_transaction.grid(row=3, column=0, sticky=tk_const.W)

        self.wjt_sorted_by_contract = Report(
            name=WidgetNames.report_sorted_by_contract,
            command=lambda: write_report_sorted_by_contract(
                report=report_sorted_by_contract(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
            )
        )
        self.wjt_sorted_by_contract.grid(row=4, column=0, sticky=tk_const.W)

        self.wjt_sum_by_transaction = Report(
            name=WidgetNames.report_sum_by_transaction,
            command=lambda: write_report_sum_by_transaction(
                report=report_sum_by_transaction(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
            )
        )
        self.wjt_sum_by_transaction.grid(row=5, column=0, sticky=tk_const.W)

        self.wjt_list_tn = Report(
            name=WidgetNames.report_list_tn,
            command=lambda: write_report_list_tn(
                report=report_list_tn(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
            )
        )
        self.wjt_list_tn.grid(row=6, column=0, sticky=tk_const.W)

    def load_data(self):
        self.data = WorkData(
            Path(self.working_dirs.get_ttn_file()),
            Path(self.working_dirs.get_report_file())
        )

    def check_data(self):
        return (self.data and
                self.data.check_files(Path(self.working_dirs.get_ttn_file()),
                                      Path(self.working_dirs.get_report_file())
                                      )
                )

    def get_transactions(self):
        if not self.check_data():
            self.load_data()
        return copy.deepcopy(self.data.tns)


class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.working_dirs = WorkingDirs(100)

        self.reports_panel = ReportsPanel(self.working_dirs)


def run_gui():
    app = App()
    app.mainloop()

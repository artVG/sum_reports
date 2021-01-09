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
    """collection of all strings been used in GUI"""
    choose_report: str = 'Отчет БЦК'
    choose_ttn: str = 'Список ТН'
    out_dir: str = 'Сохранить'
    create_report: str = 'Создать'

    report_list_tn: str = 'Сортировка по ТН'
    report_sum_by_transaction: str = 'Сумма по позициям'
    report_sorted_by_contract: str = 'Сортировка по контрактам'
    report_sorted_by_contract_sum_by_transaction: str = 'Сортировка по контрактам сумма по позициям'


class ChooseFile(Frame):
    """Choose File dialog"""

    def __init__(self, name, width):
        Frame.__init__(self)

        # file address text field
        self.file_entry = Entry(self, width=width)
        self.file_entry.grid(row=0, column=0, sticky=tk_const.W)

        # open ChooseFile dialog button
        self.choose_file_btn = Button(self, text='...', command=lambda: self.choose_file())
        self.choose_file_btn.grid(row=0, column=1, sticky=tk_const.W)

        # label with name for user
        self.name = StringVar()
        self.label = Label(self, textvariable=self.name)
        self.name.set(name)
        self.label.grid(row=0, column=2, sticky=tk_const.W)

        # file address
        self.file = str()

    def choose_file(self):
        """ask user address of a file"""
        # get file address string with askopenfilename tkinter dialog
        self.file = askopenfilename()
        # clear previous stored in entry address
        self.file_entry.delete(0, 'end')
        # insert new file address to entry
        self.file_entry.insert(0, self.file)

    def get_address(self):
        """return stored in entry address"""
        return self.file_entry.get()


class ChooseOutDir(Frame):
    """Choose Output Directory dialog"""

    def __init__(self, name, width):
        Frame.__init__(self)

        # Output Directory address text field
        self.file_entry = Entry(self, width=width)
        self.file_entry.grid(row=0, column=0, sticky=tk_const.W)

        # open ChooseOutDir dialog button
        self.choose_file_btn = Button(self, text='...', command=lambda: self.choose_file())
        self.choose_file_btn.grid(row=0, column=1, sticky=tk_const.W)

        # label with name for user
        self.name = StringVar()
        self.label = Label(self, textvariable=self.name)
        self.name.set(name)
        self.label.grid(row=0, column=2, sticky=tk_const.W)

        # directory address
        self.dir = str()

    def choose_file(self):
        """ask user address of a directory"""
        # get directory address string with askdirectory tkinter dialog
        self.dir = askdirectory()
        # clear previous stored in entry address
        self.file_entry.delete(0, 'end')
        # insert new directory address to entry
        self.file_entry.insert(0, self.dir)

    def get_address(self):
        """return stored in entry address"""
        return self.file_entry.get()


class WorkingDirs(Frame):
    """stores ingoing data files and output directory for reports"""
    def __init__(self, width):
        Frame.__init__(self)

        # report from Профит
        self.report = ChooseFile(WidgetNames.choose_report, width)
        self.report.grid(row=0, column=0, sticky=tk_const.W)

        # list of ttn
        self.ttn = ChooseFile(WidgetNames.choose_ttn, width)
        self.ttn.grid(row=1, column=0, sticky=tk_const.W)

        # output directory for reports
        self.out_dir = ChooseOutDir(WidgetNames.out_dir, width)
        self.out_dir.grid(row=2, column=0, sticky=tk_const.W)

    def get_report_file(self):
        """return address of a file containing report from Профит"""
        return self.report.get_address()

    def get_ttn_file(self):
        """return address of a file containing ttn list"""
        return self.ttn.get_address()

    def get_out_dir(self):
        """return address of output directory"""
        return self.out_dir.get_address()


class Report(Frame):
    """single output report name and "create" button"""
    def __init__(self,
                 name,  # report name string
                 command):  # report file creator function callback
        Frame.__init__(self)
        self.description_label_text = StringVar()
        self.description_label = Label(self, textvariable=self.description_label_text)
        self.description_label_text.set(name)
        self.description_label.grid(row=0, column=1, sticky=tk_const.W)

        self.create_report_btn = Button(self, text=WidgetNames.create_report, command=command)
        self.create_report_btn.grid(row=0, column=0, sticky=tk_const.W)


class ReportsPanel(Frame):
    """container for all outgoing reports"""
    def __init__(self, working_dirs):
        Frame.__init__(self)

        # parsed transactions data for reports (workdata.py)
        self.data = None
        # current working directories shown to user
        self.working_dirs = working_dirs

        # --------------------------------------------------------------------------------------------
        # all reports in order as shown to user. all the same as in the first except create report file function
        self.wjt_sorted_by_contract_sum_by_transaction = Report(
            # string name of report
            name=WidgetNames.report_sorted_by_contract_sum_by_transaction,
            # create report file function
            command=lambda: write_report_sorted_by_contract_sum_by_transaction(
                # create report function from transactions data. don't pass self.data directly
                # see get_transactions function description
                report=report_sorted_by_contract_sum_by_transaction(self.get_transactions()),
                # output directory path
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
        # --------------------------------------------------------------------------------------------

    def load_data(self):
        """load transactions data from working directories"""
        self.data = WorkData(
            Path(self.working_dirs.get_ttn_file()),
            Path(self.working_dirs.get_report_file())
        )

    def check_data(self):
        """check if user changed working directories"""
        return (self.data and
                self.data.check_files(Path(self.working_dirs.get_ttn_file()),
                                      Path(self.working_dirs.get_report_file())
                                      )
                )

    def get_transactions(self):
        """check if user changed working directories and
        return transactions data"""
        if not self.check_data():
            self.load_data()
        return copy.deepcopy(self.data.tns)


class App(Tk):
    """main and the only window"""
    def __init__(self):
        Tk.__init__(self)

        self.working_dirs = WorkingDirs(100)

        self.reports_panel = ReportsPanel(self.working_dirs)


def run_gui():
    """create and run gui"""
    app = App()
    app.mainloop()

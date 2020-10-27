from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Entry, Button, Frame, Label
from tkinter import StringVar
from tkinter import constants as tk_const

from pathlib import Path

from reports import (report_sorted_contract_sum_transactions_name, 
                    report_sorted_contract,
                    report_sum_transactions_name,
                    report_list_tn)
from write_excell import (write_report_sorted_contract_sum_transactions_name,
                    write_report_sorted_contract,
                    write_report_sum_transactions_name,
                    write_report_list_tn)
from workdata import WorkData

import copy



WIDGET_NAMES = {
    'choose_report':'Отчет БЦК',
    'choose_ttn':'Список ТН',
    'out_dir':'Сохранить',
    'create_report': 'Создать',

    'report_list_tn': 'Сортировка по ТН',
    'report_sum_transactions_name': 'Сумма по позициям',
    'report_sorted_contract': 'Сортировка по контрактам',
    'report_sorted_contract_sum_transactions_name': 'Сортировка по контрактам сумма по позициям',
}


class Choose_file(Frame):

    def __init__(self, name, width):
        Frame.__init__(self)
        self.file_entry = Entry(self, width=width)
        self.file_entry.grid(row=0, column=0, sticky=tk_const.W)

        self.choose_file_btn = Button(self, text='...', command=lambda : self.choose_file())
        self.choose_file_btn.grid(row=0, column=1, sticky=tk_const.W)

        self.name = StringVar()
        self.lable = Label(self, textvariable=self.name)
        self.name.set(name)
        self.lable.grid(row=0, column=2, sticky=tk_const.W)

        self.file = str()


    def choose_file(self):
        self.file = askopenfilename()
        self.file_entry.insert(0, self.file)

    def get_addr(self):
        return self.file_entry.get()



class Choose_out_dir(Frame):

    def __init__(self, name, width):
        Frame.__init__(self)
        self.file_entry = Entry(self, width=width)
        self.file_entry.grid(row=0, column=0, sticky=tk_const.W)

        self.choose_file_btn = Button(self, text='...', command=lambda : self.choose_file())
        self.choose_file_btn.grid(row=0, column=1, sticky=tk_const.W)

        self.name = StringVar()
        self.lable = Label(self, textvariable=self.name)
        self.name.set(name)
        self.lable.grid(row=0, column=2, sticky=tk_const.W)

        self.dir = str()


    def choose_file(self):
        self.dir = askdirectory()
        self.file_entry.insert(0, self.dir)

    def get_addr(self):
        return self.file_entry.get()



class Working_dirs(Frame):

    def __init__(self, width):
        Frame.__init__(self)

        self.report = Choose_file(WIDGET_NAMES['choose_report'], width)
        self.report.file_entry.insert(0, 'E:/python_prj/summ_report_contracts/report.rtf')
        self.report.grid(row=0, column=0, sticky=tk_const.W)

        self.ttn = Choose_file(WIDGET_NAMES['choose_ttn'], width)
        self.ttn.file_entry.insert(0, 'E:/python_prj/summ_report_contracts/ttn.rtf')
        self.ttn.grid(row=1, column=0, sticky=tk_const.W)

        self.out_dir = Choose_out_dir(WIDGET_NAMES['out_dir'], width)
        self.out_dir.file_entry.insert(0, 'E:/python_prj/summ_report_contracts')
        self.out_dir.grid(row=2, column=0, sticky=tk_const.W)

    def get_report_file(self):
        return self.report.get_addr()

    def get_ttn_file(self):
        return self.ttn.get_addr()

    def get_out_dir(self):
        return self.out_dir.get_addr()


    



class Report(Frame):

    def __init__(self, name, command):
        Frame.__init__(self)
        self.description_label_text = StringVar()
        self.description_label = Label(self, textvariable=self.description_label_text)
        self.description_label_text.set(name)
        self.description_label.grid(row=0, column=1, sticky=tk_const.W)

        self.create_report_btn = Button(self, text=WIDGET_NAMES['create_report'], command=command)
        self.create_report_btn.grid(row=0, column=0, sticky=tk_const.W)



class Reports_panell(Frame):

    def __init__(self, working_dirs):
        Frame.__init__(self)

        self.data = None
        self.working_dirs = working_dirs

        self.wjt_sorted_contract_sum_transactions_name = Report(
            name=WIDGET_NAMES['report_sorted_contract_sum_transactions_name'],
            command=lambda : write_report_sorted_contract_sum_transactions_name(
                report=report_sorted_contract_sum_transactions_name(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
                )
            )
        self.wjt_sorted_contract_sum_transactions_name.grid(row=3, column=0, sticky=tk_const.W)

        self.wjt_report_sorted_contract = Report(
            name=WIDGET_NAMES['report_sorted_contract'],
            command=lambda : write_report_sorted_contract(
                report=report_sorted_contract(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
                )
            )
        self.wjt_report_sorted_contract.grid(row=4, column=0, sticky=tk_const.W)

        self.wjt_report_sum_transactions_name = Report(
            name=WIDGET_NAMES['report_sum_transactions_name'],
            command=lambda : write_report_sum_transactions_name(
                report=report_sum_transactions_name(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
                )
            )
        self.wjt_report_sum_transactions_name.grid(row=5, column=0, sticky=tk_const.W)

        self.wjt_report_list_tn = Report(
            name=WIDGET_NAMES['report_list_tn'],
            command=lambda : write_report_list_tn(
                report=report_list_tn(self.get_transactions()),
                save_dir=Path(self.working_dirs.get_out_dir())
                )
            )
        self.wjt_report_list_tn.grid(row=6, column=0, sticky=tk_const.W)


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
        return copy.deepcopy(self.data.transactions)



class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.working_dirs = Working_dirs(100)

        self.reports_panell = Reports_panell(self.working_dirs)



def run_gui():
    app = App()
    app.mainloop()


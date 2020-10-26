from pathlib import Path
from load_data import read_file
from parsers import parse_tn, parse_transaction, add_tn_to_transaction
from tn import from_dict


class WorkData:

    def __init__(self, tn_list_path: Path, bck_report_path: Path) -> None:
        self.tn_list_path = tn_list_path
        self.bck_report_path = bck_report_path
        bck_tn_list = parse_tn(read_file(self.tn_list_path))
        bck_report = parse_transaction(read_file(self.bck_report_path))
        tn_dict = add_tn_to_transaction(bck_report, bck_tn_list)
        self.tns = from_dict(tn_dict)

    def check_files(self, tn_list_path: Path, bck_report_path: Path) -> bool:
        return (self.tn_list_path == tn_list_path and
                self.bck_report_path == bck_report_path
                )

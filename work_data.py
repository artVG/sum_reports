from pathlib import Path
from shipment import shipments
from transaction import transactions, transactions_add_contract
from load_data import read_file

class Work_data:
    
    def __init__(self, shipments_path :Path, transactions_path :Path) ->None:

        self.shipments_path = shipments_path
        self.transactions_path = transactions_path

        self.shipments = shipments(read_file(shipments_path))
        self.transactions = transactions(read_file(transactions_path))
        transactions_add_contract(self.transactions, self.shipments)


    def check_files(self, shipments_path :Path, transactions_path :Path) ->bool:
        return (self.shipments_path == shipments_path and 
            self.transactions_path == transactions_path
        )

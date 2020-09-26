def sort_transactions_contract(transactions :list) -> list:
    contract_sorted = []
    for transaction in transactions:
        found = False
        for sublist in contract_sorted:
            if found:
                pass
            elif sublist:
                if sublist[0].contract == transaction.contract:
                    sublist.append(transaction)
                    found = True
        if not found:
            contract_sorted.append([transaction, ])
    return contract_sorted

def sum_transactions_name(transactions :list) -> list:
    sum_transactions = []
    for transaction in transactions:
        found = False
        for sumed_transaction in sum_transactions:
            if found:
                pass
            elif sumed_transaction:
                if sumed_transaction.name == transaction.name:
                    sumed_transaction.amount+=transaction.amount
                    found = True
        if not found:
            sum_transactions.append(transaction)
    return sum_transactions

def f(t):
    for i in t:
        if i.amount > 15:
            print(i)

def report_sorted_contract_sum_transactions_name(transactions :list) -> list:#----------------------
    f(transactions)
    contract_sorted = sort_transactions_contract(transactions)
    report = []
    for contract in contract_sorted:
        sumed_transactions_name = sum_transactions_name(contract)
        report.append(sumed_transactions_name)
    return report

def report_sorted_contract(transactions :list) -> list:
    f(transactions)
    contract_sorted = sort_transactions_contract(transactions)
    report = []
    for contract in contract_sorted:
        report.append(sorted(contract))
    return report

def report_sum_transactions_name(transactions :list) -> list:#---------------------------
    f(transactions)
    report = sum_transactions_name(transactions)
    return report

def report_list_tn(transactions :list) -> list:
    f(transactions)
    sorted_transactions = sorted(transactions)
    report = []
    for transaction in sorted_transactions:
        found = False
        for sublist in report:
            if found:
                pass
            elif sublist:
                if sublist[0].tn == transaction.tn:
                    sublist.append(transaction)
                    found = True
        if not found:
            report.append([transaction, ])
    return report
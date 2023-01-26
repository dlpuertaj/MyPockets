def get_name_from_pocket_id(pockets, source_pocket_id):
    for pocket in pockets:
        if pocket.get_id() == source_pocket_id:
            return pocket.get_name()
    return "External Source"


def get_event_type_from_pocket_transaction(transaction):
    if transaction.income_type_id is not None:
        return "Income"
    elif transaction.expense_type_id is not None:
        return "expense"
    else:
        return ""
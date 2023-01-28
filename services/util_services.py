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


def is_amount_valid(amount_in_source, amount):
    if len(amount) > 0 and amount.isnumeric():
        if amount_in_source >= int(amount):
            return True
        else:
            return False
    else:
        return False


def calc_new_amount(original_amount, amount_to_transfer, source_or_target):
    if source_or_target:
        new_amount = original_amount - amount_to_transfer
    else:
        new_amount = original_amount + amount_to_transfer

    return new_amount

def get_pocket_by_name(list_of_pockets, pocket_name):
    for pocket in list_of_pockets:
        if pocket_name == pocket.name:
            return pocket
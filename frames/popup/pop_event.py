import ttkbootstrap as ttkboot
from tkinter import E, W
from datetime import date
from services import gui_services, global_constants, db_services


class PopEvent(ttkboot.Toplevel):
    """ Class that creates the popup for a new event"""

    EXPENSE_LABEL = "Expense"
    INCOME_LABEL = "Income"
    NEW_LABEL = "New"
    EDIT_LABEL = "Edit"

    def __init__(self, root, pockets, expense_types, income_types, new_event):
        ttkboot.Toplevel.__init__(self, root)
        self.root = root
        self.resizable(width=False, height=False)
        self.pockets = pockets
        self.expense_types = expense_types
        self.income_types = income_types
        self.new_event = new_event
        self.create_or_update_title = ''
        self.grab_set()
        self.set_create_or_update_title()
        self.event_title = self.create_or_update_title + " " + self.new_event.show_type()

    def set_create_or_update_title(self):
        if self.new_event.has_id():
            self.create_or_update_title = self.EDIT_LABEL
        else:
            self.create_or_update_title = self.NEW_LABEL

    def create_and_show_popup(self, db_connection):
        event_type_options = self.get_event_types_by_event()

        type_options = []
        pockets_options = []
        for type_option in event_type_options:
            type_options.append(type_option.get_name())

        for pocket in self.pockets:
            pockets_options.append(pocket.get_name())

        type_label = self.new_event.show_type() + " Type:"

        clicked_type = ttkboot.StringVar()
        self.add_options_to_dropdown(type_options, clicked_type, type_label, 1)

        clicked_pocket = ttkboot.StringVar()
        self.add_options_to_dropdown(pockets_options, clicked_pocket, "Pocket:", 2)

        amount_label = ttkboot.Label(self, text="Amount: ")
        amount_entry = ttkboot.Entry(self)

        date_label = ttkboot.Label(self, text="Date: ")
        date_entry = ttkboot.Entry(self)
        date_entry.insert(0, str(date.today()))

        note_label = ttkboot.Label(self, text="Note: ")
        note_entry = ttkboot.Entry(self)

        save_button = ttkboot.Button(self, text="Save", width=10,command=lambda: self.save_event(db_connection,
                                                                                                 event_type_options,
                                                                                                 clicked_pocket.get(),
                                                                                                 clicked_type.get(),
                                                                                                 amount_entry.get(),
                                                                                                 date_entry.get(),
                                                                                                 note_entry.get(), ))

        close_button = ttkboot.Button(self, text="Close", width=10, command=self.destroy, bootstyle='danger')

        self.title(self.event_title)
        amount_label.grid(column=0, row=3, sticky=W, padx=5, pady=5)
        amount_entry.grid(column=1, row=3, sticky=(E, W), padx=5, pady=5)
        date_label.grid(column=0, row=4, sticky=W, padx=5, pady=5)
        date_entry.grid(column=1, row=4, sticky=(E, W),padx=5, pady=5)
        note_label.grid(column=0, row=5, sticky=W, padx=5, pady=5)
        note_entry.grid(column=1, row=5, sticky=(E, W), padx=5, pady=5)

        save_button.grid(column=0, row=6, columnspan=2,padx=5,pady=5,sticky=(E, W))
        close_button.grid(column=0, row=7,columnspan=2, padx=5,pady=5, sticky=(E, W))

    def add_options_to_dropdown(self, options, clicked, label, grid_row):
        clicked.set(options[0])
        type_label = ttkboot.Label(self, text=label)
        type_label.grid(column=0, row=grid_row,padx=5,pady=5,sticky=W)
        dropdown = ttkboot.Combobox(self, textvariable=clicked, values=options)
        dropdown.grid(column=1, row=grid_row,padx=5,pady=5)

    def save_event(self, db_connection, types, selected_pocket, selected_event,
                   amount, current_date, note):
        used_pocket = None
        for t in types:
            if t.get_name() == selected_event:
                selected_event = t.get_id()
                break

        for pocket in self.pockets:
            if pocket.get_name() == selected_pocket:
                used_pocket = pocket
                selected_pocket = pocket.get_id()
                break

        type_of_event = str(type(self.new_event))
        if "income" in type_of_event:
            db_services.insert_event(db_connection=db_connection,
                                     is_income=True,
                                     amount=amount,
                                     event_type=selected_event,
                                     date=current_date,
                                     note=note,
                                     pocket=selected_pocket)

            db_services.update_pocket_amount(db_connection, used_pocket.get_id(),
                                             (used_pocket.get_amount() + int(amount)))

            gui_services.show_popup_message(self.root, global_constants.SUCCESS_OPERATION)
        else:
            if used_pocket.get_amount() < int(amount):
                gui_services.show_popup_message(self.root, global_constants.AMOUNT_GRATER_THAN_POCKET_AMOUNT)
            else:
                db_services.insert_event(db_connection=db_connection,
                                         is_income=False,
                                         amount=amount,
                                         event_type=selected_event,
                                         date=current_date,
                                         note=note,
                                         pocket=selected_pocket)

                db_services.update_pocket_amount(db_connection, used_pocket.get_id(),
                                                 (used_pocket.get_amount() - int(amount)))
                gui_services.show_popup_message(self.root, global_constants.SUCCESS_OPERATION)

    def get_event_types_by_event(self):
        type_of_event = str(type(self.new_event))
        if "expense" in type_of_event:
            return self.expense_types
        elif "income" in type_of_event:
            return self.income_types

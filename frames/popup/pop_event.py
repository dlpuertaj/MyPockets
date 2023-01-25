from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar, E, W
from datetime import date
from util import global_constants
from frames.popup.popup_message import PopupGenericMessage
from services import data_services, gui_services


class PopEvent(Toplevel):
    """ Class that creates the popup for a new event"""

    EXPENSE_LABEL = "Expense"
    INCOME_LABEL = "Income"
    NEW_LABEL = "New"
    EDIT_LABEL = "Edit"

    def __init__(self, root, pockets, expense_types, income_types, new_event):
        Toplevel.__init__(self,root)
        self.root = root
        self.resizable(width=False,height=False)
        self.pockets = pockets
        self.expense_types = expense_types
        self.income_types = income_types
        self.new_event = new_event
        self.create_or_update_title = ''
        self.grab_set()
        self.set_create_or_update_title()
        self.event_title = "=== " + self.create_or_update_title + " " + self.new_event.show_type() + " ==="

    def set_create_or_update_title(self):
        if self.new_event.has_id():
            self.create_or_update_title = self.EDIT_LABEL
        else:
            self.create_or_update_title = self.NEW_LABEL

    def create_and_show_popup(self,db_connection):
        event_type_options = self.get_event_types_by_event()

        type_options = []
        pockets_options = []
        for type_option in event_type_options:
            type_options.append(type_option.get_name())

        for pocket in self.pockets:
            pockets_options.append(pocket.get_name())

        type_label = self.new_event.show_type() + " Type:"

        clicked_type = StringVar()
        self.add_options_to_dropdown(type_options, clicked_type, type_label,1)

        clicked_pocket = StringVar()
        self.add_options_to_dropdown(pockets_options, clicked_pocket, "Pocket:",2)

        amount_label = Label(self, text="Amount: ")
        amount_entry = Entry(self)

        date_label = Label(self,text="Date: ")
        date_entry = Entry(self)
        date_entry.insert(0,str(date.today()))

        note_label = Label(self,text="Note: ")
        note_entry = Entry(self)

        save_button = Button(self, text="Save", command=lambda: self.save_event(db_connection,
                                                                                event_type_options,
                                                                                clicked_pocket.get(),
                                                                                clicked_type.get(),
                                                                                amount_entry.get(),
                                                                                date_entry.get(),
                                                                                note_entry.get(),))

        close_button = Button(self, text="Close", command=self.destroy)

        title_label = Label(self, text=self.event_title)
        title_label.grid(column=0, row=0,columnspan=2)
        amount_label.grid(column=0, row=3, sticky=W,padx=2)
        amount_entry.grid(column=1,row=3, sticky=(E, W),padx=3)
        date_label.grid(column=0,row=4, sticky=W,padx=2)
        date_entry.grid(column=1,row=4, sticky=(E, W),padx=3)
        note_label.grid(column=0,row=5, sticky=W,padx=2)
        note_entry.grid(column=1,row=5, sticky=(E, W),padx=3)

        save_button.grid(column=0,row=6,pady=7, padx=2,sticky=(E, W))
        close_button.grid(column=1,row=6,pady=7, padx=2,sticky=(E, W))

    def add_options_to_dropdown(self, options, clicked, label, grid_row):
        clicked.set(options[0])
        type_label = Label(self, text=label,)
        type_label.grid(column=0,row=grid_row,sticky=W,padx=2)
        dropdown = OptionMenu(self, clicked, *options)
        dropdown.grid(column=1,row=grid_row,sticky=W)

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
            data_services.insert_event(db_connection=db_connection,
                                       is_income=True,
                                       amount=amount,
                                       event_type=selected_event,
                                       date=current_date,
                                       note=note,
                                       pocket=selected_pocket)

            data_services.update_pocket_amount(db_connection,used_pocket.get_id(),
                                               (used_pocket.get_amount() + int(amount)))

            gui_services.show_popup_message(self.root,global_constants.SUCCESS_OPERATION)
        else:
            if used_pocket.get_amount() < int(amount):
                gui_services.show_popup_message(self.root, global_constants.AMOUNT_GRATER_THAN_POCKET_AMOUNT)
            else:
                data_services.insert_event(db_connection=db_connection,
                                           is_income=False,
                                           amount=amount,
                                           event_type=selected_event,
                                           date=current_date,
                                           note=note,
                                           pocket=selected_pocket)

                data_services.update_pocket_amount(db_connection, used_pocket.get_id(),
                                                   (used_pocket.get_amount() - int(amount)))
                gui_services.show_popup_message(self.root,global_constants.SUCCESS_OPERATION)

    def get_event_types_by_event(self):
        type_of_event = str(type(self.new_event))
        if "expense" in type_of_event:
            return self.expense_types
        elif "income" in type_of_event:
            return self.income_types

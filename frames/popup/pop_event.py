from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar, E, W
from datetime import date
from util import global_constants
from frames.popup.popup_message import PopupGenericMessage


class PopEvent(Toplevel):
    """ Class that creates the popup for a new event"""

    EXPENSE_LABEL = "Expense"
    INCOME_LABEL = "Income"
    NEW_LABEL = "New"
    EDIT_LABEL = "Edit"

    def __init__(self, root, event_type):
        Toplevel.__init__(self,root)
        self.root = root
        #self.geometry('250x200')
        self.resizable(width=False,height=False)
        self.event_type = event_type
        self.create_or_update_title = ''
        self.grab_set()
        self.set_create_or_update_title()
        self.event_title = "=== " + self.create_or_update_title + " " + self.event_type.show_type() + " ==="

    def set_create_or_update_title(self):
        if self.event_type.has_id():
            self.create_or_update_title = self.EDIT_LABEL
        else:
            self.create_or_update_title = self.NEW_LABEL

    def create_and_show_popup(self,serve, pockets):
        options = self.get_options_for_dropdown(serve, False) # TODO: Get type from object

        type_options = []
        pockets_options = []
        for option in options:
            type_options.append(option.get_name())

        for pocket in pockets:
            pockets_options.append(pocket.get_name())

        type_label = self.event_type.show_type() + " Type:"

        clicked_type = StringVar()
        self.add_select_dropdown(type_options, clicked_type, type_label,1)

        clicked_pocket = StringVar()
        self.add_select_dropdown(pockets_options, clicked_pocket, "Pocket:",2)

        amount_label = Label(self, text="Amount: ")
        amount_entry = Entry(self)

        date_label = Label(self,text="Date: ")
        date_entry = Entry(self)
        date_entry.insert(0,str(date.today()))

        note_label = Label(self,text="Note: ")
        note_entry = Entry(self)

        save_button = Button(self, text="Save", command=lambda: self.save_event(
            serve, options, pockets, clicked_type.get(), amount_entry.get(), date_entry.get(),
            note_entry.get(),clicked_pocket.get()))

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

    def get_options_for_dropdown(self,serve,get_pockets):
        if get_pockets:
            return serve.get_pockets()
        else:
            return serve.get_events_by_type(self.event_type)

    def add_select_dropdown(self, options, clicked, label,grid_row):
        clicked.set(options[0])
        type_label = Label(self, text=label,)
        type_label.grid(column=0,row=grid_row,sticky=W,padx=2)
        dropdown = OptionMenu(self, clicked, *options)
        dropdown.grid(column=1,row=grid_row,sticky=W)

    def save_event(self, serve, types, pockets, event_type, amount, current_date,
                   note, pocket):
        used_pocket = None
        for t in types:
            if t.get_name() == event_type:
                event_type = t.get_id()
                break

        for a in pockets:
            if a.get_name() == pocket:
                used_pocket = a
                pocket = a.get_id()
                break

        type_of_event = str(type(self.event_type))
        if "income" in type_of_event:
            serve.insert_event(True,amount,event_type, current_date, note, pocket)
            serve.update_pocket_amount(used_pocket.get_id(), (used_pocket.get_amount() + int(amount)))
            self.show_popup_message(global_constants.SUCCESS_OPERATION)
        else:
            if used_pocket.get_amount() < int(amount):
                self.show_popup_message(global_constants.AMOUNT_GRATER_THAN_POCKET_AMOUNT)
            else:
                serve.insert_event(False,amount,event_type, current_date, note, pocket)
                serve.update_pocket_amount(used_pocket.get_id(), (used_pocket.get_amount() - int(amount)))
                self.show_popup_message(global_constants.SUCCESS_OPERATION)

    def show_popup_message(self,message):
        error_popup = PopupGenericMessage(self.root, message)
        error_popup.grab_set()
        self.wait_window(error_popup)

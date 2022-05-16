from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar, E, W


class PopNewType(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root, type):
        Toplevel.__init__(self, root)
        self.root = root
        self.grab_set()
        self.type = type

    def create_and_show_popup(self,serve):

        type_name_label = Label(self, text="Name: ")
        type_name_entry = Entry(self)

        type_note_label = Label(self, text="Note: ")
        type_note_entry = Entry(self)

        save_button = Button(self,text="Save",
                             command=lambda: self.save(serve,type_name_entry.get(),type_note_entry.get()))
        cancel_button = Button(self,text="Close", command=self.destroy)

        title_label = Label(self, text="==== New " + str(self.type) + " ====")
        title_label.grid(column=0,row=0,columnspan=2)
        type_name_label.grid(column=0,row=1)
        type_name_entry.grid(column=1,row=1)

        type_note_label.grid(column=0,row=2)
        type_note_entry.grid(column=1,row=2)

        save_button.grid(column=0,row=3,pady=7,sticky=(E, W))
        cancel_button.grid(column=1,row=3,pady=7,sticky=(E, W))

    def save(self,serve,name, note):
        if self.type:
            serve.insert_expense_type(name,note)
        else:
            serve.insert_income_type(name,note)
        serve.show_popup_message(self.root, "Success!")

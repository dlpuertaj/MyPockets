from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar

class PopNewType(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.root = root
        self.grab_set()

    def create_and_show_popup(self,serve):

        type_name_label = Label(self, text="Name")
        type_name_entry = Entry(self)

        type_note_label = Label(self, text="Note")
        type_note_entry = Entry(self)

        save_button = Button(self,text="Save",
                             command=lambda: self.save(serve,type_name_entry.get(),type_note_entry.get()))
        cancel_button = Button(self,text="Cancel", command=self.destroy)

        type_name_label.pack()
        type_name_entry.pack()

        type_note_label.pack()
        type_note_entry.pack()

        save_button.pack()
        cancel_button.pack()

    def save(self,serve,name, note):
        serve.insert_expense_type(name,note)
        serve.show_popup_message(self.root, "Success!")

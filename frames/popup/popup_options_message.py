from tkinter import Toplevel, Button, Label

""" Generic popup for error, alert or any message"""
class PopupOptionsMessage(Toplevel):

    def __init__(self, root,message):
        Toplevel.__init__(self,root)
        self.title("Message")
        self.root = root
        self.message = message
        self.show_popup()
        self.choice = "no"

    def show_popup(self):
        message_label = Label(self, text=self.message)
        yes_button = Button(self, text="Yes", command=lambda: self.set_choice("yes"))
        no_button = Button(self, text="No", command=lambda : self.set_choice("no"))
        message_label.pack()
        yes_button.pack()
        no_button.pack()

    def set_choice(self, clicked_choice):
        self.choice = clicked_choice

    def get_choice(self):
        return self.choice

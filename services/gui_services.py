from tkinter import Toplevel, Label, Button

from frames.popup.popup_message import PopupGenericMessage


def show_popup_message(root, message):
    error_popup = PopupGenericMessage(root, message)
    error_popup.grab_set()
    root.wait_window(error_popup)

def show_choice_popup(root, choice_variable):
    popup = Toplevel(root)

    def set_choice(choice):
        choice_variable = choice
        popup.destroy()

    popup.title("Alert!")
    popup.geometry("150x120")

    popup_label = Label(popup, text="Are you sure?")

    popup_label.grid(column=0,row=0)
    yes_button = Button(popup, text="YES", command=lambda:set_choice("Yes"))
    no_button = Button(popup, text="NO", command=lambda:set_choice("No"))
    yes_button.grid(column=0, row=1)
    no_button.grid(column=2, row=1)

    popup.grab_set()
    root.wait_window(popup)
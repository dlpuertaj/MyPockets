from frames.popup.popup_message import PopupGenericMessage


def show_popup_message(root, message):
    error_popup = PopupGenericMessage(root, message)
    error_popup.grab_set()
    root.wait_window(error_popup)
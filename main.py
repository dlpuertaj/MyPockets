from frames.window_manager import WindowManager as wm


def main():
    app = wm()

    app.create_popup_login()

    app.root.mainloop()


if __name__ == "__main__":
    main()
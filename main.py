from frames.window_manager import WindowManager as wm


def run(app):
    app.root.mainloop()


if __name__ == "__main__":
    run(wm())
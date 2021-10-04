from frames.window_manager import WindowManager as wm

def instantiate_app():
    return wm()

def run(app):
    app.root.mainloop()


if __name__ == "__main__":
    app = instantiate_app()
    run(app)
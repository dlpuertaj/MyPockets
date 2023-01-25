from frames.window_manager import WindowManager as pockets
from services import data_services


def run(app):
    app.root.mainloop()


if __name__ == "__main__":
    run(pockets(data_services.get_database_connection()))
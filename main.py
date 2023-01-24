from frames.window_manager import WindowManager as wm
from services import data_services


def run(app):
    app.root.mainloop()


if __name__ == "__main__":
    database_connection = data_services.get_database_connection()
    run(wm(database_connection))
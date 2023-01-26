from frames.window_manager import WindowManager as pockets
from services import db_services


def run(app):
    app.root.mainloop()


if __name__ == "__main__":
    run(pockets(db_services.get_database_connection()))
DATABASE = "database/pockets.db"
USER_DB = "root"
PASSWORD_DB = "root"
HOST_DB = "localhost"

# SQLITE #
CREATE_TABLE_USER = """ CREATE TABLE IF NOT EXISTS user (
                         id integer PRIMARY KEY,
                         first_name text NOT NULL,
                         last_name text NOT NULL,
                         email text NOT NULL,
                         username text NOT NULL UNIQUE,
                         password text NOT NULL)"""

INSERT_INTO_USER = """ INSERT INTO user (first_name,last_name,email,username,password)
                            VALUES (?,?,?,?,?)"""

SEARCH_USER_BY_USERNAME = """ SELECT * FROM user WHERE username = ? """

SEARCH_USER_BY_USERNAME_AND_PASSWORD = """ SELECT * FROM user WHERE username = ? AND password = ?"""

SELECT_POCKETS = "SELECT * FROM pocket"

GET_EXPENSE_TYPES = "SELECT * FROM expense_type"

GET_INCOME_TYPES = "SELECT * FROM income_type"

GET_EXPENSE_TYPE_NAMES = "SELECT expense_name FROM expense_type"

GET_INCOME_TYPE_NAMES = "SELECT income_name FROM income_type"

GET_EXPENSE_SUM_BY_TYPE_AND_MONTH = """SELECT t.expense_name as type, SUM(e.expense_amount) as amount 
    FROM expense_event e
    INNER JOIN expense_type t
    ON e.expense_type = t.id
    WHERE strftime('%m', e.expense_date) = ?
    GROUP BY t.expense_name;"""

GET_PAYROLL_BY_MONTH = """SELECT income_amount FROM income_event WHERE income_type = 1 
AND strftime('%m', income_date) = ?"""

GET_INCOME_EVENTS_BY_MONTH = "SELECT * FROM income_event WHERE strftime('%m', income_date) = ?"

GET_INCOME_EVENTS_WITH_NAME_BY_MONTH = """SELECT t.income_name, e.income_amount, e.income_date, e.description, 
    a.name FROM income_event e 
    INNER JOIN income_type t ON e.income_type = t.id
    INNER JOIN pocket a ON e.pocket = a.id 
    WHERE strftime('%m', e.income_date) = ?;
    """

GET_EXPENSE_EVENTS_WITH_NAME_BY_MONTH = """SELECT t.expense_name, e.expense_amount, e.expense_date, e.description, 
    a.name FROM expense_event e 
    INNER JOIN expense_type t ON e.expense_type = t.id
    INNER JOIN pocket a ON e.pocket = a.id 
    WHERE strftime('%m', e.expense_date) = ?
    """

GET_EXPENSE_EVENTS_BY_MONTH = "SELECT * FROM expense_event WHERE strftime('%m',expense_date) = ?"

GET_EXPENSE_TYPE_BY_ID = "SELECT * FROM expense_type WHERE expense_id = ?"

INSERT_EXPENSE_TYPE = "INSERT INTO expense_type (expense_name,note) VALUES (?,?,?)"

INSERT_INCOME_TYPE = "INSERT INTO income_type (income_name,note) VALUES (?,?)"

INSERT_EXPENSE_EVENT = """INSERT INTO expense_event (expense_amount, expense_type, expense_date, description, pocket)
VALUES (?, ?, ?, ?, ?)"""

INSERT_INCOME_EVENT = """INSERT INTO income_event (income_amount, income_type, income_date, description, pocket)
VALUES (?, ?, ?, ?, ?)"""

""" POCKETS """

INSERT_POCKET = """INSERT INTO pocket (name,amount) VALUES (?,?)"""

SELECT_POCKET_BY_NAME = """SELECT name FROM pocket WHERE name = ?"""

UPDATE_POCKET_AMOUNT_BY_NAME = """UPDATE pocket SET amount = ? WHERE name = ?"""

UPDATE_POCKET_NAME_BY_ID = """UPDATE pocket SET name = ? WHERE id = ?"""

UPDATE_POCKET_BY_ID = """UPDATE pocket SET name = ?, amount = ? WHERE id = ?"""

DELETE_POCKET_BY_NAME = """DELETE FROM pocket WHERE name = ?"""

""" TRANSACTIONS """
INSERT_TRANSACTION = """INSERT INTO pocket_transaction 
(pocket_id, target_pocket_id, amount, transaction_date) VALUES (?,?,?,?)"""

SELECT_TRANSACTIONS_BY_POCKET_ID = """SELECT * FROM pocket_transaction WHERE pocket_id = ? OR 
(pocket_id IS NULL AND target_pocket_id = ?)"""

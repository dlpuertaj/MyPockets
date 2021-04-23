DATABASE = "pockets.bd"
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


GET_ACCOUNT_DATA_BY_ID = "SELECT * FROM account WHERE id = ?"

SELECT_POCKETS = "SELECT * FROM pocket"

GET_EXPENSE_TYPES = "SELECT expense_name FROM expense_type"

GET_EXPENSE_SUM_BY_TYPE_AND_MONTH = """SELECT t.expense_name as type, SUM(e.expense_amount) as amount 
FROM expense_event e
INNER JOIN expense_type t
ON e.expense_type = t.id
WHERE strftime('%m', e.expense_date) = ?
GROUP BY t.expense_name;"""

GET_PAYROLL_BY_MONTH = "SELECT income_amount FROM income_event WHERE income_type = 1 AND strftime('%m', income_date) = ?"
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


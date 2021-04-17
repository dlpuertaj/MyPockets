PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user(
id integer PRIMARY KEY,
first_name text NOT NULL,
last_name text NOT NULL,
email text NOT NULL,
username text NOT NULL,
password text NOT NULL);
INSERT INTO user VALUES(1,'David','Puerta','dlpuerta@gmail.com','dlpuerta','123');

CREATE TABLE account(
id integer PRIMARY KEY,
name text NOT NULL,
amount integer NOT NULL);

INSERT INTO account VALUES(1,'Ahorros',100)

CREATE TABLE expense_type(
id integer PRIMARY KEY,
expense_name text NOT NULL);

CREATE TABLE income_type(
id integer PRIMARY KEY,
income_name text NOT NUL);

CREATE TABLE expense_event(
id integer PRIMARY KEY,
expense_amount integer NOT NULL,
expense_type integer NOT NULL,
expense_date text NOT NULL,
description text NOT NULL,
FOREIGN KEY(expense_type) REFERENCES expense_type(id));

CREATE TABLE income_event(
id integer PRIMARY KEY,
income_amount integer NOT NULL,
income_type integer NOT NULL,
income_date text NOT NULL,
description text NULL,
FOREIGN KEY(income_type) REFERENCES income_type(id));


COMMIT;

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

INSERT INTO account VALUES(1,'Savings',100);
INSERT INTO account VALUES(2,'Other',50);

CREATE TABLE pocket(
id integer PRIMARY KEY,
name text NOT NULL,
amount integer NOT NULL
);
INSERT INTO pocket VALUES(1,'Other',500);

CREATE TABLE expense_type(
id integer PRIMARY KEY,
expense_name text NOT NULL,
Note text NULL);

INSERT INTO  expense_type VALUES(1,'Services','');
INSERT INTO  expense_type VALUES(2,'Food','');
INSERT INTO  expense_type VALUES(3,'People','');

CREATE TABLE income_type(
id integer PRIMARY KEY,
income_name text NOT NULL,
Note text NULL);

INSERT INTO  income_type VALUES(1,'Salary','');
INSERT INTO  income_type VALUES(2,'Other','');

CREATE TABLE expense_event(
id integer PRIMARY KEY,
expense_amount integer NOT NULL,
expense_type integer NOT NULL,
expense_date text NOT NULL,
description text NOT NULL,
FOREIGN KEY(expense_type) REFERENCES expense_type(id));

INSERT INTO  expense_event VALUES(1,50,1,'2021-04-15','Tigo');
INSERT INTO  expense_event VALUES(2,50,2,'2021-04-15','Movistar');

CREATE TABLE income_event(
id integer PRIMARY KEY,
income_amount integer NOT NULL,
income_type integer NOT NULL,
income_date text NOT NULL,
description text NULL,
FOREIGN KEY(income_type) REFERENCES income_type(id));


COMMIT;

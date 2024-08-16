-- DROP DATABASE bank_konto_verwaltung;

CREATE DATABASE IF NOT EXISTS bank_konto_verwaltung;

USE bank_konto_verwaltung;

CREATE TABLE IF NOT EXISTS Bank (
	bic VARCHAR(20) PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Customer(
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
	bank_bic VARCHAR(20) NOT NULL,
    FOREIGN KEY (bank_bic) REFERENCES Bank(bic) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Account(
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    iban VARCHAR(50) NOT NULL UNIQUE,
	balance DECIMAL(10, 2) NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SaveAccount(
    account_id INT PRIMARY KEY REFERENCES Account(account_id) ON DELETE CASCADE
    interest_rate DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS CurrentAccount(
    account_id INT PRIMARY KEY REFERENCES Account(account_id) ON DELETE CASCADE,
	overdraft_limit DECIMAL(10, 2) NOT NULL
);


CREATE VIEW AllAccounts AS
SELECT a.account_id, a.iban, a.balance, a.customer_id, sa.interest_rate, ca.overdraft_limit
FROM SaveAccount sa RIGHT JOIN
Account a ON sa.account_id = a.account_id
LEFT JOIN currentaccount ca ON a.account_id = ca.account_id;

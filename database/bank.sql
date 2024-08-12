-- DROP DATABASE bank_konto_verwaltung;

CREATE DATABASE IF NOT EXISTS bank_konto_verwaltung;

USE bank_konto_verwaltung;

CREATE TABLE IF NOT EXISTS Bank (
	bic VARCHAR(11) PRIMARY KEY,
    bcn VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS Customer(
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
	bank_bic VARCHAR(50) NOT NULL,
    FOREIGN KEY (bank_bic) REFERENCES Bank(bic)
);

create database if not exists bank_konto_verwaltung;

use bank_konto_verwaltung;

create table if not exists Bank (
	bic varchar(11) primary key,
    blz varchar(10),
    name varchar(50),
    anschrift varchar(100)
);

create table if not exists Customer (
	customer_id int primary key auto_increment,
    name varchar(50),
	bank_bic varchar(50),
    foreign key (bank_bic) references Bank(bic)
);


create table if not exists Save_Account(
    iban varchar(27) primary key,
    bank_bic varchar(11),
    customer_id int,
    starting_balance decimal(10,2),
    account_status decimal(10,2),
    interest decimal(5,2),
    foreign key (bank_bic)	references Bank(bic),
    foreign key (customer_id) references Customer(customer_id)
);

create table if not exists current_account(
    iban varchar(27) primary key,
    bank_bic varchar(11),
    customer_id int,
    starting_balance decimal(10,2),
    account_status decimal(10,2),
    overdraft_limit decimal(7,2),
    foreign key (bank_bic)	references Bank(bic),
    foreign key (customer_id) references Customer(customer_id)
);

-- ----------------------------------------------------------------


-- Einfügen von Banken
insert into bank (bic, blz, name, anschrift) values ('FRSPDE66XXX', '68050101', 'Sparkasse Freiburg-Nördlicher Breisgau', 'Weingarten, Freiburg');
insert into bank (bic, blz, name, anschrift) values ('MARKDEF1100', '10000000', 'Bundesbank', 'Weingarten, Freiburg');
insert into bank (bic, blz, name, anschrift) values ('PBNKDEFFXXX', '10010010', 'Postbank Ndl der Deutsche', 'Berlin');
insert into bank (bic, blz, name, anschrift) values ('QNTODEB2XXX', '10010123', 'OLINDA Zweigniederlassung', 'Berlin');
insert into bank (bic, blz, name, anschrift) values ('REVODEB2XXX', '10010178', 'Revolut Bank, Zweigniederlassung', 'Berlin');
insert into bank (bic, blz, name, anschrift) values ('GENODEF1OGK', '10030600', 'North Channel Bank', 'Mainz');
insert into bank (bic, blz, name, anschrift) values ('DLGHDEB1XXX', '10030700', 'Eurocity Bank', 'Frankfurt am Main');
insert into bank (bic, blz, name, anschrift) values ('COBADEFFXXX', '10045050', 'Commerzbank Service-BZ', 'Berlin');


-- Einfügen von Kunden
insert into customer (name, bank_bic) values ('Anja Haus', 'COBADEFFXXX');
insert into customer (name, bank_bic) values ('Ramona Krause', 'DLGHDEB1XXX');
insert into customer (name, bank_bic) values ('Stefan Hashage', 'COBADEFFXXX');
insert into customer (name, bank_bic) values ('Sybille Großbaum', 'MARKDEF1100');
insert into customer (name, bank_bic) values ('Hasan Kaymaz', 'COBADEFFXXX');
insert into customer (name, bank_bic) values ('Michael Jackson', 'GENODEF1OGK');
insert into customer (name, bank_bic) values ('Micky Maus', 'QNTODEB2XXX');
insert into customer (name, bank_bic) values ('Sven Dietenbach', 'MARKDEF1100');
insert into customer (name, bank_bic) values ('Sabine Voges', 'FRSPDE66XXX');


-- Einfügen von Sparkonten
insert into Save_Account (iban, bank_bic, customer_id, starting_balance, account_status, interest)
	values ('DE19 5634 0101 3256 7754 89', 'COBADEFFXXX', 1, 2500, -1, 2);
insert into Save_Account (iban, bank_bic, customer_id, starting_balance, account_status, interest)
	values ('DE39 5555 3434 6756 1234 56', 'QNTODEB2XXX', 4, 180000, -1, 2);
insert into Save_Account (iban, bank_bic, customer_id, starting_balance, account_status, interest)
	values ('DE54 7655 6766 2334 6757 99', 'MARKDEF1100', 2, 19750, -1, 1);
insert into Save_Account (iban, bank_bic, customer_id, starting_balance, account_status, interest)
	values ('DE64 2356 4677 8786 5445 22', 'FRSPDE66XXX', 5, 35000, -1, 3);
insert into Save_Account (iban, bank_bic, customer_id, starting_balance, account_status, interest)
	values ('DE22 2323 4677 5555 5445 23', 'FRSPDE66XXX', 9, 7800, -1, 4);


-- Einfügen von Giro konten
insert into current_account (iban, bank_bic, customer_id, starting_balance, account_status, overdraft_limit)
	values ('DE21 1111 2222 5555 5445 54', 'FRSPDE66XXX', 9, 5000, -1, 40);
insert into current_account (iban, bank_bic, customer_id, starting_balance, account_status, overdraft_limit)
	values ('DE23 5423 4565 9877 8265 23', 'DLGHDEB1XXX', 3, 50000, -1, 400);
insert into current_account (iban, bank_bic, customer_id, starting_balance, account_status, overdraft_limit)
	values ('DE34 5677 2222 7656 5656 77', 'COBADEFFXXX', 4, 4500, -1, 240);
insert into current_account (iban, bank_bic, customer_id, starting_balance, account_status, overdraft_limit)
	values ('DE77 1843 5677 7657 8788 88', 'COBADEFFXXX', 5, 76600, -1, 3340);
insert into current_account (iban, bank_bic, customer_id, starting_balance, account_status, overdraft_limit)
	values ('DE56 7890 6666 9876 8957 99', 'DLGHDEB1XXX', 6, 1250900, -1, 3340);
insert into current_account (iban, bank_bic, customer_id, starting_balance, account_status, overdraft_limit)
	values ('DE26 0000 5445 5496 2996 29', 'MARKDEF1100', 7, 56000, -1, 460);

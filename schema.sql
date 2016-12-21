DROP TABLE if exists accounts;
DROP TABLE if exists balances;
DROP TABLE if exists customers;
DROP TABLE if exists events;
DROP TABLE if exists transactions;
DROP TABLE if exists settings;
CREATE TABLE accounts (
    account_type TEXT NOT NULL,
    active INTEGER NOT NULL,
    account_number INTEGER PRIMARY KEY AUTOINCREMENT,
    last_event_time TEXT NOT NULL,
    last_event_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    balance REAL NOT NULL DEFAULT 0
    );
CREATE TABLE balances (
    event_id INTEGER,
    balance DECIMAL NOT NULL,
    account_number INTEGER NOT NULL
    );
CREATE TABLE customers (
    customer_name TEXT NOT NULL,
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mobile_number TEXT UNIQUE NOT NULL
    );
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    event_type TEXT NOT NULL
    );
CREATE TABLE transactions (
    event_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    originator INTEGER NOT NULL,
    beneficiary INTEGER NOT NULL,
    reference TEXT NOT NULL
    );
CREATE TABLE settings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    savings_rate REAL NOT NULL,
    close_of_biz TEXT NOT NULL,
    compound_int_type TEXT NOT NULL
)

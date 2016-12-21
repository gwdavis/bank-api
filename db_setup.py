#!flask/bin/python
# import sqlite3
from db_helper import *
from models import *


########################################################################
# Populate tables
########################################################################

def main():

    # Note: There is a lot of customization in create_bank_api_tables
    with open('schema.sql', mode='r') as f:
        c.executescript(f.read())

    # Add customers from models
    for row in customers:
        clean_row = removekey(row, 'customer_id')
        add_new_customer(**clean_row)

    # initialize treasury account manually to set an intial
    # account number
    initialize_treasury_account(12345678, 200000)

    # Add accounts from models
    for row in accounts:
        # pull k,v from accounts for select keys
        clean_row = {k: row[k] for k in row
                     if k in set(['customer_id',
                                  'account_type'])}
        # add a new key
        clean_row.update({"initial_deposit": 0})
        add_new_account(**clean_row)

    # To Do = Refactor settings table to use these tables
    # c.execute("""INSERT INTO defaults (savings_rate, close_of_biz, compound_int_type)
    #     VALUES ({sr}, "{cb}", "{cit}")""".format(sr=10.0, cb='24:59:59', cit='continuous'))
    # # Add to settings - hard code
    # c.execute("""INSERT INTO settings (savings_rate, close_of_biz,
    #     compound_int_type) VALUES ({sr}, "{cb}", "{cit}")
    #         """.format(sr=0.0125, cb='19:59:59', cit='continuous'))

    conn.commit()
    conn.close()


#########################################################################
#  Functions
##########################################################################

# def create_bank_api_tables():
#     """Creates table from models.py """
#     def make_table(table_name, source):
#         """Create tables from models.py """
#         fields = ""
#         for fn in source:
#             f = '{fn} {fe},'.format(fn=fn, fe=source[fn])
#             fields += f
#         if fields[-1:] == ',':
#             fields = fields[:-1]
#         try:
#             c.execute('DROP TABLE {tn};'.format(tn=table_name))
#         except:
#             pass
#         # print('CREATE TABLE {tn} ({f})'.format(tn=table_name, f=fields))
#         c.execute('CREATE TABLE {tn} ({f});'.format(tn=table_name, f=fields))

#     make_table('accounts', Accounts)
#     make_table('balances', Balances)
#     make_table('customers', Customers)
#     make_table('events', Events)
#     make_table('transactions', Transactions)
#     make_table('settings', Settings)
#     # To Do - Refactor settings module to use these tables
#     # make_table('defaults', Defaults)
#     return


def removekey(d, key):
    """remove selected key from dict and return new dict"""
    r = dict(d)
    del r[key]
    return r


def initialize_treasury_account(account_number, initial_deposit):
    """Insert first account record manually to set the account
    number to start the increment"""
    new_event = add_new_event('New Account')
    c.execute("""
        INSERT INTO accounts (account_number, customer_id,
            account_type, last_event_id, last_event_time,
            balance, active)
        VALUES ({an}, {ci}, "{t}", {lei}, "{let}", {b}, {a})
        """.format(an=account_number, ci=1, t='dda',
                   lei=new_event['event_id'],
                   let=new_event['timestamp'],
                   b=initial_deposit, a=1))


###########################################################################
# Create a table - simple and straight forward
###########################################################################
# try:
#     c.execute('''DROP TABLE Accounts''')
# except:
#     pass

# c.execute('''CREATE TABLE Accounts(
#                 account_number    INTEGER PRIMARY KEY AUTOINCREMENT,
#                 customer_id     INTEGER NOT NULL,
#                 customer_name   TEXT NOT NULL,
#                 type            TEXT NOT NULL,
#                 balance         REAL NOT NULL,
#                 last_event_id   REAL NOT NULL,
#                 last_event_time REAL NOT NULL,
#                 active          INTEGER NOT NULL 
#                 )''')
# c.execute("""INSERT INTO Accounts VALUES (12345678,
#                                           1, 
#                                           'Treasury', 
#                                           'DDA', 
#                                           100000, 
#                                           1, 
#                                           1479444205.588373,1) """)
# conn.commit()
# conn.close()
# 

main()
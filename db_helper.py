import sqlite3
from datetime import datetime


#########################################################################
# Set up Database
#########################################################################
# Source:
# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

sqlite_file = 'bankapi_db.sqlite'


# Connecting to the database file
conn = sqlite3.connect(sqlite_file, check_same_thread=False)
# Set row factory to address rows by tuple and column name
conn.row_factory = sqlite3.Row
c = conn.cursor()


#########################################################################
# def add_new_account(initial_deposit, customer_id, account_type):
#     """add new account to Accounts, return account object
#     Parms:  initial deposit
#             customer id
#             account type
#     """

#     def new_account_number():
#         """return the highest current event_id plus 1"""
#         seq = [a['account_number'] for a in Accounts]
#         return max(seq) + 1
#     customer_name = get_customer(customer_id)['customer_name']
#     new_account = {
#         'customer_id': customer_id,
#         'customer_name': customer_name,
#         'account_number': new_account_number(),
#         'type': 'account_type',
#         'balance': 0,
#         'active': True
#         }
#     Accounts.append(new_account)
#     return new_account
#########################################################################

def add_new_account(initial_deposit, customer_id, account_type):
    """add new account to Accounts, return account object
    Parms:  initial deposit
            customer id
            account type
    """

    new_event = add_new_event('New Account')
    c.execute("""
        INSERT INTO accounts (customer_id, account_type, last_event_id,
                              last_event_time, balance, active)
        VALUES ({ci}, "{t}", {lei}, "{let}", {b}, {a});""".format(
                ci=customer_id, t=account_type, lei=new_event['event_id'],
                let=new_event['timestamp'], b=0, a=1))
    new_account = {
        'customer_id': customer_id,
        # 'customer_name': customer_name,
        'account_number': c.lastrowid,
        'account_type': account_type,
        'last_event_id': new_event['event_id'],
        'last_event_time': new_event['timestamp'],
        'balance': 0,
        'active': 1
    }
    conn.commit()
    return new_account


def add_new_event(event_type):
    """Add new event to Events, returns new event object
    Parms: event type as string"""
    ts = datetime.now().isoformat()
    c.execute("""
        INSERT INTO events (timestamp, event_type)
        VALUES ("{ts}", "{et}");""".format(ts=ts, et=event_type))
    new_event = {
        "event_id": c.lastrowid,
        "timestamp": ts,
        "event_type": event_type
    }
    conn.commit()
    return new_event


def add_new_balance(event_id, balance_amount, account_number):
    """Add updated balance to database
    parms:  event object
            amount
            accountnumber
            """
    c.execute("""
        INSERT INTO balances (event_id, balance, account_number)
        VALUES ({ei}, {ba}, {an});""".format(ei=event_id,
                                             ba=balance_amount,
                                             an=account_number))
    # balance = {"event_id": event_id,
    #            "balance": balance_amount,
    #            "account_number": account_number}
    conn.commit()
    # Balances.append(balance)
    return


def customer_true(customer_id):
    c.execute("""
        SELECT * FROM customers
        WHERE customer_id={} LIMIT 1;""".format(customer_id))

    # customer = json.dumps(dict(c.fetchone()))
    customer = dict(c.fetchone())
    return customer


def mobile_number_unique(mobile_number):
    '''compare arg to existing customer's mobile numbers, if
    unique return number'''
    # TO DO - string format in database includes the literal ""
    # NOTE kwarg for importing data!!!!!  Cool
    c.execute("""
        SELECT * FROM customers
        WHERE mobile_number={}""".format(mobile_number))
    exists = c.fetchone()
    if exists:
        return
    else:
        return mobile_number

# def add_new_customer(customer_name, mobile_number):
#     # def new_customer_id():
#         # seq = [c['customer_id'] for c in Customers]
#         # return max(seq) + 1
#     new_customer = {
#                     'customer_name': customer_name,
#                     'mobile_number': mobile_number}
#     Customers.append(new_customer)
#     return new_customer


def add_new_customer(customer_name, mobile_number):
    c.execute("""
        INSERT INTO customers (customer_name, mobile_number)
        VALUES ("{cn}", '{mn}');""".format(cn=customer_name, mn=mobile_number))
    new_customer = {'customer_id': c.lastrowid,
                    'customer_name': customer_name,
                    'mobile_number': mobile_number}
    conn.commit()
    return new_customer


def add_new_transaction(transaction):
    """Add new transaction to database"""
    c.execute("""
        INSERT INTO transactions (event_id, originator, beneficiary,
                                  amount, reference)
        VALUES ({ei}, {orig}, {be}, {am}, '{re}');
        """.format(ei=transaction['event_id'],
                   orig=transaction['originator'],
                   be=transaction['beneficiary'],
                   am=transaction['amount'],
                   re=transaction['reference']
                   ))
    conn.commit()


def get_account(account_number):
    """return account if account number exists"""
    try:
        c.execute("""
        SELECT * FROM accounts 
        WHERE account_number={}""".format(account_number))
        return dict(c.fetchone())
    except:
        return None


def get_all_accounts():
    """Returns Accounts"""
    accounts = []
    for row in c.execute("""SELECT * FROM accounts;"""):
        accounts.append(dict(row))
    return accounts


def get_customer(customer_id):
    '''return customer if customer id  exists'''
    c.execute("""
        SELECT * FROM customers 
        WHERE customer_id={}""".format(customer_id))
    return dict(c.fetchone())


def get_all_customers():
    """Returns Customers"""
    customers = []
    for row in c.execute("""SELECT * FROM customers;"""):
        customers.append((dict(row)))
    return customers


def get_customer_accounts(customer_id):
    """Returns list of accounts as dict for customers id"""
    account_list = []
    for a in c.execute("""
            SELECT * FROM accounts
            WHERE customer_id={}""".format(customer_id)):
        account_list.append(dict(a))
    return account_list


def get_all_events():
    """Returns Events"""
    events = []
    for row in c.execute("""SELECT * FROM events;"""):
        events.append((dict(row)))
    return events


def update_account_balance(account_number, balance,
                           latest_event_id, latest_event_timestamp):
    a = get_account(account_number)

    a.update({'balance': balance,
              'latest_event_id': latest_event_id,
              'latest_event_timestamp': latest_event_timestamp})
    c.execute("""
        UPDATE accounts 
        SET balance = {bl},
        last_event_id = "{lei}", last_event_time = "{lets}"
        WHERE account_number = {an};""".format(bl=balance,
                                               lei=latest_event_id,
                                               lets=latest_event_timestamp,
                                               an=account_number))

    conn.commit()
    return


# def get_variables(table, column):
#     """Return variables from column in table as dict."""
#     c.execute("""SELECT {dc} FROM {dt};
#         """.format(dt=table, dc=column))
#     v = dict(c.fetchone())[column]
#     # return p as a dict
#     return eval(v)

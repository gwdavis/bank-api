#!flask/bin/python

########################################################################
# Table Definitions
########################################################################

Accounts = {
        'customer_id': "INTEGER NOT NULL",  # integer
        # 'customer_name': "TEXT NOT NULL",  # string
        'account_number': "INTEGER PRIMARY KEY AUTOINCREMENT",  # int
        'account_type': "TEXT NOT NULL",  # string
        'balance': "REAL NOT NULL DEFAULT 0",  # deprecated
        'last_event_id': "INTEGER NOT NULL",  # integer
        'last_event_time': "TEXT NOT NULL",  # decimal
        'active': "INTEGER NOT NULL"  # boolean
    }

Balances = {
        'event_id': "INTEGER",  # integer
        'account_number': "INTEGER NOT NULL",  # string
        'balance':  "DECIMAL NOT NULL"  # decimal
    }

Customers = {
        'customer_id': "INTEGER PRIMARY KEY AUTOINCREMENT",
        'customer_name': "TEXT NOT NULL",
        'mobile_number': "TEXT NOT NULL"  # string reg-ex
    }

Events = {
        'event_id': "INTEGER PRIMARY KEY AUTOINCREMENT",
        'timestamp': "REAL NOT NULL",  # seconds since epoch
        'event_type': "TEXT NOT NULL",  # string
    }

Transactions = {
        'event_id': "INTEGER NOT NULL",  # integer
        'originator': "INTEGER NOT NULL",  # string
        'beneficiary': "INTEGER NOT NULL",  # string
        'amount': "REAL NOT NULL",  # decimal
        'reference': "TEXT NOT NULL"  # string
    }

Parms = {
        'var_id': "INTEGER PRIMARY KEY AUTOINCREMENT",
        'var_json': "TEXT NOT NULL"
    }

Defaults = {
        'var_id': "INTEGER PRIMARY KEY AUTOINCREMENT",
        'var_json': "TEXT NOT NULL"
    }

########################################################################
# Data
########################################################################


defaults = {
        'close_of_biz': '24:59:59',
        'compound': 'c'
    }

parms = {'savings_rate': 0.0125,
         'close_of_biz': '20:00:00',
         'compound': 'c'
         }

accounts = [
    {
        'customer_id': 1,  # integer
        'customer_name': u'treasury',  # string
        'account_number': 12345678,  # int
        'account_type': u'dda',  # string
        'balance': 95000,  # deprecated
        'last_event_id': 4,  # integer
        'last_event_time': 1479444205.588373,  # decimal
        'active': True  # boolean
    },
    {
        'customer_id': 2,
        'customer_name': u'Gary Davis',
        'account_number': 48739278,
        'account_type': u'dda',
        'balance': 1000,
        'last_event_id': 2,
        'last_event_time': 1479444203.588373,
        'active': True
    },
    {
        'customer_id': 3,
        'customer_name': u'Gordon Baird',
        'account_number': 48739777,
        'account_type': u'dda',
        'balance': 2000,
        'last_event_id': 3,
        'last_event_time': 1479444204.588373,
        'active': True
    },
    {
        'customer_id': 3,
        'customer_name': u'Gordon Baird',
        'account_id': 4,
        'account_number': 48739778,
        'account_type': u'savings',
        'interest': True,
        'interest_rate': 'savings_rate',
        'balance': 2000,
        'last_event_id': 4,
        'last_event_time': 1479444205.588373,
        'active': True
    },
    ]

balances = [
    {
        'account_number': 12345678,  # string
        'event_id': 1,  # integer
        'balance':  100000  # decimal
    },
    {
        'account_number': 48739278,
        'event_id': 2,
        'balance':  1000
    },
    {
        'account_number': 12345678,
        'event_id': 2,
        'balance':  99000
    },
    {
        'account_number': 48739777,
        'event_id': 3,
        'balance':  2000
    },
    {
        'account_number': 12345678,
        'event_id': 3,
        'balance':  97000
    },
    {
        'account_number': 48739778,
        'event_id': 4,
        'balance':  2000
    },
    {
        'account_number': 12345678,
        'event_id': 4,
        'balance':  95000
    },
    ]

customers = [
    {
        'customer_id': 1,
        'customer_name': u'treasury',
        'mobile_number': u'212-111-1111'
    },
    {
        'customer_id': 2,
        'customer_name': u'Gary Davis',
        'mobile_number': u'914-419-9788'
    },
    {
        'customer_id': 3,
        'customer_name': u'Gordon Baird',
        'mobile_number': u'203-111-1111'
    }
    ]

events = [
    {
        'event_id': 1,  # integer
        'timestamp': 1479444202.588373,  # seconds since epoch
        'event_type': 'transfer',  # string
    },
    {
        'event_id': 2,  # integer
        'timestamp': 1479444203.588373,
        'event_type': 'transfer',  # string
    },
    {
        'event_id': 3,  # integer
        'timestamp': 1479444204.588373,
        'event_type': 'transfer',  # string
    },
    {
        'event_id': 4,  # integer
        'timestamp': 1479444205.588373,
        'event_type': 'transfer',  # string
    },
    ]

transactions = [
    {
        'event_id': 2,  # integer
        'originator': 12345678,  # string
        'beneficiary': 48739278,  # string
        'amount': -1000,  # decimal
        'reference': u'Initial Deposit'  # string
    },
    {
        'event_id': 2,
        'originator': 48739278,
        'beneficiary': 12345678,
        'amount': 1000,
        'reference': u'Initial Deposit'
    },
    {
        'event_id': 3,
        'originator': 12345678,
        'beneficiary': 48739777,
        'amount': -2000,
        'reference': u'Initial Deposit'
    },
    {
        'event_id': 3,
        'originator': 48739777,
        'beneficiary': 12345678,
        'amount': 2000,
        'reference': u'Initial Deposit'
    },
    {
        'event_id': 4,
        'originator': 12345678,
        'beneficiary': 48739778,
        'amount': -2000,
        'reference': u'Initial Deposit'
    },
    {
        'event_id': 4,
        'originator': 48739778,
        'beneficiary': 12345678,
        'amount': 2000,
        'reference': u'Initial Deposit'
    }
    ]

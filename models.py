#!flask/bin/python



Accounts = [
    {
        'customer_id': 1,
        'customer': u'treasury',
        'account_id': 1,
        'account_number': u'12345678',
        'type': u'dda',
        'balance': 97000,
        'active': True
    },
    {
        'customer_id': 2,
        'customer': u'Gary Davis',
        'account_id': 2,
        'account_number': u'48739278',
        'type': u'dda',
        'balance': 1000,
        'active': True
    },
    {
        'customer_id': 3,
        'customer': u'Gordon Baird',
        'account_id': 3,
        'account_number': u'48739777',
        'type': u'dda',
        'balance': 2000,
        'active': True
    }
]

Customers = [
    {
        'customer_id': 1,
        'customer': u'treasury',
        'mobile_number': u'212-111-1111'
    },
    {
        'customer_id': 2,
        'customer': u'Gary Davis',
        'mobile_number': u'914-419-9788'
    },
    {
        'customer_id': 3,
        'customer': u'Gordon Baird',
        'mobile_number': u'203-111-1111'
    }
]

Transactions = [
    {
        'transaction_id': 1,
        'originator': u'12345678',
        'beneficiary': u'48739278',
        'amount': -1000,
        'reference': u'Initial Deposit'
    },
    {
        'transaction_id': 1,
        'originator': u'48739278',
        'beneficiary': u'12345678',
        'amount': 1000,
        'reference': u'Initial Deposit'
    },
    {
        'transaction_id': 2,
        'originator': u'12345678',
        'beneficiary': u'48739777',
        'amount': -2000,
        'reference': u'Initial Deposit'
    },
    {
        'transaction_id': 2,
        'originator': u'48739777',
        'beneficiary': u'12345678',
        'amount': 2000,
        'reference': u'Initial Deposit'
    }]
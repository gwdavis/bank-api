#!flask/bin/python
from flask import Flask, jsonify, request, url_for

from api_utils import *
from models import *

app = Flask(__name__)

"""
    Bank API Backend
    ----------------
    :copyright: (c) 2016 Gary W Davis
    :license: MIT, see LICENSE for more details.

    Modelled after YABAB by Alexis Hildebrandt 2016

    Uses arrays for a database.  Data model is not really separated.  NOTE: is
    used to indicate some outstanding questions.  Not really sure abou the
    scope of variables.  In coding, it appeared that all variables might be
    global.
"""

__author__  = "Gary W Davis"
__version__ = "0.0.1"
__license__ = "MIT"
__copyright__ = "Copyright 2016, Gary W Davis"
__version__ = "0.0.1"
__api_descr__ = "https://github.com/gwdavis/bank-api/blob/1fa121a9c2da77163ba88d1f939027e89f07ed71/API.md"


###########################################################################
# api_info
###########################################################################
@app.route('/')
@app.route('/api/')
def api_info():
    '''Display API information'''
    response = {'message': 'Welcome to NewBank API',
                'version': '{}'.format(__version__),
                'api documentation': '{}'.format(__api_descr__)
                }
    return jsonify(response)

###########################################################################
# /accounts
###########################################################################


@app.route('/api/accounts',
           methods=['POST', 'GET'],
           defaults={'account_number': None})
@app.route('/api/accounts/<account_number>', methods=['GET'])
def accounts(account_number):
    """Routes requests to `create_account()` or `show_balance()`"""
    if request.method == 'POST':
        return create_account(get_data(request))
    elif request.method == 'GET' and account_number:
        return show_balance(account_number)
    else:
        return list_accounts()


def list_accounts():
    accounts = Accounts
    return jsonify({"accounts": accounts})


def create_account(data):
    """Creates a new account for a customer identified by customer_id.
    Creates transaction records and new balance."""  

    # NOTE - Transaction is assumed
    # to be transfer from Treasury but does not show a transfer from cash or
    # accounts receivable

    mandatory_params = ['customer_id', 'initial_deposit']
    result = check_required_params(mandatory_params, data)
    if result:
        return result

    customer = customer_true(int(data['customer_id']))
    if not customer:
        return error("No customer with id {} found".format(data['customer_id']), 404)
    
    new_account_id = max_account_id() + 1
    new_account_number = str(int(max_account_number()) + 1)
    initial_deposit = int(data['initial_deposit'])
    new_account = {
        'customer_id': customer['customer_id'],
        'customer': customer['customer'],
        'account_id': new_account_id,
        'account_number': new_account_number,
        'type': u'dda',
        'balance': 0,
        'active': True
        }
    (amount, reject) = numeric_amount('initial_deposit', data)
    if reject:
        return reject

    Accounts.append(new_account)
    beneficiary = search_account(new_account_number)
    originator = search_account(u'12345678')

    committed_transaction = commit_transaction(
        originator=originator,
        beneficiary=beneficiary,
        reference="Initial Deposit",
        amount=initial_deposit)

    return jsonify({"transaction id": committed_transaction,
                    "new account": new_account}), 201


def show_balance(account_number):
    """Show the current balance of an account identified by account_number"""
    account = search_account(account_number)
    if not account:
        return error("No account with number {} found".format(account_number), 404)

    balance = account['balance']
    return jsonify({"balance": balance})

##########################################################################
# /transactions
##########################################################################


@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction.
    For every request to this API endpoint two Transaction database entries
    are made in order to have some sort of double entry bookkeeping.
    """
    data = get_data(request)
    mandatory_params = ['amount', 'reference', 'originator', 'beneficiary']
    result = check_required_params(mandatory_params, data)
    if result:
        return result

    (originator, reject) = get_account('originator', data)
    if reject:
        return reject

    (beneficiary, reject) = get_account('beneficiary', data)
    if reject:
        return reject

    (amount, reject) = numeric_amount('amount', data)
    if reject:
        return reject

    committed_transaction = commit_transaction(
        originator=originator,
        beneficiary=beneficiary,
        reference=data['reference'],
        amount=amount)

    return jsonify({"transaction": committed_transaction}), 201


##########################################################################
# /customers
##########################################################################


@app.route('/api/customers',
           methods=['POST', 'GET'],
           defaults={'customer_id': None})
@app.route('/api/customers/<customer_id>', methods=['GET'])
def customers(customer_id):
    """Routes requests to `create_customer()` or `show_customer_accounts()`"""
    if request.method == 'POST':
        return create_customer(get_data(request))
    elif request.method == 'GET' and customer_id:
        return show_customer_accounts(customer_id)
    else:
        return list_customers()


def list_customers():
    """List of all customers and customer_id"""
    customers = Customers

    return jsonify({"accounts": customers})


def show_customer_accounts(customer_id):
    """Show a list of accounts for requested customer_ID"""
    customer_accounts = search_customer_accounts(customer_id)
    if not customer_accounts:
        return error("No accounts for customer with id number {} found".format(customer_id), 404)
    else:
        return jsonify({"accounts": customer_accounts})


def create_customer(data):
    """Creates a new customer for a customer name and mobile number"""
    mandatory_params = ['customer_name', 'mobile_number']
    result = check_required_params(mandatory_params, data)
    if result:
        return result
    mobile_number = mobile_number_unique(data['mobile_number'])
    if not mobile_number:
        return error("There already is a customer with mobile number {} found".format(data['mobile_number']), 404)
    new_customer_id = max_customer_id() + 1
    new_customer = {'customer_id': new_customer_id,
                    'customer_name': data['customer_name'],
                    'mobile_number': mobile_number}
    Customers.append(new_customer)
    return jsonify({'new_customer': new_customer})


###########################################################################

if __name__ == '__main__':
    app.run(debug=True)

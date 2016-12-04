#!flask/bin/python
import time
from flask import Flask, jsonify, request
import api_utils
import db_helper


"""
    Bank API Backend
    ----------------
    :copyright: (c) 2016 Gary W Davis
    :license: MIT, see LICENSE for more details.

    Modelled after YABAB by Alexis Hildebrandt 2016

    Uses SQLITE for a database. Database and access is separated from the
    front-end.

    The term "NOTE:"" is used to indicate some outstanding questions.
"""

__author__ = "Gary W Davis"
__version__ = "0.0.2"
__license__ = "MIT"
__copyright__ = "Copyright 2016, Gary W Davis"
__api_descr__ = "https://github.com/gwdavis/bank-api/blob/master/API.md"


# create application
app = Flask(__name__)


# Set defaults and parameters


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
@app.route('/api/accounts/<int:account_number>', methods=['GET'])
def accounts(account_number):
    """Routes requests to `create_account()` or `show_balance()`"""
    if request.method == 'POST':
        return create_account(api_utils.get_data(request))
    elif request.method == 'GET' and account_number:
        return show_adjusted_balance(account_number)

    else:
        return list_accounts()


def list_accounts():
    accounts = db_helper.get_all_accounts()
    return jsonify({"accounts": accounts})


def create_account(data):
    """Creates a new account and records initial deposit.
    Args:  customer id
            initial deposit
    Creates transaction records and new balance."""

    # NOTE - All deposits come from treasury
    # NOTE - To do: set initial deposit to zero if not provided.

    mandatory_params = ['customer_id', 'initial_deposit']
    result = api_utils.check_required_params(mandatory_params, data)
    if result:
        return result

    customer = db_helper.customer_true(int(data['customer_id']))
    if not customer:
        return api_utils.error("No customer with id {} \
            found".format(data['customer_id']), 404)

    new_account = db_helper.add_new_account(int(data['initial_deposit']),
                                            customer['customer_id'],
                                            u'dda')
    initial_deposit = int(data['initial_deposit'])

    (amount, reject) = api_utils.numeric_amount('initial_deposit', data)
    if reject:
        return reject

    beneficiary = db_helper.get_account(new_account['account_number'])
    originator = db_helper.get_account(12345678)

    committed_transaction = api_utils.commit_transaction(
        originator=originator,
        beneficiary=beneficiary,
        reference="Initial Deposit",
        amount=initial_deposit)

    return jsonify({"transaction id": committed_transaction,
                    "new account": new_account}), 201


def show_adjusted_balance(account_number):
    """Finds latest balance and adjusts for accrued interest rate"""
    account = db_helper.get_account(account_number)
    if not account:
        return api_utils.error("No account with number {} found".format(account_number), 404)

    if account['account_type'] == 'savings':
        balance = api_utils.calc_pv(account['balance'],
                                    account['last_event_time'],
                                    time.time(),
                                    param.savings_rate)
        return jsonify({"balance": balance})

    return jsonify({"balance": account['balance']})

##########################################################################
# /events
##########################################################################


@app.route('/api/events',
           methods=['GET'])
def list_events():
    """List of all events"""
    events = db_helper.get_all_events()
    return jsonify({"events": events})

##########################################################################
# /transactions
##########################################################################


@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction.
    For every request to this API endpoint two Transaction database entries
    are made in order to have some sort of double entry bookkeeping.
    """
    data = api_utils.get_data(request)
    mandatory_params = ['amount', 'reference', 'originator', 'beneficiary']
    result = api_utils.check_required_params(mandatory_params, data)
    if result:
        return result

    (originator, reject) = api_utils.get_designated_account('originator', data)
    if reject:
        return reject

    (beneficiary, reject) = api_utils.get_designated_account('beneficiary', data)
    if reject:
        return reject

    (amount, reject) = api_utils.numeric_amount('amount', data)
    if reject:
        return reject

    committed_transaction = api_utils.commit_transaction(
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
        return api_utils.create_customer(api_utils.get_data(request))
    elif request.method == 'GET' and customer_id:
        return show_customer_accounts(customer_id)
    else:
        return list_customers()


def list_customers():
    """List of all customers and customer_id"""
    customers = db_helper.get_all_customers()

    return jsonify({"customers": customers})


def show_customer_accounts(customer_id):
    """Show a list of accounts for requested customer_ID"""
    customer_accounts = db_helper.get_customer_accounts(customer_id)
    if not customer_accounts:
        return api_utils.error("No accounts for customer with id \
                               number {} found".format(customer_id), 404)
    else:
        return jsonify({"accounts": customer_accounts})


def create_customer(data):
    """Creates a new customer for a customer name and mobile number"""
    mandatory_params = ['customer_name', 'mobile_number']
    result = api_utils.check_required_params(mandatory_params, data)
    if result:
        return result
    mobile_number = db_helper.mobile_number_unique(data['mobile_number'])
    if not mobile_number:
        return api_utils.error("There already is a customer with \
                 mobile number {} found".format(data['mobile_number']), 404)

    new_customer = db_helper.add_new_customer(data['customer_name'],
                                              mobile_number)

    return jsonify({'new_customer': new_customer})


###########################################################################

if __name__ == '__main__':
    app.run(debug=True)

#!flask/bin/python
from flask import Flask, jsonify, request
import api_utils
import account
import transaction
import customer


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
__version__ = "0.0.3"
__license__ = "MIT"
__copyright__ = "Copyright 2016, Gary W Davis"
__api_descr__ = "https://github.com/gwdavis/bank-api/blob/master/API.md"


# create application
app = Flask(__name__)


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
        return account.create_account(api_utils.get_data(request))
    elif request.method == 'GET' and account_number:
        return account.show_adjusted_balance(account_number)

    else:
        return account.list_accounts()


##########################################################################
# /events
##########################################################################
# NOTE - SHould this call be moved to a controller module?  which one?

@app.route('/api/events',
           methods=['GET'])
def events():
    """List of all events"""
    return transaction.list_events()

##########################################################################
# /transactions
##########################################################################


@app.route('/api/transactions', methods=['POST'])
def transactions():
    if request.method == 'POST':
        return transaction.make_payment(api_utils.get_data(request))
    else:
        return transaction.list_transactions()


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
        return customer.create_customer(api_utils.get_data(request))
    elif request.method == 'GET' and customer_id:
        return customer.show_accounts(customer_id)
    else:
        return customer.list_customers()


###########################################################################

if __name__ == '__main__':
    app.run(debug=True)

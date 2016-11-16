#!flask/bin/python
from flask import jsonify, request

from models import Accounts, Transactions, Customers


def search_account(account_number):
    '''return account if account number exists'''
    for a in Accounts:
        if a['account_number'] == account_number:
            return a


def search_customer_accounts(customer_id):
    account_list = []
    for a in Accounts:
        if a['customer_id'] == int(customer_id):
            account_list.append(a)
    return account_list


def customer_true(customer_id):
    for c in Customers:
        if c['customer_id'] == customer_id:
            return c


def mobile_number_unique(mobile_number):
    '''compare arg to existing customer's mobile numbers, if
    unique return number'''
    for c in Customers:
        if c['mobile_number'] == mobile_number:
            return
    return mobile_number


def max_account_id():
    '''return the highest record_id in array containing dictionaries'''
    seq = [r['account_id'] for r in Accounts]
    return max(seq)


def max_account_number():
    '''return the highest record_id in array containing dictionaries'''
    seq = [r['account_number'] for r in Accounts]
    return max(seq)


def max_transaction_id():
    seq = [t['transaction_id'] for t in Transactions]
    return max(seq)


def max_customer_id():
    seq = [c['customer_id'] for c in Customers]
    return max(seq)


def get_data(request):
    """Get data from request either from form-data or json body"""

    # NOTE: something about this seems odd.  It does not seem
    # to need flask.request

    data = request.form
    if not data:
        data = request.get_json()
    return data


def error(message, status=200):
    """Wrap an error message in a response JSON"""
    data = {"status": "error", "reason": message}
    return jsonify(data), status


def check_required_params(params, data):
    """Check if `data` contains list of mandatory parameters `params`"""
    for param in params:
        result = check_required_param(param, data)
        if result:
            return result


def check_required_param(param, data):
    """Check if `data` contains mandatory parameter `param`"""
    if not data:
        return error("Missing mandatory parameter {}".format(param))
    try:
        data[param]
    except KeyError:
        return error("Missing mandatory parameter {}".format(param))
    return None


def get_account(param, data):
    """Return account model if account referenced by number in data exists, 
    error otherwise"""
    account = search_account(data[param])
    if not account:
        return (None, error("Invalid {} account number {}".format(param, data[param])))
    return (account, None)


def numeric_amount(param, data):
    """Validate that param in data is a representation of a positive decimal number"""
    try:
        numeric_amount = float(data[param])
    except ValueError:
        return (None, error("Invalid {} specified: {}. Must be a decimal number, e.g. 123.45.".format(param, data[param]), 400))
    if numeric_amount < 0:
        return (None, error("{} must be a positive decimal number.".format(param, data[param]), 400))
    return (numeric_amount, None)


def commit_transaction(originator, beneficiary, reference, amount):
    """Commits a transaction to the database and returns the transaction id.
    Requires originator and benficiary account objects, a reference note as
    text and an amount as a decimal.  Adds transaction log and updates running
    balances for each account."""

    new_transaction_id = max_transaction_id() + 1

    originator_transaction = {
        "orginator": originator['account_number'],
        "beneficiary": beneficiary['account_number'],
        "reference": reference,
        "transaction_id": new_transaction_id,
        "amount": -amount}

    beneficiary_transaction = {
        "orginator": beneficiary['account_number'],
        "beneficiary": originator['account_number'],
        "reference": reference,
        "transaction_id": new_transaction_id,
        "amount": amount
        }
    Transactions.append(originator_transaction)
    Transactions.append(beneficiary_transaction)
    originator['balance'] -= amount
    beneficiary['balance'] += amount

    return originator_transaction['transaction_id']

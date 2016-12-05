from flask import jsonify
import time
import api_utils
import db_helper
import settings
import transaction


def get_designated_account(param, data):
    """Return account model if account referenced by number in data
    exists, error otherwise"""
    account_number = data[param]
    account = db_helper.get_account(account_number)
    if not account:
        return (None, api_utils.error("Invalid {} account number {}".format(param, data[param])))
    return (account, None)


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

    committed_transaction = transaction.commit_transfer(
        originator=originator,
        beneficiary=beneficiary,
        reference="Initial Deposit",
        amount=initial_deposit)

    account_summary = db_helper.get_account(new_account['account_number'])

    return jsonify({"transaction id": committed_transaction,
                    "new account": account_summary}), 201


def list_accounts():
    accounts = db_helper.get_all_accounts()
    return jsonify({"accounts": accounts})


def show_adjusted_balance(account_number):
    """Finds latest balance and adjusts for accrued interest rate"""
    account = db_helper.get_account(account_number)
    if not account:
        return api_utils.error("No account with number {} found".format(account_number), 404)

    if account['account_type'] == 'savings':
        balance = api_utils.calc_pv(account['balance'],
                                    account['last_event_time'],
                                    time.time(),
                                    settings.savings_rate)
        return jsonify({"balance": balance})

    return jsonify({"balance": account['balance']})
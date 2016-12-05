from flask import jsonify
import api_utils
import account
import db_helper
import fincalc
import time
import params


def make_payment(data):
    """Create a new payment transaction.
    For every request to this API endpoint two Transaction database entries
    are made in order to have some sort of double entry bookkeeping.
    """
    mandatory_params = ['amount', 'reference', 'originator', 'beneficiary']
    result = api_utils.check_required_params(mandatory_params, data)
    if result:
        return result

    (originator, reject) = account.get_designated_account('originator', data)
    if reject:
        return reject

    (beneficiary, reject) = account.get_designated_account('beneficiary', data)
    if reject:
        return reject

    (amount, reject) = api_utils.numeric_amount('amount', data)
    if reject:
        return reject

    committed_transaction = commit_transaction(
        originator=originator,
        beneficiary=beneficiary,
        reference=data['reference'],
        amount=amount)

    return jsonify({"transaction": committed_transaction}), 201


def list_transactions():
    print("TO DO:  Create list_transaction() in transaction module")
    return None


def commit_transaction(originator, beneficiary, reference, amount):
    """Commits a transaction to the database and returns the transaction id.
    Requires originator and benficiary account objects, a reference note as
    text and an amount as a decimal.  Adds transaction log and updates running
    balances for each account."""

    # NOTE: For daily compounding, accrued account balances assume interest is
    # credited to the account on the event date when in reality the accured
    # balanceshould only reflect interest until the day before.  This is a bit
    # of a mess to sort out as the event date for the accured interest is
    # the day before the event date of the transaction and all the interest
    # displayed will not be available for immediate withdrawl.  SOLUTION:
    # don't keep a current running balance in the DB.  Rather the running
    # balance lag by a few days. A "show balance" would show accrued to the
    # close of biz the day before based on a calculation of transactions since
    # the last running balance.  Any transaction event would update the running
    # balance to the lag date.

    new_event = db_helper.add_new_event('transfer')

    originator_transaction = {
        "originator": originator['account_number'],
        "beneficiary": beneficiary['account_number'],
        "reference": reference,
        "event_id": new_event['event_id'],
        "amount": -amount}

    beneficiary_transaction = {
        "originator": beneficiary['account_number'],
        "beneficiary": originator['account_number'],
        "reference": reference,
        "event_id": new_event['event_id'],
        "amount": amount
        }

    db_helper.add_new_transaction(originator_transaction)
    db_helper.add_new_transaction(beneficiary_transaction)

    # NOTE: I am updating the balance for accrued with each tranaction this has
    # issues as mentioned above.
    db_helper.update_account_balance(originator['account_number'],
                                     adjusted_balance(originator['account_number']) - amount,
                                     new_event['event_id'],
                                     new_event['timestamp'])

    db_helper.update_account_balance(beneficiary['account_number'],
                                     adjusted_balance(beneficiary['account_number']) - amount,
                                     new_event['event_id'],
                                     new_event['timestamp'])

    db_helper.add_new_balance(new_event['event_id'],
                              originator['balance'],
                              originator['account_number'])

    db_helper.add_new_balance(new_event['event_id'],
                              beneficiary['balance'],
                              beneficiary['account_number'])

    return originator_transaction['event_id']


def adjusted_balance(account_number):
    """Returns latest balance and adjusted for accrued interest"""
    account = db_helper.get_account(account_number)
    if not account:
        return api_utils.error("No account with number {} found \
                     ".format(account_number), 404)
    if account['account_type'] == 'savings':
        balance = fincalc.calc_pv(account['balance'],
                                  account['last_event_time'],
                                  time.time(),
                                  params.parms.savings_rate)
        return balance

    return account['balance']


def list_events():
    """List of all events"""
    events = db_helper.get_all_events()
    return jsonify({"events": events})

from flask import jsonify
from db_helper import add_new_event, add_new_balance, add_new_transaction, \
     get_account, update_account_balance
import time
from math import exp
import datetime
import params


def get_data(request):
    """Get data from request either from form-data or json body"""

    # NOTE:  Not sure this works for a form as request is not a FLASK
    # function

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


def get_designated_account(param, data):
    """Return account model if account referenced by number in data
    exists, error otherwise"""
    account_number = data[param]
    account = get_account(account_number)
    if not account:
        return (None, error("Invalid {} account number {}".format(param, data[param])))
    return (account, None)


def numeric_amount(param, data):
    """Validate that param in data is a representation of a positive
    decimal number"""
    try:
        numeric_amount = float(data[param])
    except ValueError:
        return (None, error("Invalid {} specified: {}. Must be a decimal number\
                            , e.g. 123.45.".format(param, data[param]), 400))
    if numeric_amount < 0:
        return (None, error("{} must be a positive decimal \
                            number.".format(param, data[param]), 400))
    return (numeric_amount, None)


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

    new_event = add_new_event('transfer')

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

    add_new_transaction(originator_transaction)
    add_new_transaction(beneficiary_transaction)

    # NOTE: I am updating the balance for accrued with each tranaction this has
    # issues as mentioned above.
    update_account_balance(originator['account_number'],
                           adjusted_balance(originator['account_number']) - amount,
                           new_event['event_id'],
                           new_event['timestamp'])

    update_account_balance(beneficiary['account_number'],
                           adjusted_balance(beneficiary['account_number']) - amount,
                           new_event['event_id'],
                           new_event['timestamp'])

    add_new_balance(new_event['event_id'],
                    originator['balance'],
                    originator['account_number'])

    add_new_balance(new_event['event_id'],
                    beneficiary['balance'],
                    beneficiary['account_number'])

    return originator_transaction['event_id']


def adjusted_balance(account_number):
    """Returns latest balance and adjusted for accrued interest"""
    account = get_account(account_number)
    if not account:
        return error("No account with number {} found \
                     ".format(account_number), 404)
    if account['account_type'] == 'savings':
        balance = calc_pv(account['balance'],
                          account['last_event_time'],
                          time.time(),
                          parms.savings_rate)
        return balance

    return account['balance']


##########################################################################
# Interest rate functions
##########################################################################

def calc_pmt(principal, start, end, rate, closeofbiz):
    """
    Returns interest earned on principal between start and end.
    Compounding defaults to continuous but can be set in Parms
    c for continuous, d for daily based on close_of_biz
    Principal:  principal at start
    start:      starting datetime in seconds since epoch
    end:        ending datetime in seconds since epoch (time.time())
    rate:       annual daily compound rate
    closeofbiz: optional string format '20:00:00'
    """
    if 'close_of_biz' in params.parms.__dict__:
        closeofbiz = params.parms.close_of_biz
    else:
        closeofbiz = params.defaults.close_of_biz

    def compound_daily(principal, start, end, rate, closeofbiz):
        end = effective_date(end, closeofbiz)
        start = effective_date(start, closeofbiz)
        return principal * (pow(1 + rate/365, abs((end - start).days))-1)

    def compound_continuous(principal, start, end, rate, closeofbiz):
        return principal * (1-exp(rate*(end-start)/(365*24*60*60)))

    # check compounding method
    if 'compound' in params.parms.__dict__:
        if params.parms.compound == 'c':
            pmt = compound_continuous(principal, start, end, rate, closeofbiz)
            return pmt
        elif params.parms.compound == 'd':
            pmt = compound_daily(principal, start, end, rate, closeofbiz)
            return pmt
        else:
            print("Invalid compounding parameter in Parms.compound")
            return -1
    print("compound term not in parameters or defaults")
    return -1


def calc_pv(principal, start, end, rate, closeofbiz):
    """
    Returns PV of principal between start and end.
    Compounding defaults to continuous but can be set in Parms
    c for continuous, d for daily based on close_of_biz
    Principal:  principal at start
    start:      starting datetime in seconds since epoch
    end:        ending datetime in seconds since epoch (time.time())
    rate:       annual daily compound rate
    closeofbiz: optional string format '20:00:00'
    """
    if 'close_of_biz' in params.parms.__dict__:
        closeofbiz = params.parms.close_of_biz
    else:
        closeofbiz = params.defaults.close_of_biz

    def compound_daily(principal, start, end, rate, closeofbiz):
        end = effective_date(end, closeofbiz)
        start = effective_date(start, closeofbiz)
        return principal * pow(1 + rate/365, abs((end - start).days))

    def compound_continuous(principal, start, end, rate, closeofbiz):
        return principal * exp(rate*(end-start)/(365*24*60*60))

    # check compounding method
    if 'compound' in params.parms.__dict__:
        if 'c' in params.parms.compound:
            PV = compound_continuous(principal, start, end, rate, closeofbiz)
            return PV
        elif 'd' in params.parms.compound:
            PV = compound_daily(principal, start, end, rate, closeofbiz)
            return PV
        else:
            print("Invalid compounding parameter in Parms.compound")
            return -1
    print("compound term not in parameters or defaults")
    return -1

###############################################################################
#
# Effective close of business
#
###############################################################################


def close_of_business(timestamp, closeofbiz):
    """Returns close of business on day of timestamp
    for a given time of close
    """
    date_of_event = datetime.date.fromtimestamp(timestamp)
    date_time_close = datetime.datetime.strptime(str(date_of_event) + " " + closeofbiz, '%Y-%m-%d %H:%M:%S')
    return date_time_close


def effective_date(timestamp, closeofbiz):
    """returns date of close of business for timestamp and local time of day
    for close of business"""
    event_dtime = datetime.datetime.fromtimestamp(timestamp)
    cob_dtime = close_of_business(timestamp, closeofbiz)
    if (cob_dtime - datetime.timedelta(days=1)) < event_dtime < cob_dtime:
        return cob_dtime.date()
    if cob_dtime < event_dtime < (cob_dtime + datetime.timedelta(days=1)):
        return cob_dtime.date() + datetime.timedelta(days=1)
    print("houson we have a problem with effective date")
    return -1



import params
import datetime
from math import exp


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


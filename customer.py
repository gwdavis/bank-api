from flask import jsonify
import db_helper
import api_utils


def list_customers():
    """List of all customers and customer_id"""
    customers = db_helper.get_all_customers()
    return jsonify({"customers": customers})


def show_accounts(customer_id):
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
    
import db_helper


def variables(dt, dc):
    """Return an object with variable names and values in dict format.
    Arg is db table name and column name where the variables are stored
    in in single cell of db """
    class Bunch(object):
        def __init__(self, x):
            self.__dict__.update(x)      
    return Bunch(db_helper.get_variables(dt, dc))

parms = variables('parms', 'var_json')
defaults = variables('defaults', 'var_json')

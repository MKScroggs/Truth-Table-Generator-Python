import re


class InvalidExpressionException(Exception):
    pass


replacements = (
    (r'\bif and only if\b', ' = '),
    (r'\band\b', ' * '),
    (r'\bor\b', ' + '),
    (r'\bnot\b', ' ~ '),
    (r'\bif\b',  ' > '),
    (r'\biff\b', ' = '),
    (r'<->', ' = '),
    (r'<>', ' = '),
    (r'-->', ' > '),
    (r'->', ' > '),
    (r'!', ' ~ '),
    (r'/\\', ' * '),
    (r'\\/', ' + '),
    (r'\(', ' ( '),
    (r'\)', ' ) '),
    (r'=+', ' = '),
    (r' +', ' '),
    (r'^ +', ''),
    (r' +$', '')
    )

invalid_preceeding_binary = ('+', '*', '>', '=', '(', None)
invalid_following_binary = ('+', '*', '>', '=', ')', None)
invalid_preceeding_unary = (')')
invalid_following_unary = ('+', '*', '>', '=', ')', None)
invalid_preceeding_open = (')', 'true', 'false', 'VAR')
invalid_following_open = (')', '+', '*', '>', '=', None)
invalid_preceeding_close = ('(', '+', '*', '>', '=', '~', None)
invalid_following_close = ('(', '!', 'true', 'false', 'VAR')
invalid_preceeding_var = (')', 'true', 'false', 'VAR', None)
invalid_following_var = ('(', '~', 'true', 'false', 'VAR')


def standardize_string(expression):
    """
    Converts all symbols to uniform version (*+>=~) ensures spacing around
    words and operators
    """
    expression = expression.lower()

    for replacement in replacements:
        expression = re.sub(replacement[0], replacement[1], expression)

    return expression


def has_invalid_chars(expression):
    match = re.match('[^0-9a-zA-Z \~\+\*\(\)=]', expression)
    if match is not None:
        return match.group(0)
    else:
        return None


def var_to_placeholder(string):
    '''
    Takes an input string and determines if it is a variable or not. If not,
    the string is returned. If it is, 'VAR' is returned.
    '''
    non_vars = {'+', '*', '~', '>', '=', '(', ')', 'true', 'false', None}
    if non_vars.contains(string):
        return string
    else:
        return 'VAR'

    '''
    yes these are all more or less the same function, but it seems easier to
    add new functions when they are grouped like this.
    '''
def validate_binary_operator(preceeding, following):
    if invalid_preceeding.contains(preceeding):
        return (False, 'Binary operator preceeded by "{}"'.format(preceeding))
    elif invalid_following.conatins(following):
        return (False, 'Binary operator followed by "{}"'.format(following))
    else:
        return (True, 'Valid')


def validate_neighbors(preceeding, current, following):
    

def validate(expression):
    """
    Validates an expression. If the expression is valid, it is formatted and
    returned as a list of parts. 
    If invalid a message detailing the error is returned for dispay.
    
    Args:
    param1(string): the expression to validate
    
    Returns: either (True, list(strings)) or (False, message)
    bool: is the expression valid
    message(string): reason for invalidation
    """    
    try:
        # standardize the expression to simplify validation and
        expression = standardize_string(expression)

        # ensure all parts are allowed (no invalid chars)
        contains_invalid_chars = has_invalid_chars(expression)
        if contains_invalid_chars is not None:
            raise InvalidExpressionException('Invalid character: {}'.format(
                contains_invalid_chars))
        
        # split into parts to verify each
        parts = expression.split()

        
    except:
        pass
    return (False, "unimplnted")



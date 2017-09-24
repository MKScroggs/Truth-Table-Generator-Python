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

def validate_binary_operator(proceeding, following):
    invalid_preceeding = {'+', '*', '>', '=', '('}
    invalid_following = {'+', '*', '>', '=', ')'}

def has_invalid_neighbors(preceeding, current, following):

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



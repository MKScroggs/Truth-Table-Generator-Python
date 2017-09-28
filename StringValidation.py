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

binary_operators = ('+', '*', '>', '=')
unary_operators = ('~')

invalid_preceeding_binary = ('+', '*', '>', '=', '(', None)
invalid_following_binary = ('+', '*', '>', '=', ')', None)
invalid_preceeding_unary = (')',)  # comma needed to make it a tuple
invalid_following_unary = ('+', '*', '>', '=', ')', None)
invalid_preceeding_open = (')', 'true', 'false', 'VAR')
invalid_following_open = (')', '+', '*', '>', '=', None)
invalid_preceeding_close = ('(', '+', '*', '>', '=', '~', None)
invalid_following_close = ('(', '!', 'true', 'false', 'VAR')
invalid_preceeding_var = (')', 'true', 'false', 'VAR')
invalid_following_var = ('(', '~', 'true', 'false', 'VAR')


def standardize_string(expression):
    '''
    Converts all symbols to uniform version (*+>=~) ensures spacing around
    words and operators
    '''
    expression = expression.lower()

    for replacement in replacements:
        expression = re.sub(replacement[0], replacement[1], expression)

    return expression


def has_invalid_chars(expression):
    '''
    Ensures that only accepted characters are allowed in the string.

    Return: The first invalid character matched if the string is invalid.
       If the string is valid, None is returned
    '''
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
    if string in non_vars:
        return string
    else:
        return 'VAR'


def validate_neighbors(preceeding, current, following):
    '''
    Validates that the symbols passed are allowed to occur in that order
    (ie, is "AND OR p" valid [no], is "p and q" valid [yes])

    return (True, 'Valid') if valid, and (False, ERROR_STRING) if invalid.
    '''
    invalid_preceeding = ()
    invalid_following = ()

    preceeding = var_to_placeholder(preceeding)
    current = var_to_placeholder(current)
    following = var_to_placeholder(following)

    # determine what to use based on what we are looking at
    if current in binary_operators:
        invalid_preceeding = invalid_preceeding_binary
        invalid_following = invalid_following_binary
    elif current in unary_operators:
        invalid_preceeding = invalid_preceeding_unary
        invalid_following = invalid_following_unary
    elif current in ('('):
        invalid_preceeding = invalid_preceeding_open
        invalid_following = invalid_following_open
    elif current in (')'):
        invalid_preceeding = invalid_preceeding_close
        invalid_following = invalid_following_close
    elif current == 'VAR':
        invalid_preceeding = invalid_preceeding_var
        invalid_following = invalid_following_var
    elif current is None:
        return (False, 'None is not valid in an expression')
    else:
        #  how did we get here?
        raise Exception('Non valid symbol "{}" given to  \
                         validate_neighbors'.format(current))

    if preceeding in invalid_preceeding:
        return (False, '"{}" preceeded by "{}"'.format(current, preceeding))
    elif following in invalid_following:
        return (False, '"{}" followed by "{}"'.format(current, following))
    else:
        return (True, 'Valid')


def validate_parentheses(expression):
    '''
    validates that all parentheses are paired properly
    Returns: (True, 'Valid')  if all parentheses are paired
             (False, ERROR_STRING) otherwise
    '''
    count = 0  # this goes up for each '(' and down for each ')'
    for i, part in enumerate(expression, 1):
        if part is '(':
            count += 1
        elif part is ')':
            count -= 1
            # if it is below 0, there are more closing than opening
            if count < 0:
                return (False, 'Unopened ")" at postition {}'.format(i))
    if count > 0:
        return (False, '{} unclosed "(" in expression'.format(count))
    return (True, "Valid")


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



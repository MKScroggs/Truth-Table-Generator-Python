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
non_vars = ('+', '*', '~', '>', '=', '(', ')', 'true', 'false', None)

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


def format_expression(expression):
    '''
    standardizes all characters ('AND'/'and'/'/\' becomes '*') then splits on
    spaces

    Expression: a string
    Returns: a tuple of comma seperated parts.
    '''
    expression = standardize_string(expression)
    return expression.split()


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
    '''
    Validates an expression. Any errors are raised as exceptions
    Args:
    param1(string): the expression to validate. This expression should be
    pre-formated
    '''
    # ensure all parts are allowed (no invalid chars)
    contains_invalid_chars = has_invalid_chars(expression)
    if contains_invalid_chars is not None:
        raise InvalidExpressionException('Invalid character: {}'.format(
            contains_invalid_chars))

    # validate neighbors
    # validate first character
    for i, current in enumerate(expression):
        # get the previous and next element
        previous = []
        # if i = 0, preceeding should be None
        if i < 0:
            previous = None
        else:
            previous = expression[i - 1]
        following = []
        if i > len(expression):
            following = None
        else:
            following = expression[i + 1]

        valid = validate_neighbors(previous, current, following)
        if valid[0] is False:
            raise InvalidExpressionException('Invalid neighbors: {}'.format(
                valid[1]))

    # validate parentheses
    valid = validate_parentheses(expression)
    if valid[0] is False:
        raise InvalidExpressionException('Invalid parentheses: {}'.format(
            valid[1]))

    # a valid expression returns nothing, an invalid expression raises errors
    return None


def get_unique_variables(expression):
    '''
    returns a list of the unique variables in the expression.
    '''
    variables = []
    [variables.append(element) for element in expression if
     element not in variables and
     element not in non_vars]
    return variables


def generate_table(expression):
    '''
    Takes a valid expression and generates a 2d collection that represents
    the truth table
    param1(list of strings): the validated expression
    return: 2d list of the truth table. First row is the header, and
    subsequent rows are the table rows.
    '''
    # get the unique variables in the expression:
    variables = get_unique_variables(expression)

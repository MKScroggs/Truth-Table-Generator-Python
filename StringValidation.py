import re

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


def standardize_string(string):
    string = string.lower()

    for replacement in replacements:
        string = re.sub(replacement[0], replacement[1], string)

    return string


def parse(string):
    print("Parsing {}".format(string))
    string = standardize_string(string)

    print("new string: {}".format(string))
    return [string]


def validate(expression):
    return (False, "unimplemented")
'''
'''

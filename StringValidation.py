import re

replacements = (
    (r"\bif and only if\b", "@"),
    (r"\band\b" , "*"),
    (r"\bor\b", "+"),
    (r"\bnot\b", "~"),
    (r"\bif\b", ">"),
    (r"\biff\b","@")
    )


def parse(string):
    print("Parsing {}".format(string))
    for replacement in replacements:
        string = re.sub(replacement[0], replacement[1], string)

    print("new string: {}".format(string))
    return [string]


def validate(expression):
    #for i in expression:
    return (False, "unimplemented")


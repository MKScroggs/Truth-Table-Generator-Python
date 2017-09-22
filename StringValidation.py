import re


def parse(string):
    print("Parsing {}".format(string))

    # define the changes to be made
    replace = {
        r'\band\b': "*"}

    replace = dict((k, v) for k, v in replace.items())
    pattern = re.compile("|".join(replace.keys()))
    print(replace.get(m.group(0)))
    replaced_string = pattern.sub(lambda m: replace.get(m.group(0)),
                                  string)

    print("new string: {}".format(replaced_string))
    return [string]


def validate(expression):
    #for i in expression:
    return (False, "unimplemented")


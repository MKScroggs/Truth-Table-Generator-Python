
def reversed_enumerate(list_):
    n = len(list_) - 1
    for i in reversed(list_):
        yield n, i
        n -= 1


def find_next_split(list_):
    """
    Finds and returns the next index of a split to make.

    returns: the index (0 based) of the next split to make.
        returns -1 if no split is to be made
    """
    order_of_operations = ('=', '>', '+', '*', '!')  # this is backwards!!!
    for op in order_of_operations:
        for index, part in reversed_enumerate(list_):
            if part == op:
                return index

    return -1


class ExpressionTree:
    """
    Its a binary tree! Has normal left and right children as well a data store.
    """

    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

    def BuildTree(self, expression, paren_map=None):
        """
        Builds a tree by repeatedly spliting the expression. The tree splits on
        the last operation to be completed following the standard order of
        operations:
            Parentheses, Not, And, Or, Implies, If and Only If
        Ties are broken right to left
        The result is a tree with the leaves as the variables and the branches
        as the operations

        args:
        Expression: the expression to calculate. Should already be cleaned and
            validated.
        paren_map: A list of how many parentheses are open at each point in the
            expression. Self generated and passed to future calls, so pass None
            on primary call to BuildTree (defaulted to None, so ignoring works
            too)

        return: None
        """
        # find the last operation in order of operations.
        for i, symbol in reversed_enumerate(expression):
            pass
        pass

    def _AddBinaryChildren(self, left, right, operator):
        pass

    def _AddUnaryChild(self, right, operator='~'):
        pass


if __name__ == "__main__":
    print(find_next_split(('a', '+', 'b', '*', 'c')))
    print(find_next_split(('a', '*', 'b', '+', 'c')))
    print(find_next_split(('a', '*', 'b', '*', 'c')))

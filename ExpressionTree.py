import ExpressionParser as EP


class BadSplitException(Exception):
    pass


def reversed_enumerate(list_):
    n = len(list_) - 1
    for i in reversed(list_):
        yield n, i
        n -= 1


def find_next_split(list_, paren_map):
    """
    Finds and returns the next index of a split to make.

    returns: the index (0 based) of the next split to make.
    returns -1 if the epxression should have outer parens removed
    returns -2 if no split is to be made
    """
    # if the len is 1, the node is a leaf
    if len(list_) == 1:
        return -2
    # this is backwards by intent! We are looking for the least
    # operand first.
    order_of_operations = ('=', '>', '+', '*', '!')

    # determine if the entire expression is in a parenthetical
    # enclosure
    if 0 not in paren_map:
        return -1

    # for each operator
    for op in order_of_operations:
        # for each part of the expression
        for index, part in reversed_enumerate(list_):
            # if the paren_map is 0 then it is not enclosed in any parentheses
            if paren_map[index] == 0:
                if part == op:
                    return index

    # this shouldn't happen ever
    raise BadSplitException('No valid split found in expression: {}'.format(
        ''.join(list_)))


def get_paren_map(list_):
    """
    Makes a map of the number of open parentheses at each point in a list
    arg1: an expression in list format
    returns: a list of equal length to arg1, with an int count of the number
        of open parentheses at each point
    """
    paren_map = []
    count = 0
    for i in list_:
        if i == '(':
            count += 1
            paren_map.append(count)
        elif i == ')':
            paren_map.append(count)  # store before incrementing to count the
            # paren before decrementing
            count -= 1
        else:
            paren_map.append(count)

    return paren_map


class ExpressionTree:
    """
    Its a binary tree! Has normal left and right children as well a data store.
    """

    def __init__(self):
        # left child. Only exists for boolean operators and ')'
        self.left = None
        # right child. Exists for all operators and '('
        self.right = None
        # the expression that the node and all children express.
        self.expression = None
        # the specific part that the node expresses.
        self.value = None
        # is this a leaf node.
        self.is_leaf = False

    def BuildTree(self, expression, paren_map=None):
        """
        Builds a tree by repeatedly spliting the expression. The tree splits on
        the last operation to be completed following the standard order of
        operations:
            Parentheses, Not, And, Or, Implies, If and Only If
        Ties are broken right to left
        The result is a tree with the leaves as the variables and the branches
        as the operations
        Parentheses are extracted together with the enclosed contents as the
        right child. Left is None
        Unary operators have their paired operand as the right child. Left is
        None again.
        Binary operators split as expected, with right and left children
        args:
        Expression: the expression to calculate. Should already be cleaned and
            validated.
        paren_map: A list of how many parentheses are open at each point in the
            expression. Self generated and passed to future calls, so pass None
            on primary call to BuildTree (defaulted to None, so ignoring works
            too)

        return: None
        """

        self.expression = expression

        if paren_map is None:
            paren_map = get_paren_map(expression)  # build paren map

        next_split = find_next_split(expression, paren_map)

        # if no split needed
        if next_split == -2:
            self.is_leaf = True
            self.value = expression[0]
        # if statement is enclosed in parens
        elif next_split == -1:
            self.value = '()'
            self._AddParenChild(expression, paren_map)
        else:
            operator = expression[next_split]
            self.value = operator
            if expression[operator] in EP.unary_operators:
                self._AddUnaryChild(expression, paren_map, next_split)
            else:
                self._AddBinaryChildren(expression, paren_map, next_split)

    def _AddBinaryChildren(self, expression, paren_map, split):
        '''
        builds the left and right children and adds them to the current node
        '''
        # this should be safe as no expression can end in a binary operator
        expression = (expression[:split], expression[split + 1:])
        paren_map = (paren_map[:split], paren_map[split + 1:])

        # build the children
        left_child = ExpressionTree()
        left_child.BuildTree(expression[0], paren_map[0])
        self.left = left_child

        right_child = ExpressionTree()
        right_child.BuildTree(expression[1], paren_map[1])
        self.right = right_child

    def _AddUnaryChild(self, expression, paren_map):
        '''
        builds the right child and adds it to the current node
        '''
        # this should be safe as no expression can end in a binary operator
        expression = (expression[:1])
        paren_map = (paren_map[:1])

        # build the child
        right_child = ExpressionTree()
        right_child.BuildTree(expression, paren_map)
        self.right = right_child

    def _addParenChild(self, expression, paren_map):
        '''
        Builds the child of a paren node. Child is stored on the right branch
        '''
        # remove parens
        expression = expression[1:-1]
        paren_map = paren_map[1:-1]

        # build the right child
        right_child = ExpressionTree()
        self.right = right_child
        right_child.BuildTree(expression, paren_map)


if __name__ == "__main__":
    print(find_next_split(('a', '+', 'b', '*', 'c')))
    print(find_next_split(('a', '*', 'b', '+', 'c')))
    print(find_next_split(('a', '*', 'b', '*', 'c')))

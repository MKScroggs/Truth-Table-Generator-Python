import unittest
import ExpressionParser as EP
import ExpressionTree as ET


class ControllerTests(unittest.TestCase):

    def test_expression_tree_infix(self):
        # this tests both tree genereation and infix traversal

        # tests all operators
        with self.subTest():
            exp = ['~', 'a', '+', 'b', '*', 'c', '>', 'd', '=', 'e']
            tree = ET.ExpressionTree()
            tree.BuildTree(exp)
            self.assertEqual(tree.InfixTraverse(), exp)
        # it should work in reverse order too
        with self.subTest():
            exp = ['a', '=', 'b', '>', 'c', '*', 'd', '+', '~', 'e']
            tree = ET.ExpressionTree()
            tree.BuildTree(exp)
            self.assertEqual(tree.InfixTraverse(), exp)
        # multiple parentheses groups
        with self.subTest():
            exp = ['(', 'a', '+', 'b', ')', '>', '~', '(', 'a', '*', 'b', ')']
            tree = ET.ExpressionTree()
            tree.BuildTree(exp)
            self.assertEqual(tree.InfixTraverse(), exp)
        # nested parentheses
        with self.subTest():
            exp = ['a', '=', '(', '(', 'a', ')', '>', 'b', ')', '*', 'b']
            tree = ET.ExpressionTree()
            tree.BuildTree(exp)
            self.assertEqual(tree.InfixTraverse(), exp)
        # entire expression in parentheses (why?)
        with self.subTest():
            exp = ['(', '~', '(', '(', 'a', ')', '>', 'b', ')', '*', 'b', ')']
            tree = ET.ExpressionTree()
            tree.BuildTree(exp)
            self.assertEqual(tree.InfixTraverse(), exp)

    def test_find_next_split(self):
        # test iff and if
        with self.subTest():
            exp = ('a', '>', 'b', '=', 'c')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                3)
        # test if and or
        with self.subTest():
            exp = ('a', '>', 'b', '+', 'c')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                1)
        # test or and and
        with self.subTest():
            exp = ('a', '+', 'b', '*', 'c')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                1)
        # test order changing or and and
        with self.subTest():
            exp = ('a', '+', 'b', '*', 'c')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                1)
        # test and and not
        with self.subTest():
            exp = ('~', 'b', '*', 'c')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                2)
        # test simple parentheses
        with self.subTest():
            exp = ('~', '(', '~', 'b', ')')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                0)
        # test multiple parentheses
        with self.subTest():
            exp = ('(', 'b', ')', '+', '(', 'a', ')')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                3)
        # test surrounded in parentheses
        with self.subTest():
            exp = ('(', '~', 'b', ')')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                -1)
        # test leaf node
        with self.subTest():
            exp = ('b')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                -2)
        # test duplicate operators
        # test order changing
        with self.subTest():
            exp = ('a', '+', 'b', '+', 'c')
            paren_map = ET.get_paren_map(exp)
            self.assertEqual(ET.find_next_split(
                exp, paren_map),
                3)
        # test error case, no operators

        # test order changing
        with self.subTest():
            exp = ('a', 'a')
            paren_map = ET.get_paren_map(exp)
            with self.assertRaises(ET.BadSplitException):
                ET.find_next_split(exp, paren_map)

    def test_get_paren_map(self):
        # no parens
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('a', '*', 'b')),
                [0, 0, 0])
        # ending with parens
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('a', '*', '(', 'b', ')')),
                [0, 0, 1, 1, 1])
        # starting with parens
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('(', 'a', ')', '*', 'b')),
                [1, 1, 1, 0, 0])
        # parens in middle
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('~', '(', 'a', ')', '*')),
                [0, 1, 1, 1, 0])
        # two sets of parens
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('(', 'a', ')', '+', '(', 'a', ')')),
                [1, 1, 1, 0, 1, 1, 1])
        # nested parend
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('(', '(', 'a', ')', ')')),
                [1, 2, 2, 2, 1])
        # deep parens
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('(', '(', '(', '(', 'a', ')', ')', ')', ')')),
                [1, 2, 3, 4, 4, 4, 3, 2, 1])
        # complex
        with self.subTest():
            self.assertEqual(ET.get_paren_map(
                ('(', 'a', '+', 'b', ')', '+',
                 '(', '~', '(', 'a', '*', 'b', ')', ')')),
                [1, 1, 1, 1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 1])

    def test_get_unique_variables(self):
        # basic case
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('p', '+', 'q')),
                ['p', 'q'])
        # with repetition
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('p', '+', '~', 'p')),
                ['p'])
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('p', '+', 'q', '*', 'p')),
                ['p', 'q'])
        # with only constants
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('false', '+', 'true')),
                [])
        # complex expression
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('p', '+', 'q', '*', 'r', '>', 's', '=', 't', '=', '~', 'u',
                 '=', '(', 'p', '+', 'q', ')')),
                ['p', 'q', 'r', 's', 't', 'u'])
        # mulitchar variables
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('first', '+', 'last')),
                ['first', 'last'])

    def test_validate_parentheses(self):
        # true cases
        with self.subTest():
            self.assertTrue(EP.validate_parentheses(
                ('(', 'p', ')'))[0])
        with self.subTest():
            self.assertTrue(EP.validate_parentheses(
                ('(', '(', 'p', ')', ')'))[0])
        with self.subTest():
            self.assertTrue(EP.validate_parentheses(
                ('(', 'p', ')', '+', '(', 'q', ')'))[0])
        with self.subTest():
            self.assertTrue(EP.validate_parentheses(
                ('(', '(', 'p', ')', '+', '(', 'q', ')', ')'))[0])
        with self.subTest():
            self.assertTrue(EP.validate_parentheses(
                ('p', '+', 'q'))[0])

        # false cases
        with self.subTest():
            self.assertFalse(EP.validate_parentheses(
                ('(', 'p'))[0])
        with self.subTest():
            self.assertFalse(EP.validate_parentheses(
                ('p', ')'))[0])
        with self.subTest():
            self.assertFalse(EP.validate_parentheses(
                ('(', '(', 'p', ')'))[0])
        with self.subTest():
            self.assertFalse(EP.validate_parentheses(
                ('(', 'p', ')', '+', 'q', ')'))[0])

    def test_var_to_placeholder(self):
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('+'), '+')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('*'), '*')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('~'), '~')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('>'), '>')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('='), '=')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('('), '(')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder(')'), ')')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('true'), 'true')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('false'), 'false')
        with self.subTest():
            self.assertIsNone(EP.var_to_placeholder(None))
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('p'), 'VAR')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('q'), 'VAR')
        with self.subTest():
            self.assertEqual(EP.var_to_placeholder('andorvar'), 'VAR')

    def test_validate_neighbors(self):
        # cases with none
        with self.subTest():
            self.assertTrue(EP.validate_neighbors(None, 'p', '+')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors(None, '~', 'p')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors(None, '~', '(')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors(None, '(', 'p')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('*', 'p', None)[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('~', 'p', None)[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('p', ')', None)[0])

        # basic valid cases
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('p', '+', 'q')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('p', '*', 'q')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('p', '>', 'q')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('p', '=', 'q')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('~', 'p', '+')[0])
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('(', 'p', ')')[0])

        # double negation is valid
        with self.subTest():
            self.assertTrue(EP.validate_neighbors('~', '~', 'p')[0])

        # invalid cases
        # double vars
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('p', 'q', '+')[0])
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('+', 'p', 'q')[0])

        # double binary ops
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('+', '>', 'q')[0])
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('p', '=', '+')[0])

        # invalid parens
        with self.subTest():
            self.assertFalse(EP.validate_neighbors(')', '(', 'p')[0])
        with self.subTest():  # empty parens is bad
            self.assertFalse(EP.validate_neighbors('(', ')', 'p')[0])
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('p', '(', ')')[0])
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('p', ')', '(')[0])
        with self.subTest():
            self.assertFalse(EP.validate_neighbors(')', '~', 'p')[0])
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('(', '>', 'p')[0])

        # unlcosed parens
        with self.subTest():
            self.assertFalse(EP.validate_neighbors('~', '(', None)[0])
        with self.subTest():
            self.assertFalse(EP.validate_neighbors(None, ')', '*')[0])

    def test_has_invalid_chars(self):
        with self.subTest():
            self.assertEqual(EP.has_invalid_chars('&'), '&')
        with self.subTest():
            self.assertIsNone(EP.has_invalid_chars('a + b'))
        with self.subTest():
            self.assertIsNone(EP.has_invalid_chars('a * b'))
        with self.subTest():
            self.assertIsNone(EP.has_invalid_chars('a > b'))
        with self.subTest():
            self.assertIsNone(EP.has_invalid_chars('a = b'))
        with self.subTest():
            self.assertIsNone(EP.has_invalid_chars('~ b'))
        with self.subTest():
            self.assertIsNone(EP.has_invalid_chars('( b )'))

    def test_and_replacement(self):
        with self.subTest():
            self.assertEqual(EP.standardize_string('a and b'), 'a * b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('testand'), 'testand')
        with self.subTest():
            self.assertEqual(EP.standardize_string('andtest'), 'andtest')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a/\\b'), 'a * b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a /\\ b'), 'a * b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('*'), '*')

    def test_or_replacement(self):
        with self.subTest():
            self.assertEqual(EP.standardize_string('a or b'), 'a + b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('testor'), 'testor')
        with self.subTest():
            self.assertEqual(EP.standardize_string('ortest'), 'ortest')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a\\/b'), 'a + b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a \\/ b'), 'a + b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('+'), '+')

    def test_not_replacement(self):
        with self.subTest():
            self.assertEqual(EP.standardize_string('a not b'), 'a ~ b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('not b'), '~ b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('testnot'), 'testnot')
        with self.subTest():
            self.assertEqual(EP.standardize_string('nottest'), 'nottest')
        with self.subTest():
            self.assertEqual(EP.standardize_string('!b'), '~ b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('! b'), '~ b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('~'), '~')

    def test_if_replacement(self):
        with self.subTest():
            self.assertEqual(EP.standardize_string('a if b'), 'a > b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('testif'), 'testif')
        with self.subTest():
            self.assertEqual(EP.standardize_string('iftest'), 'iftest')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a -> b'), 'a > b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a --> b'), 'a > b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('>'), '>')

    def test_iff_replacement(self):
        with self.subTest():
            self.assertEqual(EP.standardize_string('a iff b'), 'a = b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('testiff'), 'testiff')
        with self.subTest():
            self.assertEqual(EP.standardize_string('ifftest'), 'ifftest')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a if and only if b'),
                             'a = b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a <-> b'), 'a = b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a <> b'), 'a = b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a == b'), 'a = b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('='), '=')
        with self.subTest():
            self.assertEqual(EP.standardize_string('testif and only if b'),
                             'testif * only > b')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a if and only iftest'),
                             'a > * only iftest')
        with self.subTest():
            self.assertEqual(EP.standardize_string('a === b'), 'a = b')

    def test_space_replacement(self):
        self.assertEqual(EP.standardize_string('a       b'), 'a b')

    def test_complex_expression(self):
        self.assertEqual(EP.standardize_string(
            'a and b or c if d iff e not f'),
            'a * b + c > d = e ~ f')

    def test_complex_expression_no_spaces(self):
        self.assertEqual(EP.standardize_string('a/\\b\\/c-->d<->e!f'),
                         'a * b + c > d = e ~ f')

    def test_trailing_spaces_replacement(self):
        self.assertEqual(EP.standardize_string(' a '), 'a')


if __name__ == '__main__':
    unittest.main()

import unittest
import ExpressionParser as EP


class ControllerTests(unittest.TestCase):

    def test_get_unique_variables(self):
        # basic case
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(('p', '+', 'q')),
                             ['p', 'q'])
        # with repetition
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(('p', '+', '~', 'p')),
                             ['p'])
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('p', '+', 'q', '*', 'p')),
                ['p', 'q'])
        # with only constants
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(('false', '+', 'true')),
                             [])
        # complex expression
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(
                ('p', '+', 'q', '*', 'r', '>', 's', '=', 't', '=', '~', 'u',
                 '=', '(', 'p', '+', 'q', ')')),
                ['p', 'q', 'r', 's', 't', 'u'])
        # mulitchar variables
        with self.subTest():
            self.assertEqual(EP.get_unique_variables(('first', '+', 'last')),
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

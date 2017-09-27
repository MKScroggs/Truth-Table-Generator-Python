import unittest
import StringValidation as SV


class ControllerTests(unittest.TestCase):

    def test_var_to_placeholder(self):
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('+'), '+')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('*'), '*')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('~'), '~')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('>'), '>')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('='), '=')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('('), '(')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder(')'), ')')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('true'), 'true')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('false'), 'false')
        with self.subTest():
            self.assertIsNone(SV.var_to_placeholder(None))
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('p'), 'p')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('q'), 'q')
        with self.subTest():
            self.assertEqual(SV.var_to_placeholder('andorvar'), 'andorvar')

    def test_validate_neighbors(self):
        # cases with none
        with self.subTest():
            self.assertTrue(SV.validate_neighbors(None, 'p', '+')[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors(None, '~', 'p')[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors(None, '(', 'p')[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('*', 'p', None)[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('~', 'p', None)[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('p', ')', None)[0])

        # basic valid cases
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('p', '+', 'q')[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('p', '*', 'q')[0])
        with self.subTest():            
            self.assertTrue(SV.validate_neighbors('p', '>', 'q')[0]))
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('p', '=', 'q')[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('~', 'p', '+')[0])
        with self.subTest():
            self.assertTrue(SV.validate_neighbors('(', 'p', ')')[0])

            
    def test_has_invalid_chars(self):
        with self.subTest():
            self.assertEqual(SV.contains_invalid_chars('&'), '&')
        with self.subTest():
            self.assertIsNone(SV.contains_invalid_chars('a + b'))
        with self.subTest():
            self.assertIsNone(SV.contains_invalid_chars('a * b'))
        with self.subTest():
            self.assertIsNone(SV.contains_invalid_chars('a > b'))
        with self.subTest():
            self.assertIsNone(SV.contains_invalid_chars('a = b'))
        with self.subTest():
            self.assertIsNone(SV.contains_invalid_chars('~ b'))
        with self.subTest():
            self.assertIsNone(SV.contains_invalid_chars('( b )'))

    def test_and_replacement(self):
        with self.subTest():
            self.assertEqual(SV.standardize_string('a and b'), 'a * b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('testand'), 'testand')
        with self.subTest():
            self.assertEqual(SV.standardize_string('andtest'), 'andtest')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a/\\b'), 'a * b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a /\\ b'), 'a * b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('*'), '*')

    def test_or_replacement(self):
        with self.subTest():
            self.assertEqual(SV.standardize_string('a or b'), 'a + b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('testor'), 'testor')
        with self.subTest():
            self.assertEqual(SV.standardize_string('ortest'), 'ortest')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a\\/b'), 'a + b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a \\/ b'), 'a + b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('+'), '+')

    def test_not_replacement(self):
        with self.subTest():
            self.assertEqual(SV.standardize_string('a not b'), 'a ~ b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('not b'), '~ b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('testnot'), 'testnot')
        with self.subTest():
            self.assertEqual(SV.standardize_string('nottest'), 'nottest')
        with self.subTest():
            self.assertEqual(SV.standardize_string('!b'), '~ b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('! b'), '~ b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('~'), '~')

    def test_if_replacement(self):
        with self.subTest():
            self.assertEqual(SV.standardize_string('a if b'), 'a > b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('testif'), 'testif')
        with self.subTest():
            self.assertEqual(SV.standardize_string('iftest'), 'iftest')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a -> b'), 'a > b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a --> b'), 'a > b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('>'), '>')

    def test_iff_replacement(self):
        with self.subTest():
            self.assertEqual(SV.standardize_string('a iff b'), 'a = b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('testiff'), 'testiff')
        with self.subTest():
            self.assertEqual(SV.standardize_string('ifftest'), 'ifftest')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a if and only if b'),
                             'a = b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a <-> b'), 'a = b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a <> b'), 'a = b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a == b'), 'a = b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('='), '=')
        with self.subTest():
            self.assertEqual(SV.standardize_string('testif and only if b'),
                             'testif * only > b')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a if and only iftest'),
                             'a > * only iftest')
        with self.subTest():
            self.assertEqual(SV.standardize_string('a === b'), 'a = b')

    def test_space_replacement(self):
        self.assertEqual(SV.standardize_string('a       b'), 'a b')

    def test_complex_expression(self):
        self.assertEqual(SV.standardize_string(
            'a and b or c if d iff e not f'),
            'a * b + c > d = e ~ f')

    def test_complex_expression_no_spaces(self):
        self.assertEqual(SV.standardize_string('a/\\b\\/c-->d<->e!f'),
                         'a * b + c > d = e ~ f')

    def test_trailing_spaces_replacement(self):
        self.assertEqual(SV.standardize_string(' a '), 'a')


if __name__ == '__main__':
    unittest.main()

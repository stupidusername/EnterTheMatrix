from matrix import Matrix
import unittest


class TestMatrix(unittest.TestCase):
    """
    Tests for `Matrix` class.
    """

    def test_invalid_matrix(self):
        """
        Test that invalid matrix side length value raise the appropriate
        exceptions.
        """
        with self.assertRaises(TypeError):
            Matrix('3')
        with self.assertRaises(ValueError):
            Matrix(0)
        with self.assertRaises(ValueError):
            Matrix(101)

    def test_invalid_query_method(self):
        """
        Test that an invalid query method returns an error.
        """
        m = Matrix(3)
        self.assertEqual(m.execute('INVALID'), ('ERROR', None))

    def test_update_invalid_params(self):
        """
        Test that the `UPDATE` method returns error when using wrong params.
        """
        m = Matrix(3)
        self.assertEqual(m.execute('UPDATE'), ('ERROR', None))
        self.assertEqual(m.execute('UPDATE 1'), ('ERROR', None))
        self.assertEqual(m.execute('UPDATE a'), ('ERROR', None))
        self.assertEqual(m.execute('UPDATE 1 1 1 127'), ('ERROR', None))
        self.assertEqual(m.execute('UPDATE 1 1 1 -127'), ('ERROR', None))
        self.assertEqual(m.execute('UPDATE 0 1 1 -127'), ('ERROR', None))
        self.assertEqual(m.execute('UPDATE 4 1 1 -127'), ('ERROR', None))

    def test_query_invalid_params(self):
        """
        Test that the `QUERY` method returns error when using wrong params.
        """
        m = Matrix(3)
        self.assertEqual(m.execute('QUERY'), ('ERROR', None))
        self.assertEqual(m.execute('QUERY 0 1 1 1 1 1'), ('ERROR', None))
        self.assertEqual(m.execute('QUERY 4 1 1 1 1 1'), ('ERROR', None))
        self.assertEqual(m.execute('QUERY 2 1 1 1 1 1'), ('ERROR', None))
        self.assertEqual(m.execute('QUERY a 1 1 1 1 1'), ('ERROR', None))

    def test_update_and_query(self):
        """
        Test `UPDATE` and `QUERY` methods together since a query is the only
        way of checking a successful update using the `Matrix` public methods.
        """
        m = Matrix(3)
        for x in range(1, 4):
            for y in range(1, 4):
                for z in range(1, 4):
                    # Check support of negative values.
                    value = -((x - 1) * 3 * 3 + (y - 1) * 3 + (z - 1) + 1)
                    # Check that the query format has some degree of tolerance.
                    query = ' update  {}  {}  {}  {} '.format(x, y, z, value)
                    self.assertEqual(m.execute(query), ('SUCCESS', None))
        self.assertEqual(m.execute(' query  3 3 3 3 3 3 '), ('SUCCESS', -27))
        self.assertEqual(m.execute('QUERY 1 1 1 3 3 3'), ('SUCCESS', -378))


if __name__ == '__main__':
    unittest.main()

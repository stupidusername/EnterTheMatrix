class Matrix(object):
    """
    A cubic three dimensional matrix of integers.

    The matrix can hold values between -126 ad 126 (inclusive).

    Create an instance of this class by specifying the length of one of its
    sides. After that, you can call `execute(query)` to process a query.

    :param int n: Matrix side length. A value of 3 would create a matrix of
                  size 3 x 3 x 3. Between 1 and 100 (inclusive).
    """

    # Withe-list supported methods to prevent malicious code execution.
    METHODS = ['UPDATE', 'QUERY']

    def __init__(self, n: int):
        if type(n) is not int:
            raise TypeError
        if not 1 <= n <= 100:
            raise ValueError
        # Initialize cell values to 0.
        self._cells = [[
            [0 for i in range(0, n)] for i in range(0, n)
        ] for i in range(0, n)]

    def execute(self, query):
        """
        Execute a query.

        This method always returns a tuple of format `(str, object)`. Where the
        first value is either `'SUCCESS'` or `'ERROR'` and the second one can
        take any value that the executed query returns (including `None` if not
        needed).

        At this moment only two operatios are supported by `execute(query)`:

            - `UPDATE x y z W`
                Set the value of cell x, y, z to W. W must take values between
                -126 ad 126 (inclusive). Returns `None`.
            - `QUERY x1 y1 z1 x2 y2 z2`
                Get the sum of values between x1, y1, z1 and x2, y2, z2. Note
                that x1 should be less than or equal to x2, y1 less than or
                equal to y2 and z1 less than or equal to z2. Returns an
                integer.

        Note that coordinates are 1-based and accessing values below 1 or above
        the size of the matrix will result in an error.

        :param str query: A supported query. Query methods are case-agnostic.
        :returns: The query execution status and its result (if needed).
        :rtype: (str, object)
        """
        # Create default return values.
        success = 'ERROR'
        result = None
        # Trim and split query.
        params = query.strip().split()
        if params:
            # Get query method in uppercase.
            method = params[0].upper()
            # Check if it is secure.
            if method in Matrix.METHODS:
                # Get the actual function name.
                attr_name = '_' + method.lower()
                func = getattr(self, attr_name)
                # Catch known exceptions of inner methods.
                try:
                    result = func(*params[1:])
                    # We can assume that the method was executed succesfully.
                    success = 'SUCCESS'
                except (TypeError, ValueError):
                    # Do nothing. Default return values handle this case ;).
                    pass
        return (success, result)

    # Checks a valid sub-coordinate value.
    def _check_value(self, value):
        if not 1 <= value <= len(self._cells):
            raise ValueError

    # Update method.
    def _update(self, x, y, z, w):
        x = int(x)
        y = int(y)
        z = int(z)
        w = int(w)
        self._check_value(x)
        self._check_value(y)
        self._check_value(z)
        if not -126 <= w <= 126:
            raise ValueError
        self._cells[x - 1][y - 1][z - 1] = w

    # Query method.
    def _query(self, x1, y1, z1, x2, y2, z2):
        sum = 0
        x1 = int(x1)
        y1 = int(y1)
        z1 = int(z1)
        x2 = int(x2)
        y2 = int(y2)
        z2 = int(z2)
        self._check_value(x1)
        self._check_value(y1)
        self._check_value(z1)
        self._check_value(x2)
        self._check_value(y2)
        self._check_value(z2)
        if x1 > x2 or y1 > y2 or z1 > z2:
            raise ValueError
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    sum += self._cells[x - 1][y - 1][z - 1]
        return sum

class Matrix(object):
    """
    A cubic three dimensional matrix of integers.

    The matrix can hold values between -126 and 126 (inclusive).

    Create an instance of this class by specifying the length of one of its
    sides. After that, you can call `execute(query)` to process a query.

    :param int n: Matrix side length. A value of 3 would create a matrix of
                  size 3 x 3 x 3. Between 1 and 100 (inclusive).
    """

    # List of supported methods, their callbacks and supported parameter types.
    METHODS = {
        'UPDATE': {
            'callable': '_update',
            'params': [
                'subcoordinate',
                'subcoordinate',
                'subcoordinate',
                'value'
            ]
        },
        'QUERY': {
            'callable': '_query',
            'params': [
                'subcoordinate',
                'subcoordinate',
                'subcoordinate',
                'subcoordinate',
                'subcoordinate',
                'subcoordinate'
            ]
        }
    }

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
                -126 and 126 (inclusive). Returns `None`.
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
            # Get method definition.
            if method in Matrix.METHODS:
                method_def = Matrix.METHODS[method]
                func = getattr(self, method_def['callable'])
                # Catch known exceptions.
                try:
                    # Execute the function with validated parameters.
                    validated_params = map(
                        self._validate_param,
                        method_def['params'],
                        params[1:]
                    )
                    result = func(*validated_params)
                    # We can assume that the method was executed succesfully.
                    success = 'SUCCESS'
                except (TypeError, ValueError):
                    # Do nothing. Default return values handle this case ;).
                    pass
        return (success, result)

    # Validate and curate a query parameter.
    def _validate_param(self, type, val):
        val_int = int(val)
        if type == 'subcoordinate':
            if not 1 <= val_int <= len(self._cells):
                raise ValueError
        elif type == 'value':
            if not -126 <= val_int <= 126:
                raise ValueError
        return val_int

    # Update method.
    def _update(self, x, y, z, w):
        self._cells[x - 1][y - 1][z - 1] = w

    # Query method.
    def _query(self, x1, y1, z1, x2, y2, z2):
        sum = 0
        if x1 > x2 or y1 > y2 or z1 > z2:
            raise ValueError
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    sum += self._cells[x - 1][y - 1][z - 1]
        return sum

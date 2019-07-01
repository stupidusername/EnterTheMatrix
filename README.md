# EnterTheMatrix


## Requirements

- Python >= 3.5 (tested on 3.7.3)


## Usage Example

```
from matrix import Matrix

# Create a matrix.
m = Matrix(5)
# Change one of its values to 5.
m.execute('UPDATE 1 1 1 5')
# Get the sum of its values.
print(m.execute('QUERY 1 1 1 5 5 5')[1])
```


## Run tests

```
$ python3 test.py
```

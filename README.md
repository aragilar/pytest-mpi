[![Documentation Status](https://readthedocs.org/projects/pytest-mpi/badge/?version=latest)](http://pytest-mpi.readthedocs.org/en/latest/?badge=latest)
[![Coverage Status](https://codecov.io/github/aragilar/pytest-mpi/coverage.svg?branch=master)](https://codecov.io/github/aragilar/pytest-mpi?branch=master)
[![Version](https://img.shields.io/pypi/v/pytest-mpi.svg)](https://pypi.python.org/pypi/pytest-mpi/)
[![License](https://img.shields.io/pypi/l/pytest-mpi.svg)](https://pypi.python.org/pypi/pytest-mpi/)
[![Wheel](https://img.shields.io/pypi/wheel/pytest-mpi.svg)](https://pypi.python.org/pypi/pytest-mpi/)
[![Format](https://img.shields.io/pypi/format/pytest-mpi.svg)](https://pypi.python.org/pypi/pytest-mpi/)
[![Supported versions](https://img.shields.io/pypi/pyversions/pytest-mpi.svg)](https://pypi.python.org/pypi/pytest-mpi/)
[![Supported implemntations](https://img.shields.io/pypi/implementation/pytest-mpi.svg)](https://pypi.python.org/pypi/pytest-mpi/)
[![PyPI](https://img.shields.io/pypi/status/pytest-mpi.svg)](https://pypi.python.org/pypi/pytest-mpi/)

`pytest_mpi` is a plugin for pytest providing some useful tools when running
tests under MPI, and testing MPI-related code.

To run a test only when using MPI, use the `pytest.mark.mpi` marker like:
```python

    @pytest.mark.mpi
    def test_mpi():
        pass
```

Further documentation can be found at [https://pytest-mpi.readthedocs.io](https://pytest-mpi.readthedocs.io).

Bug reports and suggestions should be filed at
[https://github.com/aragilar/pytest-mpi/issues](https://github.com/aragilar/pytest-mpi/issues).

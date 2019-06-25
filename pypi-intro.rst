`pytest_mpi` is a plugin for pytest providing some useful tools when running
tests under MPI, and testing MPI-related code.

To run a test only when using MPI, use the `pytest.mark.mpi` marker like:
::

    @pytest.mark.mpi
    def test_mpi():
        pass


Further documentation can be found at `<https://pytest-mpi.readthedocs.io>`_.

Bug reports and suggestions should be filed at
`<https://github.com/aragilar/pytest-mpi/issues>`_.


|Documentation Status| |Build Status| |Coverage Status|

.. |Documentation Status| image:: https://readthedocs.org/projects/pytest-mpi/badge/?version=latest
   :target: http://pytest-mpi.readthedocs.org/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/aragilar/pytest-mpi.svg?branch=master
   :target: https://travis-ci.org/aragilar/pytest-mpi
.. |Coverage Status| image:: https://codecov.io/github/aragilar/pytest-mpi/coverage.svg?branch=master
   :target: https://codecov.io/github/aragilar/pytest-mpi?branch=master

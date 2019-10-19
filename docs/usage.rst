Usage
=====

The important thing to remember is that `pytest-mpi` assists with running tests
when `pytest` is run under MPI, rather than launching `pytest` under MPI. To
actually run the tests under MPI, you will want to run something like::

    $ mpirun -n 2 python -m pytest --with-mpi

Note that by default the MPI tests are not run—this makes it easy to run the
non-MPI parts of a test suite without having to worry about installing MPI and
mpi4py.

An simple test using the `mpi` marker managed by `pytest-mpi` is:

.. code-block:: python

    import pytest
    @pytest.mark.mpi
    def test_size():
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        assert comm.size > 0

This test will be automatically be skipped unless `--with-mpi` is used. We can
also specify a minimum number of processes required to run the test:

.. code-block:: python

    import pytest
    @pytest.mark.mpi(min_size=2)
    def test_size():
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        assert comm.size >= 2

There are also `mpi_skip`, for when a test should not be run under MPI (e.g. it
causes a lockup or segmentation fault), and `mpi_xfail`, for when a test should
succeed when run normally, but fail when run under MPI.

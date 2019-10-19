Markers
=======

.. py:function:: pytest.mark.mpi(min_size=None)

    Mark that this test must be run under MPI.

    :keyword int min_size:
        Specify that this test requires at least `min_size` processes to run. If
        there are insufficient processes, skip this test.

        For example:

        .. code-block:: python

            import pytest

            @pytest.mark.mpi(minsize=4)
            def test_mpi_feature():
                ...


.. py:function:: pytest.mark.mpi_skip

    Mark that this test should be skipped when run under MPI.


.. py:function:: pytest.mark.mpi_xfail

    Mark that this test should be xfailed when run under MPI.

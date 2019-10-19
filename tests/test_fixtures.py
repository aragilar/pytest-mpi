
def test_mpi(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.mpi
        def test_size():
            from mpi4py import MPI
            comm = MPI.COMM_WORLD

            assert comm.size > 0

        @pytest.mark.mpi(min_size=2)
        def test_size_min_2():
            from mpi4py import MPI
            comm = MPI.COMM_WORLD

            assert comm.size >= 2
        """
    )

    # run all tests with pytest
    result = testdir.runpytest()

    # check that all 4 tests passed
    result.assert_outcomes(skipped=2)

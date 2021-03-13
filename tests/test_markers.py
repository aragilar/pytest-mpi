from pytest_mpi._helpers import _fix_plural

MPI_TEST_CODE = """
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

    @pytest.mark.mpi(min_size=4)
    def test_size_min_4():
        from mpi4py import MPI
        comm = MPI.COMM_WORLD

        assert comm.size >= 4

    @pytest.mark.mpi(2)
    def test_size_fail_pos():
        from mpi4py import MPI
        comm = MPI.COMM_WORLD

        assert comm.size > 0

    def test_no_mpi():
        assert True
"""
MPI_SKIP_TEST_CODE = """
    import pytest

    @pytest.mark.mpi_skip
    def test_skip():
        assert True
"""
MPI_XFAIL_TEST_CODE = """
    import pytest

    @pytest.mark.mpi_xfail
    def test_xfail():
        try:
            from mpi4py import MPI
            comm = MPI.COMM_WORLD
            assert comm.size < 2
        except ImportError:
            assert True
"""


def test_mpi(testdir):
    testdir.makepyfile(MPI_TEST_CODE)

    result = testdir.runpytest()

    result.assert_outcomes(skipped=4, passed=1)


def test_mpi_with_mpi(mpi_testdir, has_mpi4py):
    mpi_testdir.makepyfile(MPI_TEST_CODE)

    result = mpi_testdir.runpytest("--with-mpi")

    if has_mpi4py:
        result.assert_outcomes(**_fix_plural(passed=3, errors=1, skipped=1))
    else:
        result.assert_outcomes(**_fix_plural(passed=1, errors=4))


def test_mpi_only_mpi(mpi_testdir, has_mpi4py):
    mpi_testdir.makepyfile(MPI_TEST_CODE)

    result = mpi_testdir.runpytest("--only-mpi")

    if has_mpi4py:
        result.assert_outcomes(**_fix_plural(passed=2, errors=1, skipped=2))
    else:
        result.assert_outcomes(**_fix_plural(errors=4, skipped=1))


def test_mpi_skip(testdir):
    testdir.makepyfile(MPI_SKIP_TEST_CODE)

    result = testdir.runpytest()

    result.assert_outcomes(passed=1)


def test_mpi_skip_under_mpi(mpi_testdir):
    mpi_testdir.makepyfile(MPI_SKIP_TEST_CODE)

    result = mpi_testdir.runpytest("--with-mpi")

    result.assert_outcomes(skipped=1)


def test_mpi_xfail(testdir):
    testdir.makepyfile(MPI_XFAIL_TEST_CODE)

    result = testdir.runpytest()

    result.assert_outcomes(passed=1)


def test_mpi_xfail_under_mpi(mpi_testdir, has_mpi4py):
    mpi_testdir.makepyfile(MPI_XFAIL_TEST_CODE)

    result = mpi_testdir.runpytest("--with-mpi")

    if has_mpi4py:
        result.assert_outcomes(xfailed=1)
    else:
        result.assert_outcomes(xpassed=1)

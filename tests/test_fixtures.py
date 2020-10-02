from pytest_mpi._helpers import _fix_plural

MPI_FILE_NAME_TEST_CODE = """
    import pytest

    def test_file_name(mpi_file_name):
        from mpi4py import MPI
        comm = MPI.COMM_WORLD

        name = str(mpi_file_name)
        names = comm.gather(name, root=0)
        if comm.rank == 0:
            for n in names:
                assert n == name
        else:
            assert names is None

"""
MPI_TMPDIR_TEST_CODE = """
    import pytest

    def test_file_name(mpi_tmpdir):
        from mpi4py import MPI
        comm = MPI.COMM_WORLD

        name = str(mpi_tmpdir)
        names = comm.gather(name, root=0)
        if comm.rank == 0:
            for n in names:
                assert n == name
        else:
            assert names is None

"""
MPI_TMP_PATH_TEST_CODE = """
    import pytest

    def test_file_name(mpi_tmp_path):
        from mpi4py import MPI
        comm = MPI.COMM_WORLD

        name = str(mpi_tmp_path)
        names = comm.gather(name, root=0)
        if comm.rank == 0:
            for n in names:
                assert n == name
        else:
            assert names is None

"""


def test_mpi_file_name(mpi_testdir, has_mpi4py):
    mpi_testdir.makepyfile(MPI_FILE_NAME_TEST_CODE)

    result = mpi_testdir.runpytest("--with-mpi", timeout=5)

    if has_mpi4py:
        result.assert_outcomes(passed=1)
    else:
        result.assert_outcomes(**_fix_plural(errors=1))


def test_mpi_tmpdir(mpi_testdir, has_mpi4py):
    mpi_testdir.makepyfile(MPI_TMPDIR_TEST_CODE)

    result = mpi_testdir.runpytest("--with-mpi", timeout=5)

    if has_mpi4py:
        result.assert_outcomes(passed=1)
    else:
        result.assert_outcomes(**_fix_plural(errors=1))


def test_mpi_tmp_path(mpi_testdir, has_mpi4py):
    mpi_testdir.makepyfile(MPI_TMP_PATH_TEST_CODE)

    result = mpi_testdir.runpytest("--with-mpi", timeout=5)

    if has_mpi4py:
        result.assert_outcomes(passed=1)
    else:
        result.assert_outcomes(**_fix_plural(errors=1))

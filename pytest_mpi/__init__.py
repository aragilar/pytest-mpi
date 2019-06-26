"""
Support for testing python code with MPI and pytest
"""
import pytest

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


WITH_MPI_ARG = "--with-mpi"
ONLY_MPI_ARG = "--only-mpi"


class MPIPlugin(object):
    """
    pytest plugin to assist with testing MPI-using code
    """

    def _testing_mpi(self, config):
        """
        Return if we're testing with MPI or not.
        """
        with_mpi = config.getoption(WITH_MPI_ARG)
        only_mpi = config.getoption(ONLY_MPI_ARG)
        return with_mpi or only_mpi

    def pytest_collection_modifyitems(self, config, items):
        """
        Skip tests depending on what options are chosen
        """
        with_mpi = config.getoption(WITH_MPI_ARG)
        only_mpi = config.getoption(ONLY_MPI_ARG)
        for item in items:
            if with_mpi and "mpi_break" in item.keywords:
                item.add_marker(
                    pytest.mark.skip(reason="test does not work under mpi")
                )
            elif only_mpi and "mpi" not in item.keywords:
                item.add_marker(
                    pytest.mark.skip(reason="test does not use mpi")
                )
            elif not (with_mpi or only_mpi) and "mpi" in item.keywords:
                item.add_marker(
                    pytest.mark.skip(reason="need --with-mpi option to run")
                )

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        """
        Hook for printing MPI info at the end of the run
        """
        # pylint: disable=unused-argument
        if self._testing_mpi(config):
            terminalreporter.section("MPI Information")
            try:
                from mpi4py import MPI
            except ImportError:
                terminalreporter.write("Unable to import mpi4py")
            else:
                comm = MPI.COMM_WORLD
                terminalreporter.write("rank: {}\n".format(comm.rank))
                terminalreporter.write("size: {}\n".format(comm.size))

    def pytest_runtest_setup(self, item):
        """
        Hook for doing additional MPI-related checks on mpi marked tests
        """
        if self._testing_mpi(item.config):
            for mark in item.iter_markers(name="mpi"):
                if mark.args:
                    raise ValueError("mpi mark does not take positional args")
                try:
                    from mpi4py import MPI
                except ImportError:
                    pytest.fail("MPI tests require that mpi4py be installed")
                comm = MPI.COMM_WORLD
                min_size = mark.kwargs.get('min_size')
                if min_size is not None and comm.size > min_size:
                    pytest.skip(
                        "Test requires {} MPI processes, only {} MPI "
                        "processes specified, skipping test"
                    )


@pytest.fixture
def mpi_file_name(tmpdir, request):
    """
    Provides a tmpfile name under mpi
    """
    try:
        from mpi4py import MPI
    except ImportError:
        pytest.fail("mpi4py needs to be installed to run this test")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # we only want to put the file inside one tmpdir, this creates the name
    # under one process, and passes it on to the others
    name = str(tmpdir.join(str(request.node) + '.hdf5')) if rank == 0 else None
    name = comm.bcast(name, root=0)
    return name


def pytest_configure(config):
    """
    Add pytest-mpi to pytest (see pytest docs for more info)
    """
    config.addinivalue_line(
        "markers", "mpi: Tests that require being run with MPI/mpirun"
    )
    config.addinivalue_line(
        "markers", "mpi_break: Tests that cannot run under MPI/mpirun"
    )
    config.pluginmanager.register(MPIPlugin(), "pytest_mpi")


def pytest_addoption(parser):
    """
    Add pytest-mpi options to pytest cli
    """
    parser.addoption(
        WITH_MPI_ARG, action="store_true", default=False,
        help="Run MPI tests, this should be paired with mpirun."
    )
    parser.addoption(
        ONLY_MPI_ARG, action="store_true", default=False,
        help="Run *only* MPI tests, this should be paired with mpirun."
    )

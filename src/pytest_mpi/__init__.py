"""
Support for testing python code with MPI and pytest
"""
from enum import Enum
from pathlib import Path

import py
import pytest

from . import _version
__version__ = _version.get_versions()['version']


WITH_MPI_ARG = "--with-mpi"
ONLY_MPI_ARG = "--only-mpi"


class MPIMarkerEnum(str, Enum):
    """
    Enum containing all the markers used by pytest-mpi
    """
    mpi = "mpi"
    mpi_skip = "mpi_skip"
    mpi_xfail = "mpi_xfail"
    mpi_break = "mpi_break"


MPI_MARKERS = {
    MPIMarkerEnum.mpi_skip: pytest.mark.skip(
        reason="test does not work under mpi"
    ),
    MPIMarkerEnum.mpi_break: pytest.mark.skip(
        reason="test does not work under mpi"
    ),
    MPIMarkerEnum.mpi_xfail: pytest.mark.xfail(
        reason="test fails under mpi"
    ),
}


class MPIPlugin(object):
    """
    pytest plugin to assist with testing MPI-using code
    """

    _is_testing_mpi = False

    def _testing_mpi(self, config):
        """
        Return if we're testing with MPI or not.
        """
        with_mpi = config.getoption(WITH_MPI_ARG)
        only_mpi = config.getoption(ONLY_MPI_ARG)
        return with_mpi or only_mpi

    def _add_markers(self, item):
        """
        Add markers to tests when run under MPI.
        """
        for label, marker in MPI_MARKERS.items():
            if label in item.keywords:
                item.add_marker(marker)

    def pytest_configure(self, config):
        """
        Hook setting config object (always called at least once)
        """
        self._is_testing_mpi = self._testing_mpi(config)

    def pytest_collection_modifyitems(self, config, items):
        """
        Skip tests depending on what options are chosen
        """
        with_mpi = config.getoption(WITH_MPI_ARG)
        only_mpi = config.getoption(ONLY_MPI_ARG)
        for item in items:
            if with_mpi:
                self._add_markers(item)
            elif only_mpi and MPIMarkerEnum.mpi not in item.keywords:
                item.add_marker(
                    pytest.mark.skip(reason="test does not use mpi")
                )
            elif not (with_mpi or only_mpi) and (
                    MPIMarkerEnum.mpi in item.keywords
            ):
                item.add_marker(
                    pytest.mark.skip(reason="need --with-mpi option to run")
                )

    def pytest_terminal_summary(self, terminalreporter, exitstatus, *args):
        """
        Hook for printing MPI info at the end of the run
        """
        # pylint: disable=unused-argument
        if self._is_testing_mpi:
            terminalreporter.section("MPI Information")
            try:
                from mpi4py import MPI, rc, get_config
            except ImportError:
                terminalreporter.write("Unable to import mpi4py")
            else:
                comm = MPI.COMM_WORLD
                terminalreporter.write("rank: {}\n".format(comm.rank))
                terminalreporter.write("size: {}\n".format(comm.size))

                terminalreporter.write("MPI version: {}\n".format(
                    '.'.join([str(v) for v in MPI.Get_version()])
                ))
                terminalreporter.write("MPI library version: {}\n".format(
                    MPI.Get_library_version()
                ))

                vendor, vendor_version = MPI.get_vendor()
                terminalreporter.write("MPI vendor: {} {}\n".format(
                    vendor, '.'.join([str(v) for v in vendor_version])
                ))

                terminalreporter.write("mpi4py rc: \n")
                for name, value in vars(rc).items():
                    terminalreporter.write(" {}: {}\n".format(name, value))

                terminalreporter.write("mpi4py config:\n")
                for name, value in get_config().items():
                    terminalreporter.write(" {}: {}\n".format(name, value))

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
                if min_size is not None and comm.size < min_size:
                    pytest.skip(
                        "Test requires {} MPI processes, only {} MPI "
                        "processes specified, skipping "
                        "test".format(min_size, comm.size)
                    )


@pytest.fixture
def mpi_file_name(tmpdir, request):
    """
    Provides a temporary file name which can be used under MPI from all MPI
    processes.

    This function avoids the need to ensure that only one process handles the
    naming of temporary files.
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


@pytest.fixture
def mpi_tmpdir(tmpdir):
    """
    Wraps `pytest.tmpdir` so that it can be used under MPI from all MPI
    processes.

    This function avoids the need to ensure that only one process handles the
    naming of temporary folders.
    """
    try:
        from mpi4py import MPI
    except ImportError:
        pytest.fail("mpi4py needs to be installed to run this test")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # we only want to put the file inside one tmpdir, this creates the name
    # under one process, and passes it on to the others
    name = str(tmpdir) if rank == 0 else None
    name = comm.bcast(name, root=0)
    return py.path.local(name)


@pytest.fixture
def mpi_tmp_path(tmp_path):
    """
    Wraps `pytest.tmp_path` so that it can be used under MPI from all MPI
    processes.

    This function avoids the need to ensure that only one process handles the
    naming of temporary folders.
    """
    try:
        from mpi4py import MPI
    except ImportError:
        pytest.fail("mpi4py needs to be installed to run this test")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # we only want to put the file inside one tmpdir, this creates the name
    # under one process, and passes it on to the others
    name = str(tmp_path) if rank == 0 else None
    name = comm.bcast(name, root=0)
    return Path(name)


def pytest_configure(config):
    """
    Add pytest-mpi to pytest (see pytest docs for more info)
    """
    config.addinivalue_line(
        "markers", "mpi: Tests that require being run with MPI/mpirun"
    )
    config.addinivalue_line(
        "markers", "mpi_break: Tests that cannot run under MPI/mpirun "
        "(deprecated)"
    )
    config.addinivalue_line(
        "markers", "mpi_skip: Tests to skip when running MPI/mpirun"
    )
    config.addinivalue_line(
        "markers", "mpi_xfail: Tests that fail when run under MPI/mpirun"
    )
    config.pluginmanager.register(MPIPlugin())


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

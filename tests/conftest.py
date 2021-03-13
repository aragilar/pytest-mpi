from logging import getLogger
import sys

import py
import pytest

log = getLogger(__name__)
MPI_ARGS = ("mpirun", "-n")
PYTEST_ARGS = (sys.executable, "-mpytest")


@pytest.fixture
def has_mpi4py():
    try:
        import mpi4py
        return True
    except ImportError:
        return False


def _to_py_path(p):
    return py.path.local(p)


def _to_pathlib(p):
    from pathlib import Path
    return Path(p)


class MPITestdir(object):
    def __init__(self, request, config):
        method = request.config.getoption("--runpytest")
        if method == "inprocess":
            log.warn("To run the MPI tests, you need to use subprocesses")
        self._pytester = None
        self._testdir = None
        self._setup(request, config)

    def _setup(self, request, config):
        """
        This handles the difference between Testdir and PyTester
        """
        try:
            self._pytester = request.getfixturevalue("pytester")
        except:
            try:
                self._testdir = request.getfixturevalue("testdir")
            except:
                raise RuntimeError(
                    "Unable to load either pytester or testdir fixtures. "
                    "Check if pytester plugin is enabled."
                )

    def makepyfile(self, *args, **kwargs):
        if self._pytester is not None:
            self._pytester.makepyfile(*args, **kwargs)
        else:
            self._testdir.makepyfile(*args, **kwargs)

    def runpytest(self, *args, **kwargs):
        if self._pytester is not None:
            return self._run_pytester(*args, **kwargs)
        return self._run_testdir(*args, **kwargs)

    def _run_testdir(self, *args, timeout=60, mpi_procs=2, max_retries=5):
        retries = 0
        p = py.path.local.make_numbered_dir(
            prefix="runpytest-", keep=None, rootdir=self._testdir.tmpdir
        )
        args = ("--basetemp=%s" % p,) + args
        plugins = [x for x in self._testdir.plugins if isinstance(x, str)]
        if plugins:
            args = ("-p", plugins[0]) + args
        args = MPI_ARGS + (str(mpi_procs),) + PYTEST_ARGS + args
        while retries < max_retries:
            try:
                return self._testdir.run(*args, timeout=timeout)
            except self._testdir.TimeoutExpired as e:
                retries += 1
                if retries >= max_retries:
                    raise
        raise e

    def _run_pytester(self, *args, timeout=60, mpi_procs=2, max_retries=5):
        retries = 0
        p = _to_pathlib(py.path.local.make_numbered_dir(
            prefix="runpytest-", keep=None,
            rootdir=_to_py_path(self._pytester.path)
        ))
        args = ("--basetemp=%s" % p,) + args
        plugins = [x for x in self._pytester.plugins if isinstance(x, str)]
        if plugins:
            args = ("-p", plugins[0]) + args
        args = MPI_ARGS + (str(mpi_procs),) + PYTEST_ARGS + args
        while retries < max_retries:
            try:
                return self._pytester.run(*args, timeout=timeout)
            except self._pytester.TimeoutExpired as e:
                retries += 1
                if retries >= max_retries:
                    raise
        raise e


@pytest.fixture
def mpi_testdir(request, pytestconfig):
    return MPITestdir(request, pytestconfig)

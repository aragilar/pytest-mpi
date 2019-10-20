.. pytest-mpi documentation master file, created by
   sphinx-quickstart on Wed Jun 26 22:34:19 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytest-mpi's documentation!
======================================

`pytest-mpi` provides a number of things to assist with using pytest with
MPI-using code, specifically:

    * Displaying of the current MPI configuration (e.g. the MPI version, the
      number of processes)
    * Sharing temporary files/folders across the MPI processes
    * Markers which allow for skipping or xfailing tests based on whether the
      tests are being run under MPI

Further features will be added in the future, and contribution of features is
very much welcomed.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   markers
   fixtures
   changelog
   contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

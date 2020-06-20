.. _contributing:

Contributing to pytest-mpi
##########################
We welcome contributions to pytest-mpi, subject to our
`code of conduct <https://github.com/aragilar/pytest-mpi/blob/master/code_of_conduct.md>`_
whether it is improvements to the documentation or examples, bug reports or code
improvements.

Reporting Bugs
--------------
Bugs should be reported to https://github.com/aragilar/pytest-mpi. Please
include what version of Python this occurs on, as well as which operating
system. Information about your h5py and HDF5 configuration is also helpful.

Patches and Pull Requests
-------------------------
The main repository is https://github.com/aragilar/pytest-mpi, please make pull
requests against that repository, and the branch that pull requests should be
made on is master (backporting fixes will be done separately if necessary).

Running the tests
-----------------
pytest-mpi uses tox_ to run its tests. See https://tox.readthedocs.io/en/latest/
for more information about tox, but the simplest method is to run::

    tox

in the top level of the git repository.

.. note::
    If you want to run pytest directly, remember to include ``-p pytester``, as
    pytester needs to be manually activated.

.. _tox: https://tox.readthedocs.io/en/latest/

Making a release
----------------
Current minimal working method (this doesn't produce a release commit, deal
with DOIs needing to be preregistered, not automated, not signed etc.):

#. Checkout the latest commit on the ``master`` branch on the main repository
   locally. Ensure the work directory is clean
   (``git purge``/``git clean -xfd``).
#. Tag this commit with an annotated tag, with the format being ``v*.*.*``
   (``git tag -a v*.*.*``; I should sign these...). The tag should mention the
   changes in this release.
#. Push tag to github.
#. Create a release on github using the web interface, copying the content of
   the tag.
#. Build sdist and wheel (``python setup.py sdist bdist_wheel``), and upload to
   PyPI (``twine upload dist/*``).

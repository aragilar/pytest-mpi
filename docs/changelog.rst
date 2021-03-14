Changelog
=========

0.5
---
* No codebase changes, only testing/CI changes needed to support pytest 6.
* We use Azure Pipelines now for CI, rather than Travis
* Autouploads to PyPI are done via Azure Pipelines
* We test on both pytest<6 and pytest>=6, due to the need to support both for
  now.

0.4
---
* Added license and contributing details
* Added fixtures to enable sharing code across files
* Numerous testing fixes/improvements

0.3
---
* Fixed pylint failures
* Added testing of examples in documentation
* Added proper tests
* Fix bugs found via tests

0.2
---
* Add proper documentation of features
* Display more MPI related information on test run
* Add `mpi_skip` and `mpi_xfail` markers
* Add `mpi_tmpdir` and `mpi_tmp_path`

0.1.1
-----
* Fix plugin as the pytest command line parsing logic needs to be outside main
  plugin class

0.1
---
Initial version

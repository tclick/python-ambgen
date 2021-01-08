========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-ambgen/badge/?style=flat
    :target: https://readthedocs.org/projects/python-ambgen
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/tclick/python-ambgen.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tclick/python-ambgen

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/tclick/python-ambgen?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/tclick/python-ambgen

.. |requires| image:: https://requires.io/github/tclick/python-ambgen/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/tclick/python-ambgen/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/tclick/python-ambgen/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/tclick/python-ambgen

.. |version| image:: https://img.shields.io/pypi/v/ambgen.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/ambgen

.. |wheel| image:: https://img.shields.io/pypi/wheel/ambgen.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/ambgen

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ambgen.svg
    :alt: Supported versions
    :target: https://pypi.org/project/ambgen

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ambgen.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/ambgen

.. |commits-since| image:: https://img.shields.io/github/commits-since/tclick/python-ambgen/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tclick/python-ambgen/compare/v0.1.0...master



.. end-badges

Generate and analyze Amber MD files.

* Free software: BSD 3-Clause License

Installation
============

::

    pip install ambgen

You can also install the in-development version with::

    pip install https://github.com/tclick/python-ambgen/archive/master.zip


Documentation
=============


https://python-ambgen.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

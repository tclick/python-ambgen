# --------------------------------------------------------------------------------------
#  Copyright (C) 2021 by Timothy H. Click <tclick@okstate.edu>
#
#  Permission to use, copy, modify, and/or distribute this software for any purpose
#  with or without fee is hereby granted.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
#  REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
#  FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
#  INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
#  OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
#  TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
#  THIS SOFTWARE.
# --------------------------------------------------------------------------------------

import re
from glob import glob
from os.path import basename
from os.path import splitext
from pathlib import Path

import pkg_resources
from setuptools import find_packages
from setuptools import setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as history_file:
    history = history_file.read().replace(".. :changelog:", "")

# workaround derived from:
# https://stackoverflow.com/questions/49689880/proper-way-to-parse-requirements-file-after-pip-upgrade-to-pip-10-x-x
with Path('requirements/prod.txt').open() as requirements_txt:
    requirements = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with Path('requirements/test.txt').open() as requirements_txt:
    test_requirements = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with Path('requirements/dev.txt').open() as requirements_txt:
    dev_requirements = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

def read(*names, **kwargs):
    """Return the contents of a file.

    Parameters
    ----------
    names : str
        list of filenames
    kwargs : dict
        encoding type of the file
    """
    encoding = kwargs.get("encoding", "utf8")
    filename = Path().joinpath(Path(__file__).parent, *names)
    with open(filename, encoding=encoding) as text_file:
        return text_file.read()


setup(
    name="ambgen",
    version="0.1.0",
    license="BSD-3-Clause",
    description="Generate and analyze Amber MD files.",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Timothy H. Click, Ph.D.",
    author_email="tclick@alumni.ou.edu",
    url="https://github.com/tclick/python-ambgen",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Researchers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    project_urls={
        "Documentation": "https://python-ambgen.readthedocs.io/",
        "Changelog": "https://python-ambgen.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/tclick/python-ambgen/issues",
    },
    keywords=["Amber", "PDB", "molecular dynamics", "quasi-anharmonic analysis"],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements
    },
    entry_points={
        "console_scripts": [
            "ambgen = ambgen.cli:main",
        ]
    },
    test_suite="tests",
    tests_require=test_requirements,
)

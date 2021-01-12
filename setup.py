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
from pathlib import Path

import pkg_resources
from setuptools import find_packages, setup

with Path("README.rst").open() as readme_file:
    readme = readme_file.read()

with Path("CHANGELOG.rst").open() as history_file:
    history = history_file.read().replace(".. :changelog:", "")

with Path("requirements/prod.txt").open() as requirements_txt:
    requirements = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

with Path("requirements/test.txt").open() as requirements_txt:
    test_requirements = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]


def read(*names, **kwargs):
    dir_name = Path(__file__).parent
    with dir_name.joinpath(*names).open(encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


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
    py_modules=[path.name for path in Path("src").glob("*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
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
        "dev": [
            "black",
            "bumpversion",
            "coverage",
            "flake8",
            "ipython",
            "pre-commit",
            "pylint",
            "setuptools",
            "tox",
            "twine",
            "wheel",
            "Sphinx",
        ]
    },
    entry_points={
        "console_scripts": [
            "ambgen = ambgen.cli:main",
        ]
    },
    test_suite="tests",
    tests_require=test_requirements,
)

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
import runpy

import pytest
from click.testing import CliRunner

from ambgen import create_logging_dict
from ambgen.cli import main


def test_main_module():
    sys_dict = runpy.run_module("ambgen", init_globals={"__name__": "__main__"})
    assert sys_dict["__name__"] == "ambgen.__main__"
    assert isinstance(sys_dict["main"], type(main))


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, args=("-h",))

    assert "Usage:" in result.output
    assert result.exit_code == 0


def test_create_logging_dict():
    logfile = "test.log"
    assert isinstance(create_logging_dict(logfile), dict)


def test_create_logging_dict_error():
    logfile = ""
    with pytest.raises(ValueError):
        create_logging_dict(logfile)

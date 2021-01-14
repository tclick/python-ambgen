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
import shutil
from pathlib import Path

from click.testing import CliRunner

from ambgen.cli import main
from ..datafile import TOP


def test_prepfiles_help():
    runner = CliRunner()
    result = runner.invoke(
        main,
        args=(
            "prepfiles",
            "-h",
        ),
        env=dict(AMBERHOME=Path(shutil.which("sander")).parent.parent.as_posix()),
    )

    assert "Usage:" in result.output
    assert result.exit_code == 0


def test_prepfiles():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            args=(
                "simfiles",
                "-s",
                f"{TOP}",
                "-p",
                "rnase2",
                "-l",
                Path.cwd().joinpath("prepare.log").as_posix(),
            ),
            env=dict(AMBERHOME=Path(shutil.which("sander")).parent.parent.as_posix()),
        )
        assert Path("prepare.log").exists()
        assert result.exit_code == 0

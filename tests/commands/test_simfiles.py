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

import pytest
from click.testing import CliRunner

import ambgen
from ambgen.cli import main
from ..datafile import TOP


def test_simfiles_help(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        main,
        args=(
            "simfiles",
            "-h",
        ),
        env=dict(AMBERHOME=tmp_path.as_posix()),
    )

    assert "Usage:" in result.output
    assert result.exit_code == 0


@pytest.mark.parametrize("sim_type", "equil prod shell all".split())
def test_simfiles(tmp_path, sim_type):
    runner = CliRunner()
    logfile = tmp_path.joinpath("prepare.log")
    result = runner.invoke(
        main,
        args=(
            "simfiles",
            "-s",
            f"{TOP}",
            "-d",
            tmp_path,
            "-p",
            "rnase2",
            "-l",
            logfile.as_posix(),
            "--type",
            sim_type,
        ),
        env=dict(AMBERHOME=tmp_path.as_posix()),
    )
    assert logfile.exists()
    assert result.exit_code == 0
    assert len([_ for _ in tmp_path.joinpath("Input").iterdir()]) > 0


def test_write_template(tmp_path, mocker):
    runner = CliRunner()
    logfile = tmp_path.joinpath("prepare.log")
    with mocker.patch("ambgen.commands.cmd_simfiles._write_template"):
        runner.invoke(
            main,
            args=(
                "simfiles",
                "-s",
                f"{TOP}",
                "-d",
                tmp_path,
                "-p",
                "rnase2",
                "-l",
                logfile.as_posix(),
            ),
            env=dict(AMBERHOME=tmp_path.as_posix()),
        )
        ambgen.commands.cmd_simfiles._write_template.assert_called()


def test_shell_chmod(tmp_path):
    runner = CliRunner()
    logfile = tmp_path.joinpath("prepare.log")
    equil_file = tmp_path.joinpath("Input", "equilibrate.sh")

    runner.invoke(
        main,
        args=(
            "simfiles",
            "-s",
            f"{TOP}",
            "-d",
            tmp_path,
            "-p",
            "rnase2",
            "-l",
            logfile.as_posix(),
            "--type",
            "shell",
        ),
        env=dict(AMBERHOME=tmp_path.as_posix()),
    )
    assert equil_file.exists()
    assert oct(equil_file.stat().st_mode)[5:] == "755"

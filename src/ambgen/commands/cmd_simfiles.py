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
"""Prepares various Amber input files for use in simulations.

Various Amber input files are created from templates. The input files follow the
protocol set forth in the Agarwal group. The production runs are microcanonical
simulations (NVE), and the equilibration runs involve both canonical (NVT) and
isobaric-isothermal (NPT) simulations with minimization steps between the equilibration
runs.
"""
import glob
import logging
import logging.config
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

import MDAnalysis as mda
import click
from jinja2 import Environment
from jinja2 import PackageLoader

from .. import create_logging_dict


@dataclass
class Data:
    temp1: float
    temp2: float
    res0: int
    res1: int
    ions0: int
    ions1: int
    solvent0: int
    solvent1: int
    force: float
    simdir: Path
    prefix: str
    amberhome: Path
    pmemd: str


def _write_template(
    env: Environment, temploc: str, data: Data, subdir: Path, logger: logging.Logger
) -> NoReturn:
    env.loader = PackageLoader("ambgen", package_path=f"templates/{temploc}")
    for filename in env.loader.list_templates():
        input_file = (
            (subdir / filename).with_suffix(".sh")
            if temploc == "scripts"
            else (subdir / filename).with_suffix(".in")
        )
        with open(input_file, mode="w") as inf:
            template = env.get_template(filename)
            logger.info(f"Writing script to {input_file}")
            print(template.render(data=data), file=inf)


@click.command("prepfiles", short_help="Prepare Amber input files.")
@click.option(
    "-s",
    "--topology",
    metavar="FILE",
    default="amber.prmtop",
    show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="Topology file",
)
@click.option(
    "-d",
    "--simdir",
    metavar="DIR",
    default=Path.cwd(),
    show_default=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Simulation subdirectory",
)
@click.option(
    "-p",
    "--prefix",
    metavar="PREFIX",
    default=Path.cwd().stem,
    show_default=True,
    help="Prefix for various output files",
)
@click.option(
    "--temp1",
    metavar="TEMP",
    default=100.0,
    show_default=True,
    type=click.IntRange(min=1.0, clamp=True),
    help="Initial temperature (K)",
)
@click.option(
    "--temp2",
    metavar="TEMP",
    default=300.0,
    show_default=True,
    type=click.IntRange(min=1.0, clamp=True),
    help="Final temperature (K)",
)
@click.option(
    "--force",
    metavar="FORCE",
    default=100.0,
    show_default=True,
    type=click.IntRange(min=1.0, clamp=True),
    help="Restraint force (kcal/mol/A^2",
)
@click.option(
    "-l",
    "--logfile",
    metavar="LOG",
    default=Path.cwd() / "prepare.log",
    show_default=True,
    type=click.Path(exists=False, file_okay=True, resolve_path=True),
    help="Log file",
)
@click.option(
    "--home",
    metavar="DIR",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Location of Amber files",
)
@click.option(
    "--type",
    "outtype",
    default="all",
    show_default=True,
    type=click.Choice("equil prod shell all".split(), case_sensitive=False),
    help="Which output files to create",
)
def cli(
    topology: str,
    simdir: str,
    prefix: str,
    temp1: float,
    temp2: float,
    force: float,
    logfile: str,
    home: str,
    outtype: str,
):
    """Prepare various Amber input files to run simulations."""
    logging.config.dictConfig(create_logging_dict(logfile))
    logger: logging.Logger = logging.getLogger(__name__)

    universe = mda.Universe(topology)
    protein = universe.select_atoms("protein")
    ions = universe.select_atoms("name Na+ K+ Cl-")
    solvent = universe.select_atoms("resname WAT")
    if home:
        amberhome = Path(home)
    else:
        try:
            amberhome = Path(os.environ["AMBERHOME"])
        except KeyError:
            logger.exception(
                "AMBERHOME environment variable not defined.", exc_info=True
            )

    simdir = Path(simdir)
    data = Data(
        temp1=temp1,
        temp2=temp2,
        res0=protein.resnums[0],
        res1=protein.resnums[-1],
        ions0=ions.resnums[0],
        ions1=ions.resnums[-1],
        solvent0=solvent.resnums[0],
        solvent1=solvent.resnums[-1],
        force=force,
        simdir=simdir,
        prefix=prefix,
        amberhome=amberhome,
        pmemd=(
            "pmemd.MPI"
            if shutil.which(amberhome / "bin" / "pmemd.MPI") is not None
            else "pmemd"
        ),
    )

    # Write input files to input subdirectory
    subdir = simdir / "Input"
    subdir.mkdir(parents=True, exist_ok=True)

    env = Environment(autoescape=True)
    temploc = []
    if outtype.lower() == "equil":
        temploc.append("equil")
    elif outtype.lower() == "prod":
        temploc.append("prod")
    elif outtype.lower() == "shell":
        temploc.append("scripts")
    else:
        temploc.extend(["equil", "prod", "scripts"])

    for _ in temploc:
        _write_template(env, _, data, subdir, logger)

    # Write the shell scripts
    for _ in glob.iglob("Input/*.sh"):
        Path(_).chmod(0o755)

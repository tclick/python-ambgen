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

import os
import subprocess
import sys
from pathlib import Path

base_path = Path(__file__).absolute().parent.parent


def check_call(args):
    print("+", *args)
    subprocess.check_call(args)


def exec_in_env():
    env_path = base_path.joinpath(".tox").joinpath("bootstrap")
    if sys.platform == "win32":
        bin_path = env_path.joinpath("Scripts")
    else:
        bin_path = env_path.joinpath("bin")
    if not env_path.exists:
        import subprocess

        print(f"Making bootstrap env in: {env_path} ...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", env_path])
        except subprocess.CalledProcessError:
            try:
                subprocess.check_call([sys.executable, "-m", "virtualenv", env_path])
            except subprocess.CalledProcessError:
                subprocess.check_call(["virtualenv", env_path])
        print("Installing `jinja2` into bootstrap environment...")
        subprocess.check_call([bin_path.joinpath("pip"), "install", "jinja2", "tox"])
    python_executable = bin_path.joinpath("python")
    if not python_executable.exists:
        python_executable += ".exe"

    print(f"Re-executing with: {python_executable}")
    print("+ exec", python_executable, __file__, "--no-env")
    os.execv(python_executable, [python_executable, __file__, "--no-env"])


def main():
    import jinja2

    print(f"Project path: {base_path}")

    jinja = jinja2.Environment(
        loader=jinja2.FileSystemLoader(base_path.joinpath("ci").joinpath("templates")),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    tox_environments = [
        line.strip()
        # 'tox' need not be installed globally, but must be importable
        # by the Python that is running this script.
        # This uses sys.executable the same way that the call in
        # cookiecutter-pylibrary/hooks/post_gen_project.py
        # invokes this bootstrap.py itself.
        for line in subprocess.check_output(
            [sys.executable, "-m", "tox", "--listenvs"], universal_newlines=True
        ).splitlines()
    ]
    tox_environments = [line for line in tox_environments if line.startswith("py")]

    for name in Path("ci").joinpath("templates").iterdir():
        with open(base_path.joinpath(name), "w") as fh:
            fh.write(jinja.get_template(name).render(tox_environments=tox_environments))
        print(f"Wrote {name}")
    print("DONE.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--no-env"]:
        main()
    elif not args:
        exec_in_env()
    else:
        print(f"Unexpected arguments {args}", file=sys.stderr)
        sys.exit(1)

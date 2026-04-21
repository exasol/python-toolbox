import os
import shutil
import site
import subprocess
from pathlib import Path

from noxconfig import PROJECT_CONFIG


def get_env(test_path: Path) -> dict[str, str]:
    venv_bin = test_path / "venv" / "bin"
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(test_path / "venv")
    env["PATH"] = f"{venv_bin}{os.pathsep}{env['PATH']}"
    env["PYTHONPATH"] = os.pathsep.join(site.getsitepackages())
    return env


def test_security_issues_works(tmp_path):
    """
    To ensure that the `tbx security cve` CLI commands work for Java and
    other non-Python projects, this test was created which:
      - builds a wheel of the python-toolbox
      - installs the wheel in a temporary directory
      - executes `tbx security cve -- help` to ensure that no errors occur

    This issue primarily arises when one of the modules in `tools` imports something
    from `noxconfig`, which is used in the Python projects using the toolbox, but it
    is not needed nor used in the non-Python projects.
    """
    build_output = subprocess.run(["poetry", "build", "--output", tmp_path])
    assert build_output.returncode == 0

    venv_output = subprocess.run(["python", "-m", "venv", "venv"], cwd=tmp_path)
    assert venv_output.returncode == 0

    env = get_env(tmp_path)
    wheel = min(tmp_path.glob("exasol_toolbox-*.whl"))
    pip_output = subprocess.run(
        ["pip", "install", "--no-deps", str(wheel)], cwd=tmp_path, env=env
    )
    assert pip_output.returncode == 0

    tbx_output = subprocess.run(
        ["tbx", "security", "cve", "--help"], cwd=tmp_path, env=env
    )
    assert tbx_output.returncode == 0


def test_security_issues_fails_when_imports_noxconfig(tmp_path):
    """
    Reproduces the failure mode where a toolbox runtime module imports
    `noxconfig`, which is not available in non-Python projects.
    """
    source_root = PROJECT_CONFIG.root_path
    project_copy = tmp_path / "python-toolbox-copy"
    shutil.copytree(
        source_root,
        project_copy,
        ignore=shutil.ignore_patterns(
            ".git", ".venv", "dist", "__pycache__", ".pytest_cache"
        ),
    )

    security_py = project_copy / "exasol" / "toolbox" / "tools" / "security.py"
    security_text = security_py.read_text()
    security_py.write_text(
        security_text.replace(
            "from __future__ import annotations\n",
            "from __future__ import annotations\n\nfrom noxconfig import PROJECT_CONFIG\n",
            1,
        )
    )

    build_output = subprocess.run(
        ["poetry", "build", "--output", tmp_path], cwd=project_copy
    )
    assert build_output.returncode == 0

    venv_output = subprocess.run(["python", "-m", "venv", "venv"], cwd=tmp_path)
    assert venv_output.returncode == 0

    env = get_env(tmp_path)
    wheel = min(tmp_path.glob("exasol_toolbox-*.whl"))
    pip_output = subprocess.run(
        ["pip", "install", "--no-deps", str(wheel)], cwd=tmp_path, env=env
    )
    assert pip_output.returncode == 0

    tbx_output = subprocess.run(
        ["tbx", "security", "cve", "--help"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert tbx_output.returncode != 0
    assert "No module named 'noxconfig'" in tbx_output.stderr

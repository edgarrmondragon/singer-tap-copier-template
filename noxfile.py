"""Nox configuration."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import nox

STREAM_TYPES = ["REST", "GraphQL"]
AUTH_METHODS = [
    "Bearer Token",
    "JWT",
    "API Key",
    "Basic Auth",
    "OAuth2",
    "Custom or N/A",
]
VISIBILITIES = ["private", "public"]
RUFF_OVERRIDES = """\
extend = "./pyproject.toml"

[lint]
extend-ignore = ["TD003"]
"""
python_versions = ["3.12", "3.11", "3.10", "3.9", "3.8"]


@nox.session(python=python_versions)
@nox.parametrize("stream_type", STREAM_TYPES)
@nox.parametrize("auth_method", AUTH_METHODS)
@nox.parametrize("visibility", VISIBILITIES)
def lint(
    session: nox.sessions.Session,
    stream_type: str,
    auth_method: str,
    visibility: str,
) -> None:
    """Lint generated project."""
    ref = session.posargs[0] if session.posargs else "HEAD"

    with TemporaryDirectory() as tmpdir:
        session.run(
            "copier",
            "copy",
            ".",
            tmpdir,
            "--UNSAFE",
            f"--vcs-ref={ref}",
            "--force",
            "--defaults",
            "-d",
            f"python_main_version='{session.python}'",
            "-d",
            f"tap_stream_type={stream_type}",
            "-d",
            f"tap_auth_method={auth_method}",
            "-d",
            f"repository_visibility={visibility}",
            external=True,
        )

        ruff_toml_path = Path(tmpdir).joinpath("ruff.toml")
        with ruff_toml_path.open("w") as ruff_toml:
            ruff_toml.write(RUFF_OVERRIDES)

        with session.cd(tmpdir):
            session.run("git", "init", external=True)
            session.run("git", "add", ".", external=True)
            session.run(
                "hatch",
                "run",
                f"+py={session.python}",
                "test:dependencies",
                external=True,
            )
            session.run(
                "hatch",
                "run",
                f"+py={session.python}",
                "typing:check",
                external=True,
            )
            session.run("pre-commit", "run", "--all", external=True)

"""Nox configuration."""

from __future__ import annotations
from pathlib import Path
from tempfile import TemporaryDirectory

import nox

python_versions = ["3.10", "3.9", "3.8", "3.7"]


@nox.session(python=python_versions)
@nox.parametrize("stream_type", ["REST", "GraphQL"])
@nox.parametrize(
    "auth_method",
    [
        "Bearer Token",
        "JWT",
        "API Key",
        "Basic Auth",
        "OAuth2",
        "Custom or N/A",
    ],
)
def lint(session: nox.sessions.Session, stream_type: str, auth_method: str) -> None:
    """Lint generated project."""
    ref = session.posargs[0] if session.posargs else "HEAD"

    with TemporaryDirectory() as tmpdir:
        session.run(
            "copier",
            ".",
            tmpdir,
            f"--vcs-ref={ref}",
            "--force",
            "--defaults",
            "-d",
            f"python_main_version='{session.python}'",
            "-d",
            f"tap_stream_type={stream_type}",
            "-d",
            f"tap_auth_method={auth_method}",
            external=True,
        )
        with session.cd(tmpdir):
            session.run("tox", "-e", "lint", "-v", external=True)

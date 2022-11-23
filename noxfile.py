"""Nox sessions."""
import platform

from nox import options
from nox_poetry import Session, session

options.sessions = ["tests", "mypy"]
python_versions = ["3.10"]


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    dependencies = ["invoke", "pytest", "xdoctest", "coverage[toml]", "pytest-cov"]
    session.install(".", *dependencies)
    try:
        session.run(
            "inv",
            "tests",
            env={
                "COVERAGE_FILE": f".coverage.{platform.system()}.{platform.python_version()}",
            },
        )
    finally:
        if session.interactive:
            session.notify("coverage")


@session
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs if session.posargs and len(session._runner.manifest) == 1 else []
    dependencies = ["invoke", "coverage[toml]"]
    session.install(*dependencies)
    session.run("inv", "coverage", *args)


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    dependencies = ["invoke", "mypy"]
    session.install(".", *dependencies)
    session.run("inv", "mypy")


@session(python=python_versions)
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    dependencies = ["invoke", "safety"]
    session.install(*dependencies)
    session.run("inv", "safety")

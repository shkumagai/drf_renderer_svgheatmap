import os

import nox

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})


def run_pytest(session):
    """Run unittest with pytest."""

    posargs = session.posargs if session.posargs else ["tests"]

    session.install(".[testing]")
    session.run(
        "pytest",
        *posargs,
        env={
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOWARNINGS": "once",
            "PYTEST_ADDOPTS": "--cov --cov-config=pyproject.toml --cov-report=term-missing -vv",
        },
    )


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def test_dj32(session):
    """Run tests against Django ~= 3.2."""

    session.install("django ~= 3.2")
    run_pytest(session)


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def test_dj40(session):
    """Run tests against Django ~= 4.0."""

    session.install("django ~= 4.0")
    run_pytest(session)


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def test_dj41(session):
    """Run tests against Django ~= 4.1."""

    session.install("django ~= 4.1")
    run_pytest(session)


@nox.session(python=["3.10", "3.11"])
def test_djmain(session):
    """Run tests against Django HEAD main (development)."""

    session.install("django @ https://github.com/django/django/archive/main.tar.gz")
    run_pytest(session)


@nox.session(tags=["style", "lint"])
def black(session):
    """Apply black format rules."""

    posargs = (
        session.posargs
        if session.posargs
        else ["--check", "--diff", "drf_renderer_svgheatmap", "tests", "noxfile.py"]
    )

    session.install("black")
    session.run("black", *posargs)


@nox.session(tags=["style", "lint"])
def isort(session):
    """Apply isort import format rules."""

    posargs = (
        session.posargs
        if session.posargs
        else ["--check-only", "--diff", "drf_renderer_svgheatmap", "tests"]
    )

    session.install("isort")
    session.run("isort", *posargs)


@nox.session
def fmt(session):
    """Format code using black and isort."""

    posargs = (
        session.posargs
        if session.posargs
        else ["drf_renderer_svgheatmap", "tests", "noxfile.py"]
    )

    session.notify("black", posargs=posargs)
    session.notify("isort", posargs=posargs)


@nox.session(tags=["style", "lint"])
def flake8(session):
    """Apply flake8 rules."""

    posargs = (
        session.posargs
        if session.posargs
        else ["drf_renderer_svgheatmap", "tests", "noxfile.py"]
    )

    session.install("flake8")
    session.install("flake8-copyright")
    session.install("flake8-commas")
    session.install("flake8-print")
    session.install("flake8-return")
    session.install("flake8-string-format")
    session.run("flake8", *posargs)


@nox.session(tags=["security", "lint"])
def bandit(session):
    """Run security check."""

    posargs = (
        session.posargs
        if session.posargs
        else ["drf_renderer_svgheatmap", "tests/test_*.py", "noxfile.py"]
    )

    session.install("bandit[toml]")
    session.run(
        # fmt: off
        "bandit", "-c", "pyproject.toml",
        "--quiet",
        "--recursive",
        *posargs,
        # fmt: on
    )


@nox.session(tags=["typing", "lint"])
def mypy(session):
    """Run static type check."""

    posargs = session.posargs if session.posargs else ["drf_renderer_svgheatmap"]

    session.install("mypy")
    session.run("mypy", *posargs)


@nox.session(tags=["lint"])
def tomlcheck(session):
    """Run toml format check."""

    session.install("tomlcheck")
    session.run("tomlcheck", "pyproject.toml")

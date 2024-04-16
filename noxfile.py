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


@nox.session(python=["3.8", "3.9", "3.10"])
def test_dj40(session):
    """Run tests against Django ~= 4.0."""

    session.install("django ~= 4.0")
    run_pytest(session)


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def test_dj41(session):
    """Run tests against Django ~= 4.1."""

    session.install("django ~= 4.1")
    run_pytest(session)


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def test_dj42(session):
    """Run tests against Django ~= 4.2."""

    session.install("django ~= 4.2")
    run_pytest(session)


@nox.session(python=["3.10", "3.11", "3.12"])
def test_dj50(session):
    """Run tests against Django ~= 5.0."""

    session.install("django ~= 5.0")
    run_pytest(session)


@nox.session(python=["3.10", "3.11", "3.12"])
def test_djmain(session):
    """Run tests against Django HEAD main (development)."""

    session.install("django @ https://github.com/django/django/archive/main.tar.gz")
    run_pytest(session)


@nox.session(tags=["lint"])
def check(session):
    """ruffを使ってpythonコードの文法チェックを実行します

    # すべてのファイル・パスを対象にruffを実行します
    $ nox --session check

    # 特定のファイル・パスを対象にruffを実行します
    $ nox --session check -- noxfile.py
    """
    posargs = (
        session.posargs
        if session.posargs
        else ["check", "--fix", "drf_renderer_svgheatmap", "tests", "noxfile.py"]
    )

    session.notify("ruff", posargs=posargs)


@nox.session
def format(session):
    """ruffを使ってpythonコードの文法チェックを実行します

    # すべてのファイル・パスを対象にruffを実行します
    $ nox --session check

    # 特定のファイル・パスを対象にruffを実行します
    $ nox --session check -- noxfile.py
    """
    posargs = (
        session.posargs
        if session.posargs
        else ["format", "drf_renderer_svgheatmap", "tests", "noxfile.py"]
    )

    session.notify("ruff", posargs=posargs)


@nox.session
def ruff(session):
    """ruffを実行します

    # すべてのファイル・パスを対象にruffを実行します
    $ nox --session ruff

    # 特定のファイル・パスを対象にruffを実行します
    $ nox --session ruff -- noxfile.py
    """

    posargs = (
        session.posargs
        if session.posargs
        else ["check", "drf_renderer_svgheatmap", "tests", "noxfile.py"]
    )

    session.install("ruff")
    session.run("ruff", *posargs)


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
        "bandit",
        "-c",
        "pyproject.toml",
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

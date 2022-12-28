import subprocess
import sys

import click

from utils.base_dir import BASE_DIR

ALEMBIC_CONFIG_FILE = BASE_DIR / "migrations" / "alembic.ini"


@click.group()
def migrations() -> None:
    """Миграции базы данных."""


@migrations.command()
@click.option("--revision", default="head", type=str)
def up(revision: str) -> None:  # pylint: disable=invalid-name
    """Мигрировать до заданной миграции в сторону обновления."""
    validate_revision(revision)

    try:
        subprocess.check_call(f"alembic -c {ALEMBIC_CONFIG_FILE} upgrade {revision}", shell=True)
    except subprocess.CalledProcessError as err:
        sys.exit(err.returncode)


@migrations.command()
@click.option("--revision", default="-1")
def down(revision: str) -> None:
    """Откатиться до заданной миграции."""
    validate_revision(revision)

    try:
        subprocess.check_call(f"alembic -c {ALEMBIC_CONFIG_FILE} downgrade {revision}", shell=True)
    except subprocess.CalledProcessError as err:
        sys.exit(err.returncode)


@migrations.command()
@click.argument("name", type=str)
def make(name: str) -> None:
    """Создать миграцию с заданным именем."""
    validate_revision(name)

    try:
        subprocess.check_call(
            f"alembic -c {ALEMBIC_CONFIG_FILE} revision --autogenerate --message {name}", shell=True
        )
    except subprocess.CalledProcessError as err:
        sys.exit(err.returncode)


def validate_revision(revision: str) -> None:
    """Валидировать название ревизии.

    :param revision: название ревизии
    :raises BadArgumentUsage: в случае невалидной ревизии
    """
    no_spaces = revision.strip()
    if " " in no_spaces:
        raise click.BadArgumentUsage(
            f"Invalid revision: '{revision}'. Revision must be one word without any spaces."
        )

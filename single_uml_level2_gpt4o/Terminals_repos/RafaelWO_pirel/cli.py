import logging
import click
from rich.console import Console
from rich.table import Table
from pirel import CONTEXT, __version__
from pirel.releases import load_releases
from pirel.python_cli import get_active_python_info
from pirel._cache import clear, calc_cache_age_days, get_latest_cache_file
from pirel._guess import get_random_question, store_question_score

logger = logging.getLogger(__name__)

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose output.")
@click.option('--no-cache', is_flag=True, help="Disable caching.")
@click.option('--version', is_flag=True, help="Show the version and exit.")
@click.pass_context
def main(ctx, verbose, no_cache, version):
    """The Python release cycle in your terminal."""
    if version:
        click.echo(f"pirel version {__version__}")
        ctx.exit()
    ctx.obj = CONTEXT
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    if no_cache:
        clear(True)

@main.command()
@click.pass_context
def list_releases(ctx):
    """Lists all Python releases in a table. Your active Python interpreter is highlighted."""
    releases = ctx.obj.releases
    active_python_info = get_active_python_info()
    table = releases.to_table(active_python_info.version if active_python_info else None)
    console = ctx.obj.rich_console
    console.print(table)

@main.command()
@click.pass_context
def check_release(ctx):
    """Shows release information about your active Python interpreter."""
    active_python_info = get_active_python_info()
    if not active_python_info:
        click.echo("No active Python interpreter found.")
        ctx.exit(2)
    releases = ctx.obj.releases
    release = releases[active_python_info.version]
    console = ctx.obj.rich_console
    console.print(release)
    if release.is_eol:
        ctx.exit(1)

@main.command()
@click.pass_context
def print_releases(ctx):
    """Prints all Python releases as a table."""
    releases = ctx.obj.releases
    table = releases.to_table()
    console = ctx.obj.rich_console
    console.print(table)

@main.command()
@click.pass_context
def ask_random_question(ctx):
    """Prompts the user with a random question regarding Python releases."""
    question = get_random_question()
    correct = question.ask()
    store_question_score(question, correct)

@main.command()
@click.pass_context
def logging_callback(ctx, verbosity):
    """Configure logging verbosity based on the provided verbosity level."""
    if verbosity:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

@main.command()
@click.pass_context
def version_callback(ctx, value):
    """Print the version of the 'pirel' package and exit the program when a boolean flag is set to True."""
    if value:
        click.echo(f"pirel version {__version__}")
        ctx.exit()

if __name__ == "__main__":
    main()
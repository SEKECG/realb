import click
from pirel.cli import main

@click.command()
@click.option('--no-cache', is_flag=True, help="Disable cache usage.")
@click.option('--verbose', count=True, help="Increase verbosity.")
@click.option('--version', is_flag=True, help="Show the version and exit.")
def cli(no_cache, verbose, version):
    main(no_cache=no_cache, verbose=verbose, version=version)

if __name__ == "__main__":
    cli()
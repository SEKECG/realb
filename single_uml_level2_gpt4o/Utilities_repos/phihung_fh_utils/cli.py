import typer
from rich import print
from fh_utils.server import serve_dev, serve_prod
from fh_utils import __version__

app = typer.Typer()
logger = typer.Typer()

def _parse_uvicorn_argument(args):
    return {arg.split("=")[0]: arg.split("=")[1] for arg in args}

@app.callback()
def callback(version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True)):
    """
    fh_utils CLI - The [bold]fh_utils[/bold] command line app. 🛠️

    Manage your [bold]FastHTML[/bold] projects, run your FastHTML apps, and more.

    Read more in the docs: [link]https://github.com/phihung/fh_utils/[/link].
    """
    pass

@app.command()
def dev(path: str, app: str, host: str = "127.0.0.1", port: int = 8000, reload: bool = True, live: bool = True, ctx: typer.Context = None):
    """
    Start FastHTML app in [green]dev mode[/green].

    The command accepts uvicorn arguments such as --reload-include and --log-level (see [green]uvicorn[/green] --help for more).
    """
    uvicorn_args = _parse_uvicorn_argument(ctx.args)
    serve_dev(path, app, host, port, live, reload, **uvicorn_args)

@app.command()
def run(path: str, app: str, host: str = "127.0.0.1", port: int = 8000, ctx: typer.Context = None):
    """
    Start FastHTML app in [green]production mode[/green].

    The command accepts uvicorn arguments such as --reload-include and --log-level (see [green]uvicorn[/green] --help for more).
    """
    uvicorn_args = _parse_uvicorn_argument(ctx.args)
    serve_prod(path, app, host, port, **uvicorn_args)

def version_callback(value: bool):
    if value:
        print(f"fh_utils version: {__version__}")
        raise typer.Exit()

if __name__ == "__main__":
    app()
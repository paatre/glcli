from typing import Annotated, Optional
import typer
from .client import get_gitlab_instance


app = typer.Typer(
    invoke_without_command=True,
)


@app.callback()
def main(
    ctx: typer.Context,
    config: Annotated[
        Optional[str],
        typer.Option(
            "--config",
            "-c",
            help="Path to your config.toml (overrides ~/.config/glcli/config.toml)",
        ),
    ] = None,
):
    """
    An interactive command-line tool for GitLab REST API.
    """
    if ctx.invoked_subcommand is None:
        gl = get_gitlab_instance(config)


if __name__ == "__main__":
    app()

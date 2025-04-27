import os
import typer
from typing import Annotated, Optional

app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=True,
)


@app.callback()
def main(
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
    if config:
        from config import Settings

        global settings
        settings = Settings(config_file=config)
        typer.echo(f"Using config file: {config}")


if __name__ == "__main__":
    app()

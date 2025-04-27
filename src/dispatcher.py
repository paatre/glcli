import gitlab
import typer
from fzf_wrapper import prompt


def run(gl: gitlab.Gitlab) -> None:
    """
    Spin up the REPL: pick an API and dispatch to its interactive() function.
    """
    while True:
        choice = prompt(
            ["projects", "quit"],
        )
        if not choice:
            typer.echo("No choice, exiting.")
            raise typer.Exit()

        api = choice[0].lower()
        match api:
            case "projects":
                typer.echo("Projects API selected.")
                raise typer.Exit()
            case "quit":
                typer.echo("👋  Goodbye!")
                raise typer.Exit()
            case _:
                typer.echo(f"Unknown API: {api!r}")
                raise typer.Exit()

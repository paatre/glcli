import gitlab
import typer
from fzf_wrapper import prompt
from .apis.registry import ApiRegistry

def run(gl: gitlab.Gitlab) -> None:
    apis = ApiRegistry.get_apis()
    choices = list(apis.keys()) + ["quit"]

    while True:
        choice = prompt(choices)
        if not choice:
            typer.echo("No choice, exiting.")
            raise typer.Exit()
        cmd = choice[0].lower()
        if cmd == "quit":
            typer.echo("👋  Goodbye!")
            raise typer.Exit()
        apis[cmd]().interactive(gl)

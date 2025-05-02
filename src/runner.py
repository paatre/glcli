import gitlab
import typer
from .adapters import get_adapters_for
from .fzf import prompt


def run(gl: gitlab.Gitlab) -> None:
    adapters = get_adapters_for(gl)
    choices = list(adapters.keys()) + ["quit"]

    while True:
        header = f"Choose a GitLab API"
        selection = prompt(choices, header=header)

        if not selection:
            typer.echo("No choice, exiting.")
            raise typer.Exit()

        cmd = selection[0]
        if cmd == "quit":
            typer.echo("👋  Goodbye!")
            raise typer.Exit()

        adapter = adapters.get(cmd)
        if adapter:
            typer.secho(f"You selected {cmd}", fg="green")
            adapter.interactive()
        else:
            typer.secho(f"⚠️  No adapter registered for “{cmd}”", fg="red")

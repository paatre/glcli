import importlib, pkgutil
import gitlab
import typer
from fzf_wrapper import prompt
from .apis.registry import ApiRegistry


def _import_all_apis() -> None:
    from . import apis

    for _, modname, _ in pkgutil.iter_modules(apis.__path__):
        importlib.import_module(f"{apis.__name__}.{modname}")


def run(gl: gitlab.Gitlab) -> None:
    _import_all_apis()

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

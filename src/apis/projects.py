import typer
from gitlab import Gitlab
from .base import GitlabAPI
from .registry import ApiRegistry


@ApiRegistry.register()
class ProjectsApi(GitlabAPI):
    name = "projects"

    def interactive(self, gl: Gitlab) -> None:
        typer.echo("Projects API selected.")
        raise typer.Exit()

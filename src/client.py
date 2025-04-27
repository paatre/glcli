from typing import Optional
import gitlab
import typer
from yaspin import yaspin
from .config import Config


def get_gitlab_instance(
    config_file: Optional[str] = None,
) -> gitlab.Gitlab:
    """
    Load Config (TOML/env), then authenticate to GitLab.
    Exits with an error message if authentication or connection fails.
    """
    try:
        typer.secho("Authenticating with GitLab…", fg="yellow")
        with yaspin(text="Authenticating with GitLab…", color="yellow"):
            cfg = Config.load(config_file)
            gl = gitlab.Gitlab(
                cfg.gitlab_url, private_token=cfg.private_access_token, timeout=20
            )
            gl.auth()
        typer.secho(f"✔ Authenticated to {cfg.gitlab_url}", fg="green")
        return gl

    except gitlab.exceptions.GitlabAuthenticationError as e:
        typer.echo(f"\nAuthentication failed: {e}", err=True)
        raise typer.Exit(code=1)

    except Exception as e:
        typer.echo(f"\nCould not connect to {cfg.gitlab_url}: {e}", err=True)
        raise typer.Exit(code=1)

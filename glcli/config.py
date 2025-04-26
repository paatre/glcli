import os
import sys
from typing import Any, Dict, Optional

# Use tomllib for Python 3.11+, otherwise use tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_CONFIG_DIR = os.path.expanduser("~/.config/glcli")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.toml")

CONFIG_FILE = os.getenv("GLCLI_CONFIG_FILE", DEFAULT_CONFIG_FILE)


def _load_toml_settings() -> Dict[str, Any]:
    """
    Read [settings] from the TOML file if it exists; otherwise return empty dict.
    """
    try:
        with open(CONFIG_FILE, "rb") as f:
            data = tomllib.load(f)
            return data.get("settings", {})
    except (FileNotFoundError, OSError):
        return {}
    except tomllib.TOMLDecodeError as e:
        raise RuntimeError(f"Error parsing TOML config {DEFAULT_CONFIG_FILE}: {e}")


def _toml_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    return _load_toml_settings()


class Settings(BaseSettings):
    gitlab_url: str = "https://gitlab.com"
    private_access_token: Optional[str] = None

    model_config = SettingsConfigDict(
        env_prefix="GLCLI_",
        settings_customise_sources=(
            lambda settings_cls, init_kwargs, env, _dotenv, _secrets: (
                init_kwargs,
                env,
                _toml_settings_source,
            ),
        ),
    )


settings = Settings()


def get_gitlab_url(cli_url: Optional[str]) -> str:
    url = cli_url or settings.gitlab_url
    if not url:
        raise RuntimeError(
            "No GitLab URL configured. Please supply `--url`, set GLCLI_GITLAB_URL, "
            "or add `gitlab_url = …` under [settings] in your config.toml."
        )
    return url


def get_private_token(cli_token: Optional[str]) -> str:
    token = cli_token or settings.private_access_token
    if not token:
        raise RuntimeError(
            "No GitLab Personal Access Token configured. Please supply --token, "
            "set GLCLI_PRIVATE_ACCESS_TOKEN, or add `private_access_token = …` "
            "under [settings] in your config.toml."
        )
    return token

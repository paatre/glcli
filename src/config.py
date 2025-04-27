import os
import sys
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class Config:
    """
    Holds GitLab connection settings.

    Attributes:
        gitlab_url: The base URL of your GitLab instance (required).
        private_access_token: A valid PAT with API scope (required).
    """

    DEFAULT_CONFIG_FILE = Path.home() / ".config" / "glcli" / "config.toml"
    ENV_CONFIG_FILE = "GLCLI_CONFIG_FILE"
    ENV_URL = "GLCLI_GITLAB_URL"
    ENV_TOKEN = "GLCLI_PRIVATE_ACCESS_TOKEN"

    def __init__(self, gitlab_url: str, private_access_token: str):
        self.gitlab_url = gitlab_url
        self.private_access_token = private_access_token

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """
        Load settings, in this order:
          1. File path: `config_path` → $GLCLI_CONFIG_FILE → DEFAULT_CONFIG_FILE
          2. TOML `[settings]` section
          3. Env vars GLCLI_GITLAB_URL and GLCLI_PRIVATE_ACCESS_TOKEN
          4. Error if either `gitlab_url` or `private_access_token` is missing
        """
        # 1) pick file
        path = (
            Path(config_path)
            if config_path
            else Path(os.getenv(cls.ENV_CONFIG_FILE, cls.DEFAULT_CONFIG_FILE))
        )

        # 2) read TOML
        data = {}
        if path.is_file():
            try:
                with path.open("rb") as f:
                    raw = tomllib.load(f)
                data = raw.get("settings", {})
            except tomllib.TOMLDecodeError as e:
                raise RuntimeError(f"Could not parse TOML at {path}: {e}")

        url = data.get("gitlab_url", "")
        token = data.get("private_access_token", "")

        # 3) override from env
        url = os.getenv(cls.ENV_URL, url).strip()
        token = os.getenv(cls.ENV_TOKEN, token).strip()

        # 4) validate url
        if not url:
            raise RuntimeError(
                "Missing GitLab instance URL. "
                "Please set it in the config file or export "
                f"${cls.ENV_URL}."
            )

        # 5) validate token
        if not token:
            raise RuntimeError(
                "Missing GitLab Personal Access Token. "
                "Please set it in the config file or export "
                f"${cls.ENV_TOKEN}."
            )

        return cls(gitlab_url=url, private_access_token=token)

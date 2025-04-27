# GLCLI - GitLab Command Line Interface

An interactive command-line tool, built with Typer and powered by `python-gitlab`, for interacting with GitLab via its REST API. Uses `fzf` for interactive selection.

## Usage

GLCLI is designed to be run from the command line with [uv](https://docs.astral.sh/uv/).

After installing uv, you just need to do the following:

1. Clone this repository: `git clone https://github.com/paatre/glcli.git`
2. Change into the directory: `cd glcli`
3. Run the command: `uv run glcli.py`

With `uv run glcli`, uv will automatically create a virtual environment for you, install all the dependencies, and run the application using that virtual environment. No need to manually create and activate a virtual environment with `python -m venv` (note that uv will create a `.venv` directory in the current working directory). Dependencies are also locked to a `uv.lock` file. `uv run glcli` uses an executable script defined in the `pyproject.toml` file to run the application.

After running the command, you can interact with the GitLab API interactively.

## Configuration

GLCLI requires a GitLab instance URL and a personal access token (PAT) with the necessary permissions to interact with the API.

You can set these in the `~/.config/cglcli/config.toml` file. Check the `config.toml.template` for the required format.

You can create the `~/.config/cglcli/config.toml` file by copying the template with

```bash
cp config.toml.template ~/.config/glcli/config.toml
```

If you want to use a different configuration file path, you can give your own path by

- passing `--config`/`-c` option to the `glcli` command OR
- setting `GLCLI_CONFIG_FILE` environment variable

## Features

COMING SOON

import os
import shlex
import tempfile
from shutil import which

FZF_CMD = "fzf"
FZF_URL = "https://github.com/junegunn/fzf"
DEFAULT_HEIGHT = "20%"
DEFAULT_LAYOUT = "reverse"


def prompt(
    choices: list[str],
    header: str = "",
    fzf_options: str = "",
    delimiter: str = "\n",
    executable_path: str = FZF_CMD,
) -> list[str]:
    """
    Show an fzf menu over `choices` and return selected entries.

    Writes `choices` to a temp file, then does:
        fzf ... < input_file > output_file

    so that fzf’s UI stays attached to the real terminal (tty).

    Returns an empty list if the user cancels or makes no selection.
    """
    if which(executable_path) is None:
        raise SystemError(
            f"Cannot find '{executable_path}' in PATH. Install from {FZF_URL}"
        )

    if not choices:
        raise ValueError("`choices` must be a non‐empty list")

    in_fd, in_path = tempfile.mkstemp(text=True)
    out_fd, out_path = tempfile.mkstemp(text=True)
    with os.fdopen(in_fd, "w", encoding="utf-8") as f:
        f.write(delimiter.join(choices))

    cmd = []
    cmd.append(shlex.quote(executable_path))
    cmd.append(f"--header={shlex.quote(header)}")
    cmd.append(f"--height={shlex.quote(DEFAULT_HEIGHT)}")
    cmd.append(f"--layout={shlex.quote(DEFAULT_LAYOUT)}")
    if fzf_options:
        cmd.extend(shlex.split(fzf_options))

    full = " ".join(cmd) + f" < {shlex.quote(in_path)} > {shlex.quote(out_path)}"
    ret = os.system(full)

    result: list[str] = []
    if ret == 0:
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if line:
                    result.append(line)

    os.unlink(in_path)
    os.unlink(out_path)

    return result

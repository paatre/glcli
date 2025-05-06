from gitlab import Gitlab
from .explorer import explore


def run(gl: Gitlab) -> None:
    explore(gl, "GitLab")

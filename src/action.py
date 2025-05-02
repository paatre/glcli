from typing import Protocol, ClassVar


class CliAction(Protocol):
    """Anything the CLI can do when selected from the menu."""

    name: ClassVar[str]

    def interactive(self) -> None: ...

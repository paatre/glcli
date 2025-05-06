import inspect
import typer
from typing import Any
from gitlab.base import RESTManager
from gitlab import Gitlab
from yaspin import yaspin
from . import handlers
from .adapter import RESTAdapter
from .fzf import prompt
from .utils import humanize, split_camel_case


def explore(node: Any, label: str) -> None:
    """
    Recursively explore either:
      - a Gitlab client (lists its top‐level managers),
      - a RESTManager (shows its CRUD/mixin actions + ‘Browse items…’),
      - or a RESTObject (lists its sub‐managers).
    You can drill in (‘manager’→‘objects’→‘sub-managers’→…) or run any action at any level.
    """
    while True:
        choices: list[str] = []
        index: dict[str, tuple[str, Any]] = {}

        # 1) If you're at the very top (node is Gitlab) or at an object, list its sub‐managers:
        if isinstance(node, Gitlab) or not isinstance(node, RESTManager):
            for attr, val in inspect.getmembers(node, lambda o: isinstance(o, RESTManager)):
                key = humanize(attr)
                choices.append(key)
                index[key] = ("mgr", val)

        # 2) If node is a RESTManager, show its mixin actions:
        if isinstance(node, RESTManager):
            adapter = RESTAdapter(label, node)
            for action_label, method in adapter.build_actions(node):
                choices.append(action_label)
                index[action_label] = ("action", method)
            # And always let them “Browse items” if it has list() so that user can select an item
            if hasattr(node, "list"):
                key = "Browse items"
                choices.append(key)
                index[key] = ("browse", None)

        # 3) Navigation controls
        if label != "GitLab":
            back = "← Back"
            choices.append(back)
            index[back] = ("back", None)
        else:
            quit_ = "Quit"
            choices.append(quit_)
            index[quit_] = ("quit", None)

        # 4) Prompt
        sel = prompt(choices, header=f"{label}>")
        if not sel:
            return
        choice = sel[0]
        typer.echo(f"Selected: {choice}")
        kind, payload = index[choice]

        if kind == "quit":
            typer.echo("👋  Goodbye!")
            raise typer.Exit()
        if kind == "back":
            return

        # 5) Drill into a manager attribute
        if kind == "mgr":
            explore(payload, label=choice)  # payload is a RESTManager
            continue

        # 6) Browse items off a RESTManager
        if kind == "browse":
            mgr: RESTManager = node
            with yaspin(text="Loading items", color="cyan") as spinner:
                try:
                    items = mgr.list(get_all=True)
                    spinner.ok("✔")
                except Exception as e:
                    spinner.fail("✘")
                    typer.echo(f"Error fetching items: {e}", err=True)
                    raise typer.Exit(code=1)
            labels = [
                f"{getattr(o, 'id', '')}\t{getattr(o, 'name', getattr(o, 'title', ''))}"
                for o in items
            ]
            pick = prompt(labels, header=f"Select a {label[:-1]}")
            if not pick:
                continue
            obj = items[labels.index(pick[0])]
            typer.echo(f"Selected: {getattr(obj, 'name', getattr(obj, 'title', ''))}")
            explore(obj, label=f"{label}:{getattr(obj, 'id', '')}")
            continue

        # 7) Invoke a CRUD/mixin action on the manager
        if kind == "action":
            fn_name = payload
            fn = getattr(node, fn_name)
            handler = getattr(handlers, f"handle_{fn_name}", handlers.handle_fallback)
            handler(fn)
            continue

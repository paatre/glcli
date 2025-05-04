import inspect
import typer
from gitlab.base import RESTManager
from yaspin import yaspin
from .adapter import RESTAdapter
from .adapters import get_adapters_for
from .fzf import prompt
from .utils import split_camel_case


def run(gl: typer.Context) -> None:
    top_level_adapters = get_adapters_for(gl)

    while True:
        # 1) Pick your top‐level resource
        choices = list(top_level_adapters.keys()) + ["quit"]
        selection = prompt(choices, header="Choose a resource")
        if not selection:
            typer.echo("No choice, exiting.")
            raise typer.Exit()
        choice = selection[0]
        if choice == "quit":
            typer.echo("👋  Goodbye!")
            raise typer.Exit()

        adapter = top_level_adapters[choice]
        mgr = adapter._mgr

        # 2) If it supports .list(), let the user pick one object
        if hasattr(mgr, "list"):
            with yaspin(text="Loading items", color="cyan") as spinner:
                try:
                    items = mgr.list(membership=True, get_all=True, order_by='last_activity_at', sort='desc')
                    spinner.ok("✔")
                except Exception as e:
                    spinner.fail("✘")
                    typer.echo(f"Error fetching items: {e}", err=True)
                    raise typer.Exit(code=1)
            labels = []
            for o in items:
                desc = getattr(o, "name", getattr(o, "title", ""))
                labels.append(f"{getattr(o, 'id', '')}\t{desc}")

            sel2 = prompt(labels, header=f"Choose a {choice[:-1]}")
            if not sel2:
                continue

            picked = items[labels.index(sel2[0])]

            # 3) discover all sub‐managers on that one object
            subs: dict[str, RESTManager] = {}
            for attr, obj in inspect.getmembers(
                picked, lambda o: isinstance(o, RESTManager)
            ):
                subs[split_camel_case(attr)] = obj

            if not subs:
                # nothing to drill into—just drop back to the normal CRUD menu
                adapter.interactive()
                continue

            # 4) let them pick which sub‐manager to drive next
            sub_choices = list(subs.keys()) + ["← Back"]
            sel3 = prompt(sub_choices, header=f"{choice[:-1]} {picked.id}: choose action")
            if not sel3 or sel3[0] == "← Back":
                continue

            sub_mgr = subs[sel3[0]]
            RESTAdapter(sel3[0], sub_mgr).interactive()

        else:
            # no .list(): just fall back to single‐manager interactive
            adapter.interactive()

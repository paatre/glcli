import inspect
import typer
import json
from .fzf import prompt


def handle_list(fn):
    list_results = fn(get_all=True)
    items, labels = [], []
    for obj in list_results:
        items.append(obj)
        labels.append(
            f"{getattr(obj, 'id', '')}\t{getattr(obj, 'name', getattr(obj, 'title', ''))}"
        )
    sel = prompt(labels)
    if not sel:
        return
    picked = items[labels.index(sel[0])]
    typer.echo(picked.attributes)


def handle_get(fn):
    sig = inspect.signature(fn)
    if "id" in sig.parameters:
        obj = fn(typer.prompt("Enter ID"))
    else:
        obj = fn()
    typer.echo(obj.attributes)


def handle_create(fn):
    raw = typer.prompt("Enter data for create (as JSON)")
    data = json.loads(raw)
    typer.echo(fn(data))


def handle_update(fn):
    raw = typer.prompt("Enter data for update (as JSON)")
    data = json.loads(raw)
    typer.echo(fn(data))


def handle_refresh(fn):
    fn()
    typer.secho("Refreshed.", fg="green")


def handle_delete(fn):
    fn(typer.prompt("Enter ID to delete"))
    typer.secho("Deleted.", fg="green")


def handle_save(fn):
    fn()
    typer.secho("Saved changes.", fg="green")


def handle_set(fn):
    key = typer.prompt("Enter key")
    value = typer.prompt("Enter value")
    typer.echo(fn(key, value))


def handle_approve(fn):
    fn(int(typer.prompt("Enter access level", default="30")))
    typer.secho("Approved.", fg="green")


def handle_download(fn):
    typer.echo_bytes(fn(streamed=False))


def handle_subscribe(fn):
    fn()
    typer.secho("Subscribe done.", fg="green")


def handle_unsubscribe(fn):
    fn()
    typer.secho("Unsubscribe done.", fg="green")


def handle_todo(fn):
    fn()
    typer.secho("Todo done.", fg="green")


def handle_time_stats(fn):
    # all the time_* methods can reuse the same pattern
    params = inspect.signature(fn).parameters
    kwargs = {n: typer.prompt(n) for n in params if n != "self"}
    res = fn(**kwargs)
    if res is not None:
        typer.echo(res)


def handle_participants(fn):
    parts = fn()
    typer.echo(f"{len(parts)} participants")


def handle_render(fn):
    link = typer.prompt("Enter link_url")
    img = typer.prompt("Enter image_url")
    typer.echo(fn(link, img))


def handle_fallback(fn):
    sig = inspect.signature(fn)
    kwargs = {}
    for name, param in sig.parameters.items():
        if param.default is inspect._empty:
            kwargs[name] = typer.prompt(name)
        else:
            kwargs[name] = typer.prompt(name, default=str(param.default))
    typer.echo(fn(**kwargs))

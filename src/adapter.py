import inspect
import gitlab
import typer
from gitlab.base import RESTManager
from typing import ClassVar
from . import handlers
from .action import CliAction
from .fzf import prompt

# For each RESTManager mixin, list the (menu label, method name) pairs it brings in
_MIXIN_ACTIONS: dict[str, list[tuple[str, str]]] = {
    "ListMixin": [("List all items", "list")],
    "GetMixin": [("Get by ID", "get")],
    "GetWithoutIdMixin": [("Get single object", "get")],
    "RefreshMixin": [("Refresh resource", "refresh")],
    "RetrieveMixin": [],  # Composite of List+Get; skip here
    "CreateMixin": [("Create new item", "create")],
    "UpdateMixin": [("Update existing", "update")],
    "SetMixin": [("Set attribute", "set")],
    "DeleteMixin": [("Delete item", "delete")],
    "CRUDMixin": [],  # Composite
    "NoUpdateMixin": [],  # Composite
    "SaveMixin": [("Save changes", "save")],
    "ObjectDeleteMixin": [("Delete object", "delete")],
    "UserAgentDetailMixin": [("User agent detail", "user_agent_detail")],
    "AccessRequestMixin": [("Approve access req.", "approve")],
    "DownloadMixin": [("Download resource", "download")],
    "SubscribableMixin": [("Subscribe", "subscribe"), ("Unsubscribe", "unsubscribe")],
    "TodoMixin": [("Create todo", "todo")],
    "TimeTrackingMixin": [
        ("Get time stats", "time_stats"),
        ("Set time estimate", "time_estimate"),
        ("Reset time estimate", "reset_time_estimate"),
        ("Add spent time", "add_spent_time"),
        ("Reset spent time", "reset_spent_time"),
    ],
    "ParticipantsMixin": [("List participants", "participants")],
    "BadgeRenderMixin": [("Render badge", "render")],
}


class RESTAdapter(CliAction):
    """
    Adapter for any gitlab.base.RESTManager,
    exposing only the methods the manager actually supports.
    """

    name: ClassVar[str]

    def __init__(self, manager_name: str, gl: gitlab.Gitlab):
        self.name = manager_name
        self._gl = gl

    def build_actions(self, mgr: RESTManager) -> list[tuple[str, str | None]]:
        """
        Builds a list of available actions for the given manager.
        """
        actions: list[tuple[str, str | None]] = []
        mro = [cls.__name__ for cls in inspect.getmro(type(mgr))]

        for mixin_name, entries in _MIXIN_ACTIONS.items():
            if mixin_name in mro:
                for label, method_name in entries:
                    if hasattr(mgr, method_name):
                        actions.append((label, method_name))

        return actions

    def get_method_for_label(
        self, selected: str, actions: list[tuple[str, str | None]]
    ) -> str | None:
        """
        Get the method name for the selected label.
        """
        return next((method for label, method in actions if label == selected), None)

    def interactive(self) -> None:
        """
        Show the interactive menu for this RESTManager.
        """
        # Build the list of available actions
        mgr = getattr(self._gl, self.name)
        actions = self.build_actions(mgr)
        actions.append(("← Back to main menu", None))

        # Prompt
        labels = [label for label, _ in actions]
        choice = prompt(labels)
        if not choice:
            typer.echo("No selection, returning…")
            return
        selected = choice[0]

        # Find and call the method
        method = self.get_method_for_label(selected, actions)
        if method is None:
            return
        fn = getattr(mgr, method)
        handler_name = f"handle_{method}"
        handler = getattr(handlers, handler_name, handlers.handle_fallback)
        handler(fn)

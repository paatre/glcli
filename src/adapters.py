import inspect
import re
from gitlab.base import RESTManager
from gitlab.v4 import objects
from .adapter import RESTAdapter
from .utils import humanize


def get_adapters_for(gl) -> dict[str, RESTAdapter]:
    """
    Wrap every top-level RESTManager on `gl` in a RESTAdapter.
    """
    adapters: dict[str, RESTAdapter] = {}

    for name, mgr in inspect.getmembers(gl, lambda o: isinstance(o, RESTManager)):
        label = humanize(name)
        adapters[label] = RESTAdapter(label, mgr)

    return adapters


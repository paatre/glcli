import inspect
import gitlab
from .adapter import RESTAdapter


def get_adapters_for(gl: gitlab.Gitlab) -> dict[str, RESTAdapter]:
    """
    Discover every gitlab.base.RESTManager on the `gl` client
    and wrap it in our RESTAdapter.

    Returns a dictionary mapping manager names to their respective adapters.
    """
    managers = inspect.getmembers(gl, lambda o: isinstance(o, gitlab.base.RESTManager))
    return {name: RESTAdapter(name, gl) for name, _ in managers}

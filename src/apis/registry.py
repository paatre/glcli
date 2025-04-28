from typing import Optional
from .base import GitlabAPI


class ApiRegistry:
    """
    Registry for GitLab API classes to be used in the CLI when dispatching.
    """

    _registry: dict[str, type[GitlabAPI]] = {}

    @classmethod
    def register(cls):
        """
        Decorator to register a GitlabAPI class in the registry.
        """

        def decorator(api_cls: type[GitlabAPI]):
            key = api_cls.name.lower()
            cls._registry[key] = api_cls
            return api_cls

        return decorator

    @classmethod
    def get_apis(cls) -> dict[str, type[GitlabAPI]]:
        """
        Get all registered API classes.
        """
        return cls._registry

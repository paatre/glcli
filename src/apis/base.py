from typing import Protocol, ClassVar
from gitlab import Gitlab


class GitlabAPI(Protocol):
    """
    Base class for GitLab API classes.

    This class defines the interface for all GitLab API classes so that they can be used in a standardized way during dispatching.

    Attributes:
        name (str): The name of the API class. This should be unique and descriptive. Used for fetching the class from the registry during dispatching.
    Methods:
        interactive(gl: Gitlab) -> None:
            This method should be implemented by subclasses to provide an interactive interface for the API. This method will be called when a user selects an API and the dispatcher finds this API by name attribute.
    """

    name: ClassVar[str]

    def interactive(self, gl: Gitlab) -> None: ...

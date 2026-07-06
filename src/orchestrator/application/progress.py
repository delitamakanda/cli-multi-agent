from typing import Protocol


class ProgressReporter(Protocol):
    """Reports audit progress to whatever is observing (CLI, tests, ...)."""

    def stage(self, message: str) -> None: ...

    def agents_planned(self, total: int) -> None: ...

    def agent_done(self, name: str, success: bool) -> None: ...


class NullProgressReporter:
    """No-op reporter used when the caller doesn't care about progress."""

    def stage(self, message: str) -> None:
        pass

    def agents_planned(self, total: int) -> None:
        pass

    def agent_done(self, name: str, success: bool) -> None:
        pass

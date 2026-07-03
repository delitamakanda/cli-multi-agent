from __future__ import annotations

import base64
import os
import shutil
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse


class RepositorySourceError(RuntimeError):
    """Raised when a repository source cannot be resolved."""


class RepositorySourceResolver:
    """Resolve a local directory or a remote Git URL to a local repository path."""

    def __init__(self, git_executable: str = "git") -> None:
        self.git_executable = git_executable

    @contextmanager
    def resolve(
        self,
        source: str | Path,
        *,
        ref: str | None = None,
        depth: int | None = 1,
        token: str | None = None,
    ) -> Iterator[Path]:
        source_value = str(source).strip()
        if not source_value:
            raise RepositorySourceError("Repository source cannot be empty.")

        if not self._is_remote(source_value):
            path = Path(source_value).expanduser().resolve()
            if not path.exists():
                raise RepositorySourceError(f"Repository path does not exist: {path}")
            if not path.is_dir():
                raise RepositorySourceError(f"Repository source is not a directory: {path}")
            yield path
            return

        if shutil.which(self.git_executable) is None:
            raise RepositorySourceError(
                f"Git executable '{self.git_executable}' was not found in PATH."
            )

        with TemporaryDirectory(prefix="repo-audit-") as temporary_directory:
            destination = Path(temporary_directory) / self._repository_name(source_value)
            command = [self.git_executable, "clone", "--quiet"]

            if depth is not None:
                if depth < 1:
                    raise RepositorySourceError("Clone depth must be greater than zero.")
                command.extend(["--depth", str(depth)])

            if ref:
                command.extend(["--branch", ref, "--single-branch"])

            command.extend([source_value, str(destination)])
            environment = self._build_git_environment(source_value, token)

            try:
                subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True,
                    env=environment,
                )
            except subprocess.CalledProcessError as error:
                detail = (error.stderr or error.stdout or "Unknown Git error").strip()
                raise RepositorySourceError(
                    f"Unable to clone repository '{self._redact(source_value)}': {detail}"
                ) from error

            yield destination

    @staticmethod
    def _is_remote(source: str) -> bool:
        parsed = urlparse(source)
        return parsed.scheme in {"http", "https", "ssh", "git"} or source.startswith("git@")

    @staticmethod
    def _repository_name(source: str) -> str:
        path = urlparse(source).path if "://" in source else source.split(":", 1)[-1]
        name = Path(path.rstrip("/")).name
        return name.removesuffix(".git") or "repository"

    @staticmethod
    def _build_git_environment(source: str, token: str | None) -> dict[str, str]:
        environment = os.environ.copy()
        environment["GIT_TERMINAL_PROMPT"] = "0"

        if not token or not source.startswith(("http://", "https://")):
            return environment

        hostname = (urlparse(source).hostname or "").lower()
        username = "oauth2" if "gitlab" in hostname else "x-access-token"
        credentials = base64.b64encode(f"{username}:{token}".encode()).decode()

        environment["GIT_CONFIG_COUNT"] = "1"
        environment["GIT_CONFIG_KEY_0"] = "http.extraHeader"
        environment["GIT_CONFIG_VALUE_0"] = f"Authorization: Basic {credentials}"
        return environment

    @staticmethod
    def _redact(source: str) -> str:
        parsed = urlparse(source)
        if not parsed.username and not parsed.password:
            return source

        hostname = parsed.hostname or ""
        if parsed.port:
            hostname = f"{hostname}:{parsed.port}"
        return parsed._replace(netloc=hostname).geturl()

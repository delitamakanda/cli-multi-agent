from __future__ import annotations

import base64
import os
import re
import shutil
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

# Matches Git's scp-like syntax, [user@]host:path (e.g. "git@host:org/repo.git" or
# "alice@gerrit.example.com:/project.git"), which has no scheme and no slash before the
# colon. A bare single-character host (no "user@") is excluded so Windows drive paths
# like "C:\repo" aren't misdetected as remote.
_SCP_LIKE_SOURCE_PATTERN = re.compile(r"^(?:[\w.\-]+@[\w.\-]+|[\w.\-]{2,}):(?!//)")


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

            if ref:
                if shutil.which(self.git_executable) is None:
                    raise RepositorySourceError(
                        f"Git executable '{self.git_executable}' was not found in PATH."
                    )
                with self._local_worktree(path, ref) as worktree_path:
                    yield worktree_path
                return

            yield path
            return

        if shutil.which(self.git_executable) is None:
            raise RepositorySourceError(
                f"Git executable '{self.git_executable}' was not found in PATH."
            )

        if depth is not None and depth < 1:
            raise RepositorySourceError("Clone depth must be greater than zero.")

        with TemporaryDirectory(prefix="repo-audit-") as temporary_directory:
            destination = Path(temporary_directory) / self._repository_name(source_value)
            environment = self._build_git_environment(source_value, token)

            if ref:
                self._fetch_ref(source_value, destination, ref, depth, environment)
            else:
                self._clone(source_value, destination, depth, environment)

            yield destination

    def _clone(
        self,
        source: str,
        destination: Path,
        depth: int | None,
        environment: dict[str, str],
    ) -> None:
        command = [self.git_executable, "clone", "--quiet"]
        if depth is not None:
            command.extend(["--depth", str(depth)])
        command.extend([source, str(destination)])
        self._run(command, source, environment, action="clone repository")

    def _fetch_ref(
        self,
        source: str,
        destination: Path,
        ref: str,
        depth: int | None,
        environment: dict[str, str],
    ) -> None:
        # `ref` may be a branch, tag, or commit SHA. `git clone --branch` only accepts
        # branch/tag names, so resolve arbitrary refs via init + fetch + checkout instead.
        self._run(
            [self.git_executable, "init", "--quiet", str(destination)],
            source,
            environment,
            action="initialize repository",
        )
        self._run(
            [self.git_executable, "-C", str(destination), "remote", "add", "origin", source],
            source,
            environment,
            action="configure remote for",
        )

        fetch_command = [self.git_executable, "-C", str(destination), "fetch", "--quiet"]
        if depth is not None:
            fetch_command.extend(["--depth", str(depth)])
        fetch_command.extend(["origin", ref])
        self._run(fetch_command, source, environment, action="fetch ref from")

        self._run(
            [self.git_executable, "-C", str(destination), "checkout", "--quiet", "FETCH_HEAD"],
            source,
            environment,
            action="checkout ref from",
        )

    def _run(
        self,
        command: list[str],
        source: str,
        environment: dict[str, str],
        *,
        action: str,
    ) -> None:
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
                f"Unable to {action} '{self._redact(source)}': {detail}"
            ) from error

    @contextmanager
    def _local_worktree(self, repository: Path, ref: str) -> Iterator[Path]:
        # Check out `ref` into a disposable worktree instead of scanning the caller's
        # current checkout, which may be on a different branch/commit than requested.
        with TemporaryDirectory(prefix="repo-audit-worktree-") as temporary_directory:
            worktree_path = Path(temporary_directory) / "worktree"
            environment = os.environ.copy()
            environment["GIT_TERMINAL_PROMPT"] = "0"

            self._run(
                [
                    self.git_executable,
                    "-C",
                    str(repository),
                    "worktree",
                    "add",
                    "--quiet",
                    "--detach",
                    str(worktree_path),
                    ref,
                ],
                str(repository),
                environment,
                action="check out ref in",
            )
            try:
                yield worktree_path
            finally:
                subprocess.run(
                    [
                        self.git_executable,
                        "-C",
                        str(repository),
                        "worktree",
                        "remove",
                        "--force",
                        str(worktree_path),
                    ],
                    capture_output=True,
                    text=True,
                    env=environment,
                )

    @staticmethod
    def _is_remote(source: str) -> bool:
        parsed = urlparse(source)
        if parsed.scheme in {"http", "https", "ssh", "git", "file"}:
            return True
        return bool(_SCP_LIKE_SOURCE_PATTERN.match(source))

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

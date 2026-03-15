"""Load .env.example into os.environ so tests can run without a real .env."""

from pathlib import Path

import pytest


def _load_env_example() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env.example"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key and key not in __import__("os").environ:
            __import__("os").environ[key] = value.strip()


_load_env_example()


@pytest.fixture(scope="session")
def _env_loaded() -> None:
    """Ensure env is loaded for the session."""
    pass

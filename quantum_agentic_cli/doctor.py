from __future__ import annotations

from pathlib import Path


def detect_repository_state() -> dict[str, object]:
    repo_root = Path(".")
    files = sorted(str(path) for path in repo_root.rglob("*") if path.is_file())
    return {
        "root": str(repo_root.resolve()),
        "files": files[:50],
        "count": len(files),
    }


def show_doctor() -> dict[str, object]:
    return {
        "python_ok": True,
        "numpy_ok": True,
        "provider_env": {"OPENAI_API_KEY": "configured" if __import__("os").getenv("OPENAI_API_KEY") else "missing", "OPENROUTER_API_KEY": "configured" if __import__("os").getenv("OPENROUTER_API_KEY") else "missing"},
        "simulator_backend": "available",
        "mock_backend": "available",
    }

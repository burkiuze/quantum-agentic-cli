from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, data_dir: str | Path = ".quantum-agent") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.conversation_path = self.data_dir / "conversation.json"
        self.checkpoints_path = self.data_dir / "checkpoints.json"
        self.experiments_path = self.data_dir / "experiments.json"
        self.history: list[dict[str, Any]] = self._load(self.conversation_path, default=[])
        self.checkpoints: dict[str, Any] = self._load(self.checkpoints_path, default={})
        self.experiments: list[dict[str, Any]] = self._load(self.experiments_path, default=[])

    @staticmethod
    def _load(path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            return default

    def save(self) -> None:
        with self.conversation_path.open("w", encoding="utf-8") as handle:
            json.dump(self.history, handle, indent=2)
        with self.checkpoints_path.open("w", encoding="utf-8") as handle:
            json.dump(self.checkpoints, handle, indent=2)
        with self.experiments_path.open("w", encoding="utf-8") as handle:
            json.dump(self.experiments, handle, indent=2)

    def append_message(self, role: str, content: str, **extra: Any) -> None:
        self.history.append({"role": role, "content": content, **extra})
        self.save()

    def add_checkpoint(self, task_id: str, state: dict[str, Any]) -> None:
        self.checkpoints[task_id] = state
        self.save()

    def add_experiment(self, record: dict[str, Any]) -> None:
        self.experiments.append(record)
        self.save()

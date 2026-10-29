from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    ok: bool
    value: Any = None
    error: str | None = None


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, Any] = {}

    def register(self, tool: Any) -> None:
        self.tools[tool.name] = tool

    def call(self, name: str, **kwargs: Any) -> ToolResult:
        tool = self.tools.get(name)
        if tool is None:
            return ToolResult(ok=False, error=f"Tool '{name}' is not registered.")
        try:
            value = tool.handler(**kwargs)
            return ToolResult(ok=True, value=value)
        except Exception as exc:  # pragma: no cover - safety boundary
            return ToolResult(ok=False, error=str(exc))

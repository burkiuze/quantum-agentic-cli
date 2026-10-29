from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any


@dataclass
class SecurityPolicy:
    allow_local_files: bool = True
    allow_read_only: bool = True
    allow_write: bool = False
    allow_process_exec: bool = False
    allow_network: bool = False
    approval_required_for_destruction: bool = True
    disallow_shell_patterns: tuple[str, ...] = ("rm -rf", "curl", "wget", "sudo ")


class SecretRedactor:
    def __init__(self) -> None:
        self.patterns = [
            re.compile(r"sk-[A-Za-z0-9]+"),
            re.compile(r"OPENAI_API_KEY=[^\s]+"),
            re.compile(r"OPENROUTER_API_KEY=[^\s]+"),
        ]

    def redact(self, text: str) -> str:
        for pattern in self.patterns:
            text = pattern.sub("[REDACTED]", text)
        return text


def sanitize_tool_input(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return {str(k): sanitize_tool_input(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_tool_input(v) for v in value]
    return value


def require_approval(policy: SecurityPolicy, action: str) -> bool:
    if not action:
        return True
    if policy.approval_required_for_destruction and any(token in action.lower() for token in ("delete", "rm ", "overwrite")):
        return True
    return False


def check_env_secret(name: str) -> str | None:
    value = os.getenv(name)
    if value and value.strip():
        return value
    return None

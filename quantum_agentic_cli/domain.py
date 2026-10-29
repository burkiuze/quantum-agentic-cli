from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Optional


@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Any]
    requires_approval: bool = False
    timeout_seconds: float = 30.0


@dataclass
class QuantumExecutionRecord:
    backend: str
    qubits: int
    shots: int
    depth: int
    result: dict[str, Any]
    elapsed_seconds: float


@dataclass
class AgentTuple:
    Q: Any
    C: Any
    M: Any
    P: Any
    A: Any


@dataclass
class RuntimeContext:
    user_prompt: str
    conversation_id: str = "default"
    facts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentConfig:
    default_provider: str = "mock"
    default_model: str = "mock-model"
    backend: str = "mock"
    max_iterations: int = 10
    max_tool_calls: int = 12
    max_shots: int = 1024
    allow_external_actions: bool = False
    approval_mode: str = "interactive"


@dataclass
class BenchmarkResult:
    name: str
    score: float
    detail: dict[str, Any]

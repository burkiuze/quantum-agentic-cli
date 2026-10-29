from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProviderConfig:
    name: str
    model_id: str = "mock-model"
    api_key: str | None = None
    base_url: str | None = None
    timeout_seconds: float = 30.0
    enabled: bool = True
    capabilities: dict[str, bool] = field(default_factory=dict)


@dataclass
class QuantumConfig:
    backend: str = "mock"
    shots: int = 256
    seed: int = 1234
    max_qubits: int = 20
    allow_remote: bool = False


@dataclass
class RuntimeSettings:
    data_dir: str = ".quantum-agent"
    log_level: str = "INFO"
    approval_mode: str = "interactive"
    max_iterations: int = 10
    max_tool_calls: int = 12
    max_shots: int = 1024
    default_provider: str = "mock"
    default_model: str = "mock-model"
    provider_configs: dict[str, ProviderConfig] = field(default_factory=dict)
    quantum: QuantumConfig = field(default_factory=lambda: QuantumConfig())

    @classmethod
    def from_env(cls) -> "RuntimeSettings":
        settings = cls(
            data_dir=os.getenv("QUANTUM_AGENT_DATA_DIR", ".quantum-agent"),
            log_level=os.getenv("QUANTUM_AGENT_LOG_LEVEL", "INFO"),
            approval_mode=os.getenv("QUANTUM_AGENT_APPROVAL_MODE", "interactive"),
            max_iterations=int(os.getenv("QUANTUM_AGENT_MAX_ITERATIONS", "10")),
            max_tool_calls=int(os.getenv("QUANTUM_AGENT_MAX_TOOL_CALLS", "12")),
            max_shots=int(os.getenv("QUANTUM_AGENT_MAX_SHOTS", "1024")),
            default_provider=os.getenv("DEFAULT_LLM_PROVIDER", "mock"),
            default_model=os.getenv("DEFAULT_MODEL_ID", "mock-model"),
        )
        settings.quantum.backend = os.getenv("QUANTUM_BACKEND", "mock")
        settings.quantum.seed = int(os.getenv("QUANTUM_SEED", "1234"))
        settings.quantum.shots = int(os.getenv("QUANTUM_AGENT_MAX_SHOTS", "256"))

        settings.provider_configs = {
            "mock": ProviderConfig(name="mock", model_id="mock-model", enabled=True, capabilities={"chat": True, "vision": False, "tools": True}),
            "openai": ProviderConfig(
                name="openai",
                model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini"),
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL"),
                timeout_seconds=30.0,
                capabilities={"chat": True, "vision": True, "tools": True},
            ),
            "openrouter": ProviderConfig(
                name="openrouter",
                model_id=os.getenv("OPENROUTER_MODEL_ID", "openai/gpt-4o-mini"),
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
                timeout_seconds=30.0,
                capabilities={"chat": True, "vision": False, "tools": True},
            ),
            "local": ProviderConfig(
                name="local",
                model_id=os.getenv("LOCAL_MODEL_ID", "local-model"),
                base_url=os.getenv("LOCAL_LLM_BASE_URL"),
                timeout_seconds=45.0,
                capabilities={"chat": True, "vision": False, "tools": False},
            ),
        }
        return settings

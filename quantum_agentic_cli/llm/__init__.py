from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable


class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def complete(self, prompt: str, *, system_prompt: str | None = None, model: str | None = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def supports(self, feature: str) -> bool:
        raise NotImplementedError


@dataclass
class ProviderResponse:
    content: str
    model: str
    provider: str
    metadata: dict[str, Any] = field(default_factory=dict)


class MockProvider(LLMProvider):
    name = "mock"

    def complete(self, prompt: str, *, system_prompt: str | None = None, model: str | None = None) -> str:
        return f"Mock provider response for: {prompt[:120]}"

    def supports(self, feature: str) -> bool:
        return feature in {"chat", "tools", "reasoning"}


class OpenAICompatibleProvider(LLMProvider):
    name = "openai-compatible"

    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout_seconds: float = 30.0) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds

    def complete(self, prompt: str, *, system_prompt: str | None = None, model: str | None = None) -> str:
        if not self.api_key:
            raise RuntimeError("OpenAI-compatible provider requires an API key in the environment.")
        return f"OpenAI-compatible request for model={model or 'default'}: {prompt[:160]}"

    def supports(self, feature: str) -> bool:
        return feature in {"chat", "tools", "reasoning"}


class OpenRouterProvider(OpenAICompatibleProvider):
    name = "openrouter"

    def complete(self, prompt: str, *, system_prompt: str | None = None, model: str | None = None) -> str:
        if not self.api_key:
            raise RuntimeError("OpenRouter requires OPENROUTER_API_KEY.")
        return f"OpenRouter request for model={model or 'default'}: {prompt[:160]}"


class LocalInferenceProvider(LLMProvider):
    name = "local"

    def __init__(self, base_url: str | None = None, timeout_seconds: float = 45.0) -> None:
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds

    def complete(self, prompt: str, *, system_prompt: str | None = None, model: str | None = None) -> str:
        if not self.base_url:
            raise RuntimeError("Local inference provider requires LOCAL_LLM_BASE_URL.")
        return f"Local provider request for model={model or 'default'}: {prompt[:160]}"

    def supports(self, feature: str) -> bool:
        return feature in {"chat", "reasoning"}


def build_provider(name: str, *, api_key: str | None = None, base_url: str | None = None, timeout_seconds: float = 30.0) -> LLMProvider:
    catalog: dict[str, type[LLMProvider]] = {
        "mock": MockProvider,
        "openai": OpenAICompatibleProvider,
        "openrouter": OpenRouterProvider,
        "local": LocalInferenceProvider,
    }
    provider_cls = catalog.get(name, MockProvider)
    return provider_cls(api_key=api_key, base_url=base_url, timeout_seconds=timeout_seconds)

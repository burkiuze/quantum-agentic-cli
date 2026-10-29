from __future__ import annotations

import json
import os
from typing import Any


class Observability:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def log(self, event_type: str, **payload: Any) -> None:
        self.events.append({"type": event_type, **payload})

    def export(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.events, handle, indent=2)


class AgentRuntime:
    def __init__(self, provider: Any, memory: Any, security_policy: Any, observability: Observability | None = None) -> None:
        self.provider = provider
        self.memory = memory
        self.security_policy = security_policy
        self.observability = observability or Observability()

    def plan(self, prompt: str) -> str:
        self.observability.log("plan", prompt=prompt)
        return "Plan: inspect context, select provider, validate tools, execute bounded action loop."

    def respond(self, prompt: str, *, context: dict[str, Any] | None = None) -> str:
        context = context or {}
        system_prompt = "You are a careful local-first quantum-agentic assistant. Keep state local and disclose uncertainty."
        response = self.provider.complete(prompt, system_prompt=system_prompt)
        self.memory.append_message("assistant", response, context=context)
        self.observability.log("response", prompt=prompt, response=response)
        return response

    def run(self, prompt: str) -> str:
        plan = self.plan(prompt)
        result = self.respond(prompt, context={"plan": plan})
        return f"{plan}\n\n{result}"

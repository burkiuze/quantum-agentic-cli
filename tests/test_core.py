from __future__ import annotations

import json


def test_tuple_contracts():
    from quantum_agentic_cli.domain import AgentTuple
    agent = AgentTuple(Q={"backend": "mock"}, C={"planner": "planner"}, M={"memory": []}, P={"input": "x"}, A={"actions": []})
    assert set(agent.__dict__.keys()) == {"Q", "C", "M", "P", "A"}


def test_provider_mock():
    from quantum_agentic_cli.llm import MockProvider
    provider = MockProvider()
    assert provider.supports("chat")
    assert "Mock provider" in provider.complete("hello")


def test_grover_selection():
    from quantum_agentic_cli.quantum.grover import GroverDecisionAgent
    from quantum_agentic_cli.quantum.backends import MockQuantumBackend
    agent = GroverDecisionAgent(["A", "B", "C", "D"])
    result = agent.evaluate(shots=32, backend=MockQuantumBackend(), marked=0)
    assert result.selected_action in {"A", "B", "C", "D"}
    assert result.probability >= 0.0


def test_bandit_runtime():
    from quantum_agentic_cli.quantum.bandit import EntropyBanditEnvironment, VariationalBanditAgent
    env = EntropyBanditEnvironment(arms=3, seed=7)
    agent = VariationalBanditAgent(3, seed=7)
    result = agent.evaluate(env, episodes=5)
    assert result["episodes"] == 5
    assert len(result["history"]) == 5


def test_image_policy():
    from quantum_agentic_cli.quantum.image_lab import AdaptiveImageTransformPolicy
    policy = AdaptiveImageTransformPolicy()
    transformed = policy.apply([0, 64, 128], "xor")
    assert transformed == [85, 117, 171]


def test_memory_store_roundtrip(tmp_path):
    from quantum_agentic_cli.memory import MemoryStore
    store = MemoryStore(tmp_path)
    store.append_message("user", "hello")
    assert len(store.history) == 1


def test_secret_redactor():
    from quantum_agentic_cli.security import SecretRedactor
    text = "OPENAI_API_KEY=abc123"
    redacted = SecretRedactor().redact(text)
    assert "abc123" not in redacted

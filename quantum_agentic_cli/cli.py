from __future__ import annotations

import argparse
import json
import os
from typing import Any

from quantum_agentic_cli.config import RuntimeSettings
from quantum_agentic_cli.domain import AgentConfig
from quantum_agentic_cli.doctor import show_doctor
from quantum_agentic_cli.llm import build_provider
from quantum_agentic_cli.memory import MemoryStore
from quantum_agentic_cli.quantum.backends import LocalSimulatorBackend, MockQuantumBackend, QuantumCircuitSpec
from quantum_agentic_cli.quantum.bandit import EntropyBanditEnvironment, VariationalBanditAgent
from quantum_agentic_cli.quantum.grover import GroverDecisionAgent
from quantum_agentic_cli.quantum.image_lab import AdaptiveImageTransformPolicy, ImageEntropyFeatureExtractor
from quantum_agentic_cli.runtime import AgentRuntime
from quantum_agentic_cli.security import SecretRedactor, SecurityPolicy


def _print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def cmd_chat(args: argparse.Namespace) -> None:
    settings = RuntimeSettings.from_env()
    provider = build_provider(settings.default_provider, api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"), timeout_seconds=30.0)
    memory = MemoryStore(settings.data_dir)
    runtime = AgentRuntime(provider=provider, memory=memory, security_policy=SecurityPolicy(), observability=None)
    print(runtime.run(args.prompt))


def cmd_run(args: argparse.Namespace) -> None:
    settings = RuntimeSettings.from_env()
    provider = build_provider(settings.default_provider)
    memory = MemoryStore(settings.data_dir)
    runtime = AgentRuntime(provider=provider, memory=memory, security_policy=SecurityPolicy())
    print(runtime.run(args.prompt))


def cmd_providers(args: argparse.Namespace) -> None:
    _print_json({
        "providers": [
            {"name": "mock", "features": ["chat", "tools", "reasoning"]},
            {"name": "openai", "requires_api_key": True},
            {"name": "openrouter", "requires_api_key": True},
            {"name": "local", "requires_base_url": True},
        ]
    })


def cmd_quantum_backends(args: argparse.Namespace) -> None:
    _print_json({
        "backends": [
            {"name": "mock", "supports_seeded_simulation": True, "max_qubits": 16},
            {"name": "simulator", "supports_seeded_simulation": True, "max_qubits": 20},
        ]
    })


def cmd_agent_grover(args: argparse.Namespace) -> None:
    actions = args.candidates.split(",") if args.candidates else ["A", "B", "C", "D"]
    agent = GroverDecisionAgent(actions)
    marked = args.mark if args.mark is not None else 0
    backend = MockQuantumBackend()
    result = agent.evaluate(shots=args.shots, backend=backend, marked=marked)
    _print_json({
        "selected_action": result.selected_action,
        "probability": result.probability,
        "counts": result.counts,
        "oracle_summary": result.oracle_summary,
        "qubits": result.qubits,
        "depth": result.depth,
    })


def cmd_agent_bandit(args: argparse.Namespace) -> None:
    env = EntropyBanditEnvironment(arms=args.arms, seed=args.seed)
    agent = VariationalBanditAgent(args.arms, seed=args.seed)
    result = agent.evaluate(env, episodes=args.episodes)
    _print_json(result)


def cmd_agent_image_lab(args: argparse.Namespace) -> None:
    policy = AdaptiveImageTransformPolicy()
    image_values = [0, 64, 128, 192, 255, 32, 96, 160]
    entropy = ImageEntropyFeatureExtractor(image_values).entropy()
    chosen = policy.select(entropy)
    transformed = policy.apply(image_values, chosen)
    _print_json({"entropy": entropy, "selected_transform": chosen, "transformed": transformed})


def cmd_benchmark(args: argparse.Namespace) -> None:
    backend = MockQuantumBackend()
    circuit = QuantumCircuitSpec(qubits=4, depth=6, operations=["Hadamard", "Oracle", "Diffusion", "Measure"])
    response = backend.execute(circuit, shots=args.shots, seed=args.seed)
    _print_json({"benchmark": "hybrid-quantum-baseline", "result": response, "documentation": "NISQ-era simulator baseline not a claim of quantum advantage."})


def cmd_config(args: argparse.Namespace) -> None:
    settings = RuntimeSettings.from_env()
    _print_json({
        "default_provider": settings.default_provider,
        "default_model": settings.default_model,
        "approval_mode": settings.approval_mode,
        "data_dir": settings.data_dir,
        "quantum": {"backend": settings.quantum.backend, "shots": settings.quantum.shots, "seed": settings.quantum.seed},
    })


def cmd_doctor(args: argparse.Namespace) -> None:
    _print_json(show_doctor())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quantum-Agentic CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat = subparsers.add_parser("chat", help="interactive or single-shot chat")
    chat.add_argument("--prompt", default="Describe a small hybrid quantum-classical task.")
    chat.set_defaults(func=cmd_chat)

    run = subparsers.add_parser("run", help="run a task with the default provider")
    run.add_argument("prompt")
    run.set_defaults(func=cmd_run)

    providers = subparsers.add_parser("providers", help="list configured providers")
    providers.set_defaults(func=cmd_providers)

    backends = subparsers.add_parser("quantum")
    backends_sub = backends.add_subparsers(dest="backend_command", required=True)
    backends_sub.add_parser("backends", help="list supported quantum backends").set_defaults(func=cmd_quantum_backends)

    grover = subparsers.add_parser("agent", help="research prototype agent commands")
    grover_sub = grover.add_subparsers(dest="agent_command", required=True)
    grover_cmd = grover_sub.add_parser("grover")
    grover_cmd.add_argument("--candidates", default="A,B,C,D")
    grover_cmd.add_argument("--mark", type=int, default=0)
    grover_cmd.add_argument("--shots", type=int, default=256)
    grover_cmd.set_defaults(func=cmd_agent_grover)

    bandit_cmd = grover_sub.add_parser("bandit")
    bandit_cmd.add_argument("--arms", type=int, default=3)
    bandit_cmd.add_argument("--episodes", type=int, default=25)
    bandit_cmd.add_argument("--seed", type=int, default=7)
    bandit_cmd.set_defaults(func=cmd_agent_bandit)

    image_cmd = grover_sub.add_parser("image-lab")
    image_cmd.add_argument("--input", default="sample.png")
    image_cmd.set_defaults(func=cmd_agent_image_lab)

    benchmark = subparsers.add_parser("benchmark", help="run a benchmark")
    benchmark.add_argument("--shots", type=int, default=256)
    benchmark.add_argument("--seed", type=int, default=123)
    benchmark.set_defaults(func=cmd_benchmark)

    config = subparsers.add_parser("config", help="show configuration")
    config.set_defaults(func=cmd_config)

    doctor = subparsers.add_parser("doctor", help="run environment checks")
    doctor.set_defaults(func=cmd_doctor)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

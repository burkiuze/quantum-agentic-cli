from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class QuantumCircuitSpec:
    qubits: int
    depth: int
    operations: list[str]


class QuantumBackend:
    name = "base"
    supports_seeded_simulation = False
    max_qubits = 32

    def estimate(self, qubits: int, depth: int) -> dict[str, Any]:
        return {"qubits": qubits, "depth": depth, "estimated_cost": qubits * depth}

    def execute(self, circuit: QuantumCircuitSpec, shots: int = 256, seed: int | None = None) -> dict[str, Any]:
        raise NotImplementedError


class MockQuantumBackend(QuantumBackend):
    name = "mock"
    supports_seeded_simulation = True
    max_qubits = 16

    def execute(self, circuit: QuantumCircuitSpec, shots: int = 256, seed: int | None = None) -> dict[str, Any]:
        counts = {"00": shots // 2, "11": shots // 2} if circuit.qubits >= 2 else {"0": shots}
        return {"backend": self.name, "counts": counts, "seed": seed, "circuit": circuit.operations}


class LocalSimulatorBackend(QuantumBackend):
    name = "simulator"
    supports_seeded_simulation = True
    max_qubits = 20

    def execute(self, circuit: QuantumCircuitSpec, shots: int = 256, seed: int | None = None) -> dict[str, Any]:
        import numpy as np

        rng = np.random.default_rng(seed)
        outcomes = [format(int(rng.integers(0, 2**min(circuit.qubits, 8))), f"0{min(circuit.qubits, 8)}b") for _ in range(shots)]
        counts = {}
        for outcome in outcomes:
            counts[outcome] = counts.get(outcome, 0) + 1
        return {"backend": self.name, "counts": counts, "seed": seed, "circuit": circuit.operations}

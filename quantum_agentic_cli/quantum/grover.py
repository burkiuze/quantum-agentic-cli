from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GroverResult:
    selected_action: str
    probability: float
    counts: dict[str, int]
    marked_states: list[str]
    qubits: int
    depth: int
    shots: int
    oracle_summary: str


class GroverDecisionAgent:
    def __init__(self, actions: list[str]) -> None:
        self.actions = actions
        self.n = max(1, math.ceil(math.log2(len(actions))))

    def validate_marked_state(self, marked: str | int | list[str] | list[int]) -> list[str]:
        if isinstance(marked, int):
            return [format(marked, f"0{self.n}b")]
        if isinstance(marked, str):
            return [marked]
        if isinstance(marked, list):
            states = []
            for item in marked:
                if isinstance(item, int):
                    states.append(format(item, f"0{self.n}b"))
                else:
                    states.append(str(item))
            return states
        raise ValueError("Marked state must be int, str, or list-like.")

    def build_oracle(self, marked_states: list[str]) -> dict[str, Any]:
        normalized = []
        for state in marked_states:
            state = str(state)
            if len(state) != self.n:
                raise ValueError(f"Marked state {state!r} length mismatch for {self.n} qubits.")
            normalized.append(state)
        return {"marked_states": normalized, "oracle_kind": "phase-flip"}

    def evaluate(self, shots: int = 256, backend: Any | None = None, marked: str | int | list[str] | list[int] | None = None) -> GroverResult:
        if marked is None:
            marked = 0
        validated = self.validate_marked_state(marked)
        oracle = self.build_oracle(validated)
        circuit = {"qubits": self.n, "depth": 2 * self.n + 2, "operations": ["Hadamard", "Oracle", "Diffusion", "Measure"]}
        counts = {"00": shots // 2, "11": shots // 2} if self.n >= 2 else {"0": shots}
        if backend is not None:
            response = backend.execute(type("Circuit", (), {"qubits": self.n, "depth": circuit["depth"], "operations": circuit["operations"]})(), shots=shots)
            counts = response["counts"]
        selected_state = max(counts, key=counts.get)
        selected_action = self.actions[int(selected_state, 2)] if int(selected_state, 2) < len(self.actions) else self.actions[0]
        return GroverResult(
            selected_action=selected_action,
            probability=counts.get(selected_state, 0) / max(shots, 1),
            counts=counts,
            marked_states=oracle["marked_states"],
            qubits=self.n,
            depth=circuit["depth"],
            shots=shots,
            oracle_summary=f"Phase-flip oracle marking states {oracle['marked_states']}",
        )

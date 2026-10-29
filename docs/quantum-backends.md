# Quantum backend guide

The project supports a backend abstraction layer rather than tying execution to a single SDK.

## Included backends

- `mock`: deterministic mock backend used for testability and baseline comparisons.
- `simulator`: local NumPy-based simulator backend for general quantum experiments.

## Design principles

- Circuit construction is separate from execution.
- Resource estimates are explicit.
- Measurement counts are returned in a machine-readable format.
- System output distinguishes simulator data from hardware result claims.
- The backend is independent from the runtime and tool orchestration layer.

## Example

```python
from quantum_agentic_cli.quantum.backends import MockQuantumBackend, QuantumCircuitSpec
backend = MockQuantumBackend()
circuit = QuantumCircuitSpec(qubits=4, depth=6, operations=["Hadamard", "Oracle", "Diffusion", "Measure"])
result = backend.execute(circuit, shots=256, seed=123)
print(result)
```

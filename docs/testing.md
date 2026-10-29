# Testing and benchmarking guide

## Core tests

The repository includes tests for:

- tuple contracts,
- mock provider behavior,
- Grover search behavior,
- multi-armed bandit evaluation,
- entropy-driven image transformation,
- memory persistence,
- secret redaction.

## Example

```bash
pytest -q
```

## Benchmarking

```bash
python -m quantum_agentic_cli.cli benchmark --shots 256 --seed 123
```

Use fixed seeds to improve reproducibility. Benchmark outputs are stored in memory and can be serialized to JSON if needed.

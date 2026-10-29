# Architecture overview

The application follows the paper's required Q, C, M, P, A decomposition.

## Components

- Q: `quantum_agentic_cli/quantum`
- C: `quantum_agentic_cli/runtime.py`, `quantum_agentic_cli/cli.py`
- M: `quantum_agentic_cli/memory.py`
- P: `quantum_agentic_cli/cli.py`, `quantum_agentic_cli/runtime.py`
- A: `quantum_agentic_cli/tools.py`, permission checks, local file actions

The runtime dependency direction remains intentionally clean:

- domain and interfaces are independent of vendor-specific provider implementations,
- quantum backends are abstracted behind a backend API,
- all tool execution enters through explicit validation and approval gates.

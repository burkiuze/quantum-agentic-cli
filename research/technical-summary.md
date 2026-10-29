# research/technical-summary.md

# Technical summary of the paper and repo alignment

This repository follows the paper: "Defining Quantum Agents: Formal Foundations, Architectures, and NISQ-Era Prototypes" (MDPI Quantum Reports 2026, 8(1), 24). The paper's abstract frames an important distinction: it is about establishing a formal and architectural understanding of quantum agents under NISQ-era constraints, not a claim that fully autonomous quantum-native cognition is already available.

## 1. Formal definition of quantum agents

The paper introduces a tuple-based representation for a quantum agent. The implementation in this repository follows the required direction:

- Q — Quantum processing: circuit construction, simulation, backend abstraction, measurement, and hardware constraints.
- C — Classical control: planning, orchestration, validation, retries, and policy selection.
- M — Hybrid memory: local conversation state, checkpoints, experiment records, and local retrieval stores.
- P — Perception: user prompts, tool observations, file inputs, measurement feedback, and environment context.
- A — Action: validated tools, file operations, and explicit user-approved external effects.

The core domain model is represented in `quantum_agentic_cli/domain.py` and is intentionally isolated from particular LLM or quantum providers.

## 2. Architectural model and bidirectional agency framework

The paper's broad claim is that quantum computing and agentic AI can reinforce one another. The conceptual architecture is bidirectional:

- quantum computing can enrich policies, search, optimization, and security-related workflows;
- agentic AI can support orchestration, evaluation, and experimental management around quantum routines.

This repository implements the conservative, NISQ-era subset of that idea: a local agent runtime with classical orchestration and optional quantum subroutines. It does not claim fully autonomous quantum-native reasoning or fault-tolerant quantum memory.

## 3. Four-level maturity model

The paper describes a maturity ladder for quantum-agentic systems:

1. Level 1: NISQ-oriented decision agents with classical control and quantum subroutines.
2. Level 2: Hybrid quantum machine learning and variational policy learning.
3. Level 3: Domain-aware adaptation and richer quantum-classical integration.
4. Level 4: Fully quantum-native autonomous systems built on fault-tolerant hardware and advanced memory models.

This repository implements Level 1 and early Level 2 traits only. It explicitly marks Levels 3 and 4 as conceptual future directions.

## 4. Prototypes overview

### Prototype A — Grover-based decision agent

The paper describes a Grover-style decision agent that uses amplitude amplification for a finite candidate set. In this repository, the `GroverDecisionAgent` class models:

- a finite set of candidate actions,
- a marked-state oracle,
- circuit construction and measurement,
- result decoding and action selection,
- comparison with a classical baseline via backend execution.

Important caveat: Grover is useful when the oracle cost is low and the search space is structured. It does not inherently make the whole agent faster end-to-end; the oracle cost and measurement model dominate the total cost.

### Prototype B — Variational quantum reinforcement learning agent

The bandit prototype is implemented in `quantum_agentic_cli/quantum/bandit.py`. It has:

- a configurable multi-armed bandit environment,
- a parameterized policy that maps feature values to action probabilities,
- a learning loop that updates parameters from observed rewards,
- reward and regret summaries for seeded evaluation.

This is an honest hybrid classical-quantum learning prototype. It does not claim general quantum advantage over classical epsilon-greedy baselines.

### Prototype C — Adaptive quantum image transformation and encryption research prototype

The image lab prototype in `quantum_agentic_cli/quantum/image_lab.py` implements entropy-driven action selection across transformations such as XOR, QFT, and scrambling. The code is intentionally framed as an experimental research prototype, not a secure cryptographic system.

The repository explicitly warns that XOR, QFT, scrambling, or a policy circuit are not sufficient to claim cryptographic security.

## 5. Equations and assumptions

The user request cites the paper's generic cost model:

- N_eval = E * C_step
- B_meas = O(N_eval * S * n)

where:

- E = number of agent episodes,
- C_step = circuit evaluations per decision step,
- S = shots,
- n = number of measured qubits.

The implementation tracks the corresponding metrics in structured results and exposes them via benchmark commands and result dictionaries.

In addition, the repository retains the distinction between:

- theoretical complexity,
- measured runtime,
- simulator cost,
- remote QPU latency and availability.

## 6. Practical scope of the implementation

This repository intentionally implements realism and truthful reporting:

- provider adapters are interface-based and configurable,
- secret values are read from environment variables only,
- a local simulator mock backend is included,
- the application can run without physical quantum hardware,
- user actions are permission-guarded,
-quantum algorithms are either real simulations or explicit classical baselines.

## 7. What remains conceptual

The paper's broader vision includes quantum-native autonomy, more advanced memory architectures, and deeper domain integration. These remain conceptual in the paper and are explicitly not claimed to be implemented here.

The repository therefore does the following deliberately:

- labels Levels 3 and 4 as future work,
- documents limitations in the README and docs,
- avoids claims of cryptographic security for research-only transforms,
- avoids unverified quantum advantage claims.

## 8. Traceability table

| Paper concept | Repository module | Status |
| --- | --- | --- |
| Q, C, M, P, A tuple | `quantum_agentic_cli/domain.py` | Implemented |
| LLM provider abstraction | `quantum_agentic_cli/llm` | Implemented |
| Local-first memory | `quantum_agentic_cli/memory.py` | Implemented |
| Security and approval | `quantum_agentic_cli/security.py` | Implemented |
| Grover prototype | `quantum_agentic_cli/quantum/grover.py` | Implemented |
| Bandit prototype | `quantum_agentic_cli/quantum/bandit.py` | Implemented |
| Image lab prototype | `quantum_agentic_cli/quantum/image_lab.py` | Implemented |
| Runtime orchestration | `quantum_agentic_cli/runtime.py` | Implemented |
| CLI experience | `quantum_agentic_cli/cli.py` | Implemented |
| Maturity model, limitations | `README.md` and `research/technical-summary.md` | Documented |
| Full paper PDF | `research/quantumrep-08-00024.pdf` | Retained as local reference / placeholder due environment constraints |

## 9. Summary

The project accurately reflects the optimistic, but still NISQ-era, tone of the paper: a hybrid quantum-classical agent architecture with clear and honest capability boundaries. It is a solid local-first basis for further research, but it should not be mistaken for a production quantum-native autonomous system.

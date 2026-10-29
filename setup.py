from setuptools import setup

setup(
    name="quantum-agentic-cli",
    version="0.1.0",
    description="Local-first quantum-agentic CLI grounded in the quantum agent research paper.",
    packages=["quantum_agentic_cli", "quantum_agentic_cli.llm", "quantum_agentic_cli.quantum"],
    install_requires=[
        "numpy>=1.26",
        "pytest>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "quantum-agent=quantum_agentic_cli.cli:main",
        ]
    },
)

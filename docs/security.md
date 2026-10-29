# Security and privacy guide

This project is local-first and intentionally conservative.

## Security boundaries

- Secrets are not hard-coded in source files.
- Credentials are read from environment variables or secure local config.
- Secret values are redacted before logs or user-facing output.
- Tool execution is schema-validated and permission-controlled.
- Destructive or externally visible actions require explicit approval.
- Untrusted input is never allowed to override system-level rules.

## Key rules

- Never store raw API keys in logs or experiment records.
- Never execute arbitrary shell commands without a clear approval policy.
- Keep all local data in a dedicated directory by default.
- Treat quantum image transforms as experimental and not production encryption.

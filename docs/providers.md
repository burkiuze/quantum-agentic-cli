# Provider setup guide

This project supports multiple provider classes behind a single interface.

## Supported configurations

- `mock`: local default; no credentials required.
- `openai`: use `OPENAI_API_KEY` and optional `OPENAI_BASE_URL`.
- `openrouter`: use `OPENROUTER_API_KEY` and optional `OPENROUTER_BASE_URL`.
- `local`: requires a local inference server URL via `LOCAL_LLM_BASE_URL`.

## Configuration examples

```bash
export DEFAULT_LLM_PROVIDER=openai
export OPENAI_API_KEY="..."
export OPENAI_MODEL_ID="gpt-4o-mini"
```

```bash
export DEFAULT_LLM_PROVIDER=openrouter
export OPENROUTER_API_KEY="..."
export OPENROUTER_MODEL_ID="openai/gpt-4o-mini"
```

```bash
export DEFAULT_LLM_PROVIDER=local
export LOCAL_LLM_BASE_URL="http://localhost:8000/v1"
```

## Failure handling

Provider errors are surfaced as explicit runtime errors. Unsupported features are reported clearly. No provider is required to be available for local development and tests.

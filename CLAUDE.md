# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (including dev group)
uv sync --group dev

# Run all tests
uv run pytest tests

# Run a single test file
uv run pytest tests/test_cli.py

# Run with coverage
uv run pytest --cov=src tests

# Lint
uv run ruff check .

# Type check (strict mode)
uv run mypy .

# Run the CLI directly
uv run repo-audit [REPOSITORY_PATH] [OPTIONS]
```

## Architecture

This is a **multi-agent repository auditor** CLI tool that orchestrates specialist LLM agents (via Mistral AI) to analyze codebases and produce structured audit reports.

### Request flow

```
CLI (typer) → bootstrap.py (factory) → AuditService → parallel specialist agents → OrchestratorAgent → ReportGenerators
```

1. **CLI** (`cli.py`) — parses args, sets up `RichProgressReporter`, calls `AuditService.analyze()`
2. **Bootstrap** (`bootstrap.py`) — wires all dependencies together via `build_audit_service()`; this is the only place where concrete implementations are chosen
3. **AuditService** (`application/audit_service.py`) — orchestrates the full pipeline using `ThreadPoolExecutor` (default 5 workers):
   - Resolves repository source (local path or remote git URL clone)
   - Detects stack (language, frameworks, tools)
   - Runs specialist agents in parallel
   - Synthesizes via `OrchestratorAgent`
   - Optionally generates roadmap via `ProductOwnerAgent`
   - Writes output via report generators
4. **RepositorySource** (`discovery/repository_source.py`) — context manager handling local and remote git repos (shallow clone support, branch/tag/commit checkout)
5. **StackDetector** (`discovery/stack_detector.py`) — glob + file inspection detects Python/JS/TS/Java/.NET, frameworks (Django, FastAPI, React, Vue, Angular), and tooling (Docker, Terraform, monorepo)
6. **AgentRegistry** (`agents/registry.py`) — resolves which `SpecialistAgent` instances to run based on detected stack
7. **ContextBuilder** (`context/context_builder.py`) — assembles per-agent LLM context, respecting a token budget per agent
8. **StackPlugin system** (`plugins/`) — `StackPlugin` ABC adds framework-specific file discovery and context. Built-ins: React, Angular, Vue, Django, FastAPI. Matched via `PluginRegistry`
9. **LLMProvider** (`providers/`) — `MistralProvider` wraps the Mistral SDK with exponential backoff retry logic. `LLMProvider` ABC allows alternative providers
10. **ReportGenerators** (`reports/`) — `MarkdownReportGenerator` and `JSONReportGenerator` write final output files

### Key data models (`domain/models.py`)

- `RepositoryContext` — everything known about the repo (stack, files, manifests, plugins)
- `SourceFile` — a scanned file with path, content, and importance score
- `AuditResult` — collected specialist reports + final orchestrated report + optional roadmap
- `AgentReport` — output from one specialist agent

### Configuration

Settings are loaded via Pydantic `BaseSettings` (`config/settings.py`) from environment variables or a YAML/JSON file passed with `--config`. Required: `MISTRAL_API_KEY`. Each of the 11 agents (2 orchestration + 9 specialist) has its own model ID configurable independently.

### Adding a new specialist agent

1. Create a class inheriting `SpecialistAgent` in `agents/`
2. Register it in `agents/registry.py` with the stack condition under which it activates
3. Add its model ID to `config/settings.py`

### Adding a new framework plugin

1. Create a class inheriting `StackPlugin` in `plugins/builtins/`
2. Register it in `plugins/registry.py`

## Notes

- Prompts and some error messages are in **French** — this is intentional
- Tests are minimal; `tests/test_cli.py` only verifies `--help` exits cleanly
- The `uv` package manager is required (not pip/poetry); Python 3.14+ is the target
- Ruff enforces 100-character line length targeting Python 3.14
- mypy runs in strict mode — all new code must be fully typed

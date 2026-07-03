# Repo Audit Orchestrator

A CLI multi-agent tool that audits a git repository and produces a consolidated report covering architecture, performance, code quality, documentation, security, accessibility, DevOps practices, and UI/UX — plus an optional product roadmap.

It detects your tech stack, builds targeted context for each specialist agent, runs them in parallel through the [Mistral](https://mistral.ai) API, synthesizes their findings into one report, and can generate a prioritized roadmap from the results.

## How it works

1. **Stack detection** — scans the repository for languages, frameworks, and infrastructure tooling (Python, JavaScript/TypeScript, .NET, Java, Docker, Terraform, Ansible, monorepo layout, etc.).
2. **Context building** — collects and chunks relevant source files per agent within a configurable token budget.
3. **Specialist agents** — a configurable set of Mistral agents (architecture, performance, quality, documentation, mentor, security, accessibility, DevOps, UI/UX) each analyze the repository in parallel.
4. **Orchestrator agent** — synthesizes all specialist reports into a single final report.
5. **Product owner agent** *(optional)* — turns the final report into a prioritized roadmap.
6. **Report writer** — outputs the result as Markdown and/or JSON.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- A Mistral API key and a set of Mistral agent IDs (see [Configuration](#configuration))

## Installation

Install `uv`:

```bash
winget install --id=astral-sh.uv
```

Set up the project:

```bash
uv init --package
uv venv
```

## Configuration

Settings are loaded from environment variables (via a `.env` file) or from a config file passed with `--config`.

Create a `.env` file at the repository root:

```dotenv
MISTRAL_API_KEY=your-mistral-api-key

ORCHESTRATOR_AGENT_ID=...
PRODUCT_OWNER_AGENT_ID=...

ARCHITECTURE_AGENT_ID=...
PERFORMANCE_AGENT_ID=...
QUALITE_AGENT_ID=...
DOCUMENTATION_AGENT_ID=...
MENTOR_AGENT_ID=...
SECURITE_AGENT_ID=...
ACCESSIBILITE_AGENT_ID=...
DEVOPS_AGENT_ID=...
UI_UX_AGENT_ID=...
```

Each ID refers to an agent you've created in Mistral's agent platform. Alternatively, pass `--config path/to/config.yaml` (or `.json`) to supply settings explicitly, including which specialist agents are enabled and which frameworks they apply to.

Other tunable settings (execution retries, worker count, token budget per agent, ignored paths during scanning) have sensible defaults and can be overridden the same way.

## Usage

Launch the orchestrator:

```bash
uv run python -m orchestrator
```

Analyze the current directory:

```bash
uv run python -m orchestrator .
```

Or use the installed CLI entry point directly:

```bash
repo-audit analyze [REPOSITORY_PATH] [OPTIONS]
```

**Options:**

| Option | Default | Description |
|---|---|---|
| `--output`, `-o` | `.repo-audit` | Directory where reports are written |
| `--config`, `-c` | none | Path to a YAML/JSON config file |
| `--format` | `markdown` | Report format(s) to generate; repeatable (`markdown`, `json`) |
| `--no-readmap` | off | Skip roadmap generation |

Reports are written to `<output>/report.<format>`.

## Development

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
uv run mypy .
```

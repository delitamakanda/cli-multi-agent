# Repo audit


install uv

```bash
winget install --id=astral-sh.uv
```


init uv

```bash
uv init --package
uv venv
```

launch orchestrator

```bash
uv run python -m orchestrator
```

scanner le dossier actuel

```bash
uv run python -m orchestrator .
```
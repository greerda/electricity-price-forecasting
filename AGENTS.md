# Repository Guidelines

## Project Structure & Module Organization

This repository uses a `src`-layout Python package. Put reusable ingestion, feature-engineering, modeling, and evaluation code under `src/electricity_forecasting/`. Keep exploratory work in `notebooks/`, and name notebooks in execution order, such as `01_data_audit.ipynb`.

Store immutable source files under `data/raw/{nyiso,pjm,noaa}/`, intermediate transformations under `data/interim/`, and analysis-ready datasets under `data/processed/`. Generated models, predictions, and metrics belong in the matching `outputs/` subdirectory. The Quarto report is `reports/capstone.qmd`; its figures and tables belong under `reports/figures/` and `reports/tables/`. Record dataset fields, sources, and analytical decisions in `docs/`.

## Build, Test, and Development Commands

Run commands from `electricity-price-forecasting/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
quarto preview reports/capstone.qmd
```

The editable install should be used once dependencies and optional `dev` extras are declared in `pyproject.toml`. `pytest` runs the test suite; Quarto previews the capstone report. If a command is introduced, document it in `README.md` and configure it in `pyproject.toml` rather than relying on machine-specific setup.

## Coding Style & Naming Conventions

Use four-space indentation, type hints for public functions, and short docstrings describing inputs, outputs, and time-zone assumptions. Follow PEP 8: `snake_case` for modules, functions, and variables; `PascalCase` for classes; `UPPER_SNAKE_CASE` for constants. Prefer small deterministic functions over notebook-only logic. Use timezone-aware timestamps and include market/location identifiers in derived column names when ambiguity is possible.

## Testing Guidelines

Place tests in `tests/`, mirroring package modules (for example, `src/electricity_forecasting/features.py` maps to `tests/test_features.py`). Name tests `test_<behavior>`. Add regression tests for joins, daylight-saving transitions, missing intervals, and leakage-prone time splits. Use tiny synthetic fixtures; do not make tests depend on large raw datasets or network access.

## Data, Security & Reproducibility

Do not commit credentials, API tokens, virtual environments, or generated data artifacts. Preserve raw inputs unchanged and document provenance in `docs/data_source_register.md`. Fix random seeds and save evaluation metrics alongside model outputs.

## Commit & Pull Request Guidelines

No Git history is currently available to establish a local convention. Use concise imperative commits such as `Add NYISO hourly loader`. Pull requests should explain the purpose, data assumptions, validation performed, and affected outputs; link relevant issues and include rendered report screenshots when presentation changes.

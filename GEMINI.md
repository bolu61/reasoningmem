# GEMINI.md - Project Context & Instructions

This file serves as the primary instructional context for Gemini CLI interactions within the `reasoningmem` repository.

## Project Overview
**reasoningmem** is a Python-based tool for extracting, storing, and retrieving the "reasoning" components of AI agent interactions. It aims to build a high-quality, observable logic database by processing chat logs (specifically from Gemini CLI) and extracting structured memory units.

### Core Data Model (`Memory`)
Each reasoning unit consists of:
- **Assumptions:** Underlying premises made by the agent.
- **Thought:** Step-by-step internal reasoning or logic.
- **Hypothesis:** Potential outcomes or predictions.
- **Action:** Primary actions taken or intended.
- **Embedding:** A vector representation for semantic search.

## Technical Stack
- **Language:** Python 3.14+
- **Dependency Management:** `uv`
- **Database:** SQLite via `apsw` (Another Python SQLite Wrapper).
- **Vector Search:** `vectorlite-py` (SQLite extension for vector search).
- **LLM Integration:** `openai` SDK (typically used with OpenRouter/Claude for extraction).
- **Build System:** `hatchling`

## Architecture
- `src/reasoningmem/parse_chat.py`: Parses Gemini CLI chat share JSON format.
- `src/reasoningmem/extract.py`: Uses an LLM to extract structured `Memory` from raw chat turns.
- `src/reasoningmem/memory/memory.py`: Defines the `Memory` dataclass.
- `src/reasoningmem/memory/vector_store.py`: (Planned) Storage layer using SQLite and vectorlite.

## Key Commands
Always use `uv` for execution to ensure the virtual environment is used correctly.

```bash
# Install/Sync dependencies
uv sync

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_file.py::test_function
uv run pytest tests/test_file.py -k "test_name_pattern"

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Linting and Formatting
uv run ruff check .
uv run ruff format .

# Type Checking
uv run mypy src/

# Build
uv run hatch build
```

## Development Conventions
- **Mandatory Linting & Type Checking:** Always run `uv run ruff check .` and `uv run mypy src/` to ensure code quality and type safety. Fix all violations before considering a task complete.
- **Testing Requirements:** Every implementation or bug fix **must** include corresponding test cases using `pytest`. Test files should be located in a `tests/` directory mirroring the `src/` structure.
  - Follow Arrange-Act-Assert (Given-When-Then) structure.
  - Use `pytest` fixtures for setup/teardown.
  - Mock external dependencies (APIs, databases, file system) with `unittest.mock` or `pytest-mock`.
- **Regular Validation:** Run tests frequently during development (`uv run pytest`), and always perform a full test pass after any significant changes to ensure no regressions.
- **Documentation Maintenance:** Any new information about the repository, architectural decisions, or conventions learned during development should be added back to this `GEMINI.md` file to keep the context up to date.
- **Type Safety:** Use type hints on all function signatures and public APIs.
  - Prefer `typing` module types: `Optional`, `Union`, `List`, `Dict`, etc.
  - Avoid `Any` — use specific types.
  - Use `dataclasses` for structured data.
- **Error Handling:** Fail fast — validate inputs at function boundaries. Use custom exception classes for domain-specific errors.
- **Environment Variables:**
  - `LLM_API_KEY`: Required for extraction logic.
  - `LLM_BASE_URL`: Optional, defaults to OpenRouter.

## Code Style & Conventions
- **General:** Follow PEP 8. Mimic neighboring files. Keep functions small/focused. Prefer early returns.
- **Naming Conventions:**
  - Variables/Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE`
  - Modules/Files: `snake_case`
  - Test files: `test_*.py`
- **Imports:** Group by (standard library → third-party → local). Use absolute imports. Order alphabetically.
- **Formatting:** 4-space indentation. Max line length: 100. Double quotes for strings. Use f-strings.
- **Git:** Use imperative mood in commit messages. Small, focused commits. Never commit secrets.

## Tool-Specific Instructions
- When adding new modules, ensure `__init__.py` files are updated if they expose public APIs.
- Prefer `apsw` for database operations as per project requirements.
- Maintain compatibility with Gemini CLI chat share JSON structures.

# AGENTS.md - Guidelines for Agentic Coding Agents

## Repository Overview
- **Name:** reasoningmem
- **Remote:** https://github.com/bolu61/reasoningmem.git
- **Type:** Python project
- **Status:** Update this file as the project takes shape.

## Build / Lint / Test Commands
> Replace placeholders with actual commands once dependencies are defined.

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_file.py::test_function
uv run pytest tests/test_file.py -k "test_name_pattern"

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Lint
uv run ruff check .

# Type check
uv run mypy src/

# Format
uv run ruff format .

# Build
uv run hatch build
```

## Code Style Guidelines

### General Conventions
- Follow PEP 8 as the baseline style guide.
- Follow the conventions already established in the codebase.
- When in doubt, mimic the style of neighboring files.
- Keep functions small and focused (single responsibility).
- Prefer early returns over deep nesting.

### Naming Conventions
| Element        | Convention      | Example              |
|----------------|-----------------|----------------------|
| Variables      | snake_case      | `user_count`         |
| Functions      | snake_case      | `calculate_total()`  |
| Classes        | PascalCase      | `UserService`        |
| Constants      | UPPER_SNAKE     | `MAX_RETRIES`        |
| Modules/Files  | snake_case      | `user_service.py`    |
| Test files     | `test_*.py`     | `test_user.py`       |
| Private members| `_leading_underscore` | `_internal_helper()` |

### Imports
- Group imports: standard library → third-party → local modules.
- Separate groups with a blank line.
- Use absolute imports over relative imports unless the project dictates otherwise.
- Remove unused imports.
- Order imports alphabetically within each group.

### Formatting
- 4-space indentation (per PEP 8).
- Max line length: 100 characters (or 88 if using Black).
- Trailing commas in multi-line structures.
- Double quotes for strings (or single quotes if the project uses them consistently).
- Use f-strings for string interpolation (Python 3.6+).

### Types
- Use type hints on all function signatures and public APIs.
- Prefer `typing` module types: `Optional`, `Union`, `List`, `Dict`, etc. (or built-in generics on Python 3.9+).
- Avoid `Any` — use specific types or `typing.Protocol` when needed.
- Use `dataclasses` or `pydantic` models for structured data.
- Make fields non-nullable by default; use `Optional[T]` explicitly.

### Error Handling
- Fail fast — validate inputs at function boundaries.
- Use custom exception classes for domain-specific errors.
- Never use bare `except:` — always catch specific exceptions.
- Use `logging` module instead of `print()` for error reporting.
- In async code, always handle exceptions and avoid silent failures.

### Testing
- Write tests for all new features and bug fixes.
- Test files live in a parallel `tests/` directory mirroring the source structure.
- Follow Arrange-Act-Assert (Given-When-Then) structure.
- Use `pytest` fixtures for setup/teardown.
- Mock external dependencies (APIs, databases, file system) with `unittest.mock` or `pytest-mock`.
- Test file naming: `test_<module>.py` with functions named `test_<behavior>()`.

### Git Conventions
- Commit messages: imperative mood, concise subject line.
- Small, focused commits — one logical change per commit.
- Never commit secrets, `.env` files, or credentials.
- Run lint + typecheck + tests before committing.
- Use `.gitignore` to exclude `__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`, etc.

## Notes for Agents
1. **Always read existing files first** to understand conventions before making changes.
2. **Run ruff check and mypy** after modifying code — fix all violations.
3. **Run relevant tests** to verify changes don't break existing behavior.
4. **Do not commit** unless the user explicitly asks.
5. **Update this file** when you discover project-specific conventions or commands.

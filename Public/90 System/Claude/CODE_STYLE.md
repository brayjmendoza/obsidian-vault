---
type: system
created: 2026-11-01
updated: 2026-11-07
version: "1.0"
---
# Code Style

How Python in this vault should be written. Today that means `91 Tooling/` (the `vault_tools` package and its tests). Every skill or run that writes or edits Python reads this file after [[CONVENTIONS]]. The checks in [[#The Bar]] are enforced by tools and CI. The rest needs judgment, so Claude applies it when writing code and when reviewing it.

## The Bar

Code isn't done until all four pass from `91 Tooling/`:

```bash
export UV_PROJECT_ENVIRONMENT=$HOME/.venvs/vault-tools
uv run ruff format --check
uv run ruff check
uv run mypy
uv run pytest
```

- **Settings live in `pyproject.toml`.** The ruff rule set, line length (100), and mypy's `strict = true` are configured there, not restated here. Tests meet the same strict mypy as `vault_tools/`, with no override.
- **No silenced checks without a reason.** A `# noqa` or `# type: ignore` names the exact code (e.g., `# type: ignore[arg-type]`) and carries a comment saying why the tool is wrong. Never a bare one.
- **No new warnings.** A change that makes any of the four noisier isn't done, even if it passes.

## Data Models

- **pydantic, not dataclasses.** Every structured value is a `pydantic.BaseModel`. Don't use `dataclasses`, `NamedTuple`, `TypedDict`, or plain dicts for data that has a known shape.
- **Frozen by default.** Models set `model_config = ConfigDict(frozen=True, extra="forbid")`. A mutable model needs a comment saying why. Build a value completely, then construct it, instead of creating it empty and appending to it.
- **Parse at the boundary.** Anything read from outside the program (YAML schemas, JSON, command-line input) is parsed into a model with `Model.model_validate(...)` the moment it's loaded. Past the loader, code works with typed models, never `dict[str, Any]`.
- **Strict parsing for external data.** Models that parse files set `strict=True`, so `"3"` never quietly becomes `3`. Their sequence fields are `list`, not `tuple`, because strict mode won't read a YAML list as a tuple. Use `Field(alias=...)` for keys that aren't valid Python names or would shadow a builtin (e.g., `value_range` for `range`).
- **Turn validation errors into issues.** A schema that fails to parse is a vault problem, not a crash: catch `pydantic.ValidationError` at the loader and report each error as an `Issue` with the path to the bad key.
- **Note frontmatter is the exception.** Judging frontmatter types is the validator's job, so property values stay loosely typed. Type them with a recursive `YamlValue` alias (text, number, checkbox, date, list, mapping, or none), never `Any`.
- **Serialize with pydantic.** Use `model_dump(mode="json", exclude_none=True)` instead of hand-written `to_dict` methods.
- **mypy plugin on.** `pyproject.toml` loads `pydantic.mypy` so field types and constructors are checked.

## Typing

- **Annotate everything:** every parameter, return value, and module-level constant, private helpers and tests included. Test functions return `-> None`.
- **No `Any`.** Use a precise type, a `YamlValue`-style alias, or `object` narrowed with `isinstance`. `cast` needs a comment saying why it's safe.
- **Closed sets are enums.** A value with a fixed set of options (e.g., severity, check name, Obsidian property type) is a `StrEnum` or a `Literal`, not a bare `str` with a comment listing the options.
- **Modern syntax:** `X | None`, built-in generics (`list[str]`), `type` statements for aliases, and `Final` for constants. Python 3.14 evaluates annotations lazily, so don't add `from __future__ import annotations`.
- **Accept abstract, return concrete.** Parameters take `Iterable`, `Sequence`, or `Mapping` from `collections.abc`; return values are `list`, `dict`, or a model.
- **No `assert` to narrow types in `vault_tools/`.** Asserts vanish under `python -O`. Restructure (e.g., `functools.cached_property` instead of an `Optional` cache plus an assert) or raise a real exception. Asserts belong in tests.

## Functions and Classes

- **One job each.** A function that needs "and" in its summary line is two functions. Aim for functions that fit on a screen.
- **Plain functions over classes.** Use a class when there's real state to share between methods, not as a namespace for functions. Modules are namespaces.
- **Pure where possible.** Keep loading and printing at the edges; the checks themselves take values and return issues.
- **Flags are keyword-only.** A `bool` parameter goes after `*` so call sites read `load(path, strict=True)`, never `load(path, True)`.
- **No mutable defaults.** Use `None` or a pydantic `Field(default_factory=...)`.
- **Return early.** Guard clauses at the top instead of nested `if`/`else` ladders. Use `match` when branching on the shape of a value reads more clearly than an `isinstance` chain.
- **No side effects at import.** Modules define constants, models, and functions. Work happens in functions, and command-line work happens only in `main()`.

## Naming

- **PEP 8 casing:** `snake_case` for functions and variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants, a leading `_` for anything private to its module.
- **Full words.** `properties`, not `props`; `issue`, not `iss`. One-letter names only for loop indexes and short comprehensions. Common abbreviations are fine (e.g., `rel` for a relative path, `yaml`, `cli`).
- **Name things after the vault's vocabulary.** Use the terms in [[CONVENTIONS]] and the schemas (e.g., note type, domain, hub, role folder), so code and docs read the same.

## Docstrings and Comments

- **Google style, everywhere in `vault_tools/`.** Every module, class, function, and method has a docstring, private ones included.
- **Summary line first.** One line in the imperative mood, ending in a period (e.g., "Resolve a link target the way Obsidian does.").
- **Sections when they apply:** `Args:`, `Returns:`, `Yields:`, and `Raises:`, in that order. Leave out a section with nothing in it. Don't repeat type hints in the text.
- **Classes document attributes.** A model lists its fields under `Attributes:`, or gives each field a `Field(description=...)`.
- **Tests get a one-line docstring** saying what behavior the test pins down. Fixture parameters don't need an `Args:` section.
- **Comments say why, not what.** Explain a surprising choice or point to the rule it enforces (e.g., "# CONVENTIONS section 4: one property name, one value type"). Delete comments that restate the code, and never leave commented-out code.

## Errors

- **Vault problems are issues; program problems are exceptions.** A bad note or a bad schema becomes an `Issue` in the report. A bug or an unreadable folder raises.
- **Catch narrowly.** Name the exceptions you expect (e.g., `OSError`, `yaml.YAMLError`). Never a bare `except:` or `except Exception:`, and never swallow an exception without recording it.
- **Chain re-raises:** `raise LoadError(...) from exc`, so the original cause survives.
- **Only the command line exits.** Library code returns or raises. `main()` turns results into exit codes and prints.

## Files and Output

- **`pathlib` only.** No `os.path` string handling.
- **Explicit encoding.** Every `read_text`, `write_text`, and `open` passes `encoding="utf-8"`.
- **Normalize names.** Compare file and note names after NFC normalization, since macOS stores them decomposed.
- **No `print` outside `main()`.** Everything else returns data for the command line to format.

## Imports

- **Define once, import everywhere.** A constant, helper, model, or type alias used by more than one module lives in exactly one of them, and the others import it. Tests import too: `conftest.py` takes `TOOLING_DIR` from `vault_tools.vault` instead of computing its own. When two modules start to grow the same code, move it to the module that owns the idea.
- **Absolute imports:** `from vault_tools.vault import Vault`, not `from .vault import Vault`.
- **Ordered by ruff.** Standard library, third-party, then first-party, as `ruff check` sorts them. No wildcard imports, and no imports inside functions unless it breaks a cycle (with a comment saying so).

## Tests

- **pytest functions, not classes.** One test file per module in `vault_tools/`, plus files for the schemas and the command line.
- **Parametrize instead of looping.** A test that checks several cases uses `@pytest.mark.parametrize`, so each case passes or fails on its own.
- **Never touch the real vault.** Tests read the fixtures in `tests/fixtures/` and write only under `tmp_path` (e.g., through `copy_fixture`).
- **Every fix comes with a test** that fails without the fix. Every new check comes with a fixture that trips it.
- **Assert on whole values.** Compare the full set of issue keys or the full JSON object, so an unexpected extra issue fails the test.

## Dependencies

- **Managed by uv.** Add packages with `uv add` or `uv add --dev`, never pip, and commit `pyproject.toml` and `uv.lock` together (see `91 Tooling/README.md`).
- **Few runtime dependencies.** PyYAML, pydantic, and requests are the runtime dependencies. A new one needs your approval and a reason the standard library can't do the job.

## Changelog

- 2026-11-01 · 1.1 · Added "Define once, import everywhere" to Imports: shared constants and helpers live in one module and are imported, tests included. Strict models use `list` fields.
- 2026-11-01 · 1.0 · First version: pydantic instead of dataclasses, parse external data into models at the boundary, ruff and strict mypy (tests included) as the bar, Google-style docstrings throughout `vault_tools/`, and general rules for typing, functions, naming, errors, files, imports, tests, and dependencies.

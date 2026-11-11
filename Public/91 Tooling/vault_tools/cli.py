"""The command line every validator shares: arguments, the report, and exit codes."""

import argparse
import io
import sys
from collections.abc import Callable, Iterable, Sequence
from enum import IntEnum
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict

from vault_tools.issues import Issue, Severity, sort_key
from vault_tools.schemas import SchemaError
from vault_tools.vault import DEFAULT_SCHEMA_DIR, DEFAULT_VAULT_ROOT, Vault

type Check = Callable[[Vault], list[Issue]]


class ExitCode(IntEnum):
    """What a validator's exit status means."""

    OK = 0  # no errors; warnings are allowed
    ERRORS = 1
    LOAD_FAILED = 2  # the vault or a schema file couldn't be read


class CliArgs(BaseModel):
    """The parsed command-line arguments.

    Attributes:
        vault: The Public/ folder to check.
        schemas: The folder holding the schemas.
        private: The Private/ folder, when given explicitly.
        as_json: Whether to print a JSON report instead of text.
        output: A file to also write the JSON report to.
        skip_urls: Whether to leave out the URL check (i.e., `--skip-urls`).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    vault: Path
    schemas: Path
    private: Path | None
    as_json: bool
    output: Path | None
    skip_urls: bool = False


class Summary(BaseModel):
    """Issue counts for a report.

    Attributes:
        errors: How many errors.
        warnings: How many warnings.
        ok: Whether there are no errors.
    """

    model_config = ConfigDict(frozen=True)

    errors: int
    warnings: int
    ok: bool


class Report(BaseModel):
    """Everything a validator found, as printed or written to JSON.

    Attributes:
        vault: The Public/ folder checked.
        schema_version: The schemas' shared version, when they loaded.
        notes_checked: How many notes the properties validator looked at.
        summary: Issue counts.
        skipped: Checks this run couldn't or didn't do, and why.
        issues: Every issue, sorted by path.
    """

    model_config = ConfigDict(frozen=True)

    vault: str
    schema_version: str | None
    notes_checked: int
    summary: Summary
    skipped: list[str]
    issues: list[Issue]


def build_parser(description: str, *, offers_skip_urls: bool = False) -> argparse.ArgumentParser:
    """Build the argument parser every validator shares.

    Args:
        description: What the validator checks, for `--help`.
        offers_skip_urls: Whether to add `--skip-urls`, for a command whose
            checks include fetching every `url`.

    Returns:
        The parser.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "vault",
        nargs="?",
        type=Path,
        default=DEFAULT_VAULT_ROOT,
        help="path to the Public/ folder (default: the one this package lives in)",
    )
    parser.add_argument(
        "--schemas",
        type=Path,
        default=DEFAULT_SCHEMA_DIR,
        help="folder holding both schema files (default: 91 Tooling/schemas)",
    )
    parser.add_argument(
        "--private",
        type=Path,
        metavar="DIR",
        help="the Private/ folder, whose file names (never contents) are checked against "
        "Public links (default: Private/ beside the vault, if it exists)",
    )
    parser.add_argument(
        "--json", dest="as_json", action="store_true", help="print a JSON report instead of text"
    )
    parser.add_argument(
        "--output", type=Path, metavar="FILE", help="also write the JSON report to FILE"
    )
    if offers_skip_urls:
        parser.add_argument(
            "--skip-urls",
            action="store_true",
            help="don't fetch any `url` (default: fetch every one over the network)",
        )
    return parser


def build_report(
    vault: Path,
    schema_version: str | None,
    notes_checked: int,
    issues: Iterable[Issue],
    skipped: Sequence[str] = (),
) -> Report:
    """Count and sort issues into a report.

    Args:
        vault: The Public/ folder checked.
        schema_version: The schemas' shared version, when they loaded.
        notes_checked: How many notes were checked.
        issues: What the checks found.
        skipped: Checks the run couldn't or didn't do, and why.

    Returns:
        The report.
    """
    ordered = sorted(issues, key=sort_key)
    errors = sum(1 for issue in ordered if issue.severity == Severity.ERROR)
    summary = Summary(errors=errors, warnings=len(ordered) - errors, ok=errors == 0)
    return Report(
        vault=str(vault),
        schema_version=schema_version,
        notes_checked=notes_checked,
        summary=summary,
        skipped=list(skipped),
        issues=ordered,
    )


def plural(count: int, word: str) -> str:
    """Write a count with its noun, adding `s` unless the count is 1.

    Args:
        count: How many.
        word: The singular noun.

    Returns:
        For example, `1 error` or `3 errors`.
    """
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def format_text(report: Report) -> str:
    """Format a report for people: issues grouped by path, then a summary line.

    Args:
        report: The report.

    Returns:
        The text, without a trailing newline.
    """
    lines: list[str] = []
    current: str | None = None
    for issue in report.issues:
        if issue.path != current:
            current = issue.path
            lines.append(f"\n{current}")
        prop = f" [{issue.property}]" if issue.property else ""
        lines.append(f"  {issue.severity:7} {issue.code}{prop}: {issue.message}")
    if report.skipped:
        lines.append("\n" + "\n".join(f"skipped: {reason}" for reason in report.skipped))
    summary = report.summary
    lines.append(
        f"\n{report.notes_checked} notes checked: "
        f"{plural(summary.errors, 'error')}, {plural(summary.warnings, 'warning')}"
    )
    return "\n".join(lines).lstrip("\n")


def format_json(report: Report) -> str:
    """Format a report as JSON, leaving out empty fields.

    Args:
        report: The report.

    Returns:
        Indented JSON, without a trailing newline.
    """
    return report.model_dump_json(indent=2, exclude_none=True)


def skipped_checks(vault: Vault, *, checks_private_links: bool, skip_urls: bool) -> list[str]:
    """List the checks a run leaves out, so a clean report isn't mistaken for a full one.

    Args:
        vault: The loaded vault.
        checks_private_links: Whether the command checks links into Private/.
        skip_urls: Whether `--skip-urls` left out the URL check.

    Returns:
        One sentence per skipped check.
    """
    skipped = []
    if skip_urls:
        skipped.append("urls: --skip-urls was given, so no `url` was fetched")
    if checks_private_links and vault.private_dir is None:
        skipped.append(
            "private links by name: no Private/ folder beside Public/ (only links with "
            "a Private/ path were checked)"
        )
    return skipped


def run_checks(args: CliArgs, check: Check, *, checks_private_links: bool) -> Report:
    """Load the vault and run the checks over it.

    A schema that breaks its own rules isn't a crash: its problems become the report.

    Args:
        args: The parsed arguments.
        check: The check to run.
        checks_private_links: Whether `check` covers links into Private/.

    Returns:
        The report.

    Raises:
        OSError: The vault or a schema file can't be read.
        yaml.YAMLError: A schema file isn't valid YAML.
    """
    try:
        vault = Vault(args.vault, args.schemas, args.private)
    except SchemaError as exc:
        return build_report(args.vault.resolve(), None, 0, exc.issues)
    issues = check(vault)
    skipped = skipped_checks(
        vault, checks_private_links=checks_private_links, skip_urls=args.skip_urls
    )
    return build_report(
        vault.root, vault.properties_schema.version, len(vault.notes), issues, skipped
    )


def run_cli(
    description: str,
    check: Check,
    argv: Sequence[str] | None = None,
    *,
    checks_private_links: bool = False,
    check_without_urls: Check | None = None,
) -> int:
    """Run a validator from the command line.

    Args:
        description: What the validator checks, for `--help`.
        check: The check to run.
        argv: The arguments, without the program name; `sys.argv[1:]` when None.
        checks_private_links: Whether `check` covers links into Private/, so the
            report says when Private/ couldn't be seen.
        check_without_urls: The same checks without fetching any `url`. Giving
            it adds `--skip-urls`, which runs it instead of `check`.

    Returns:
        The exit code: see `ExitCode`.
    """
    parser = build_parser(description, offers_skip_urls=check_without_urls is not None)
    args = CliArgs.model_validate(vars(parser.parse_args(argv)))
    chosen = check_without_urls if args.skip_urls and check_without_urls is not None else check
    try:
        report = run_checks(args, chosen, checks_private_links=checks_private_links)
    except (OSError, yaml.YAMLError) as exc:
        print(f"could not load the vault or schemas: {exc}", file=sys.stderr)
        return ExitCode.LOAD_FAILED
    # Windows consoles default to a legacy code page; note names aren't ASCII.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.output is not None:
        args.output.write_text(format_json(report) + "\n", encoding="utf-8")
    print(format_json(report) if args.as_json else format_text(report))
    return ExitCode.OK if report.summary.ok else ExitCode.ERRORS

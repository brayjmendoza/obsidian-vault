"""Enforce properties-schema.yaml on every note's frontmatter.

Checks, per note: a known `type`; required properties present and not empty;
no unknown or disallowed properties; each value has its property's one type;
no nested objects; vocab, range, pattern, and typed-link constraints.

    vault-validate-properties [PUBLIC_DIR] [--json]
    python -m vault_tools.validate_properties
"""

import datetime as dt
import re
import sys
from collections.abc import Sequence
from typing import Final, TypeIs, assert_never

from pydantic import BaseModel, ConfigDict

from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue, warning_issue
from vault_tools.schemas import PROPERTIES_SCHEMA, Constraint, ObsidianType
from vault_tools.vault import (
    UNTYPED_ALLOWED_FOLDERS,
    Note,
    PrivateMatch,
    Vault,
    YamlValue,
    parse_link,
)

DESCRIPTION: Final = "Enforce properties-schema.yaml on every note's frontmatter."
CHECK: Final = CheckName.PROPERTIES
TEMPLATE_TYPE: Final = "template"
ISO_DATE_RE: Final = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class TypeProblem(BaseModel):
    """Why a value doesn't have its property's type.

    Attributes:
        code: The issue code to report.
        message: What's wrong, with a hint where one helps.
    """

    model_config = ConfigDict(frozen=True)

    code: IssueCode
    message: str


class MergedRules(BaseModel):
    """A note type's rules with the `common` block folded in.

    Attributes:
        required: Properties a note of this type must have.
        allowed: Every property it may have.
        constraints: Value rules by property; the type's own override `common`.
    """

    model_config = ConfigDict(frozen=True)

    required: list[str]
    allowed: frozenset[str]
    constraints: dict[str, Constraint]


# -- value checks ---------------------------------------------------------------


def is_number(value: YamlValue) -> TypeIs[int | float]:
    """Check for a number, which in Python a checkbox (bool) is not.

    Args:
        value: A property value.

    Returns:
        Whether it is an int or float but not a bool.
    """
    return isinstance(value, int | float) and not isinstance(value, bool)


def is_empty(value: YamlValue) -> bool:
    """Check for a property left blank: no value, empty text, or an empty list.

    Args:
        value: A property value.

    Returns:
        Whether the property is blank.
    """
    return value is None or value == "" or value == []


def is_unquoted_link(value: YamlValue) -> bool:
    """Detect an unquoted [[Note]], which YAML reads as a list holding a list.

    Args:
        value: A property value.

    Returns:
        Whether the value has that shape.
    """
    return (
        isinstance(value, list)
        and len(value) == 1
        and isinstance(value[0], list)
        and len(value[0]) == 1
        and isinstance(value[0][0], str)
    )


def is_iso_date(value: str) -> bool:
    """Check for a real calendar date written `YYYY-MM-DD`.

    Args:
        value: Text from a property.

    Returns:
        Whether it is one.
    """
    if not ISO_DATE_RE.match(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_iso_datetime(value: str) -> bool:
    """Check for an ISO 8601 date and time.

    Args:
        value: Text from a property.

    Returns:
        Whether Python can read it as a datetime.
    """
    try:
        dt.datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def describe(value: YamlValue) -> str:
    """Name a value's type in Obsidian's terms, for messages.

    Args:
        value: A property value.

    Returns:
        For example, `checkbox`, `date`, or `nested object`.
    """
    match value:
        case bool():
            return "checkbox"
        case int() | float():
            return "number"
        case dt.datetime():
            return "datetime"
        case dt.date():
            return "date"
        case str():
            return "text"
        case list():
            return "list"
        case dict():
            return "nested object"
        case _:
            return type(value).__name__


def has_type(kind: ObsidianType, value: YamlValue) -> bool:
    """Check whether a value has an Obsidian type.

    Text in ISO form counts as a date or datetime, since Obsidian reads it as one.

    Args:
        kind: The type the property must have.
        value: The value.

    Returns:
        Whether the value has that type.
    """
    match kind:
        case ObsidianType.TEXT:
            return isinstance(value, str)
        case ObsidianType.NUMBER:
            return is_number(value)
        case ObsidianType.CHECKBOX:
            return isinstance(value, bool)
        case ObsidianType.DATE:
            if isinstance(value, str):
                return is_iso_date(value)
            return isinstance(value, dt.date) and not isinstance(value, dt.datetime)
        case ObsidianType.DATETIME:
            return isinstance(value, dt.datetime) or (
                isinstance(value, str) and is_iso_datetime(value)
            )
        case ObsidianType.LIST:
            return isinstance(value, list)
        case _:
            assert_never(kind)


def type_problem(kind: ObsidianType, value: YamlValue) -> TypeProblem | None:
    """Explain why a value doesn't have its property's type.

    Args:
        kind: The type the property must have.
        value: The value.

    Returns:
        The problem, or None when the value is fine.
    """
    items = value if kind == ObsidianType.LIST and isinstance(value, list) else []
    if is_unquoted_link(value) or any(is_unquoted_link(item) for item in items):
        return TypeProblem(
            code=IssueCode.WRONG_VALUE_TYPE,
            message='links in properties must be quoted, e.g. "[[Note]]"',
        )
    if isinstance(value, dict):
        return TypeProblem(
            code=IssueCode.NESTED_OBJECT,
            message="nested objects aren't allowed; put structured data in a body table",
        )
    if not has_type(kind, value):
        hint = ""
        if kind == ObsidianType.LIST and isinstance(value, str):
            hint = " (lists are YAML lists, never comma strings)"
        elif kind == ObsidianType.DATE:
            hint = " (use YYYY-MM-DD)"
        return TypeProblem(
            code=IssueCode.WRONG_VALUE_TYPE, message=f"expected {kind}, got {describe(value)}{hint}"
        )
    if isinstance(value, list) and any(isinstance(item, dict | list) for item in value):
        return TypeProblem(
            code=IssueCode.NESTED_OBJECT,
            message="list items must be single values, not nested objects or lists",
        )
    return None


# -- per-note checks ------------------------------------------------------------


class PropertyChecker:
    """Checks notes' frontmatter against the properties schema."""

    def __init__(self, vault: Vault) -> None:
        """Merge each note type's rules with `common` once, up front.

        Args:
            vault: The vault whose notes and schema to use.
        """
        self.vault = vault
        self.schema = vault.properties_schema
        common = self.schema.common
        self.rules = {
            name: MergedRules(
                required=common.required + rules.required,
                allowed=frozenset(common.declared + rules.declared),
                constraints=common.constraints | rules.constraints,
            )
            for name, rules in self.schema.types.items()
        }

    def check(self, note: Note) -> list[Issue]:
        """Check one note's frontmatter.

        Args:
            note: The note.

        Returns:
            Every issue found, including problems hit while loading it.
        """
        if note.load_issues:
            return list(note.load_issues)
        note_type = note.note_type
        if note_type is None:
            if note.top_folder in UNTYPED_ALLOWED_FOLDERS:
                return []  # untyped captures and attachment notes
            what = "frontmatter" if note.properties is None else "a `type` property"
            return [self._error(note, IssueCode.MISSING_TYPE, f"note has no {what}", "type")]
        if not isinstance(note_type, str) or note_type not in self.rules:
            message = f"type {note_type!r} is not a note type in {PROPERTIES_SCHEMA}"
            return [self._error(note, IssueCode.UNKNOWN_TYPE, message, "type")]
        if note_type == TEMPLATE_TYPE:
            return self._check_template(note)
        return self._check_required(note, note_type) + self._check_values(note, note_type)

    def _check_template(self, note: Note) -> list[Issue]:
        """Check a template, whose other properties hold placeholders.

        Args:
            note: A note of type `template`.

        Returns:
            An issue when it has no `version`.
        """
        if is_empty((note.properties or {}).get("version")):
            message = "templates need a `version`"
            return [self._error(note, IssueCode.MISSING_PROPERTY, message, "version")]
        return []

    def _check_required(self, note: Note, note_type: str) -> list[Issue]:
        """Check that every required property is present and not blank.

        Args:
            note: The note.
            note_type: Its type, known to the schema.

        Returns:
            One issue per missing or blank required property.
        """
        properties = note.properties or {}
        issues = []
        for prop in self.rules[note_type].required:
            if prop not in properties:
                message = f"required for type {note_type!r}"
                issues.append(self._error(note, IssueCode.MISSING_PROPERTY, message, prop))
            elif is_empty(properties[prop]):
                message = f"required for type {note_type!r} but empty"
                issues.append(self._error(note, IssueCode.EMPTY_PROPERTY, message, prop))
        return issues

    def _check_values(self, note: Note, note_type: str) -> list[Issue]:
        """Check every property the note carries.

        Args:
            note: The note.
            note_type: Its type, known to the schema.

        Returns:
            Every issue with a property's name, type, or value.
        """
        issues: list[Issue] = []
        for prop, value in (note.properties or {}).items():
            issues += self._check_value(note, note_type, prop, value)
        return issues

    def _check_value(self, note: Note, note_type: str, prop: str, value: YamlValue) -> list[Issue]:
        """Check one property: declared, allowed, not blank, the right type, and constrained.

        Args:
            note: The note.
            note_type: Its type, known to the schema.
            prop: The property name.
            value: Its value.

        Returns:
            The first problem found, plus every constraint it breaks.
        """
        rules = self.rules[note_type]
        kind = self.schema.property_types.get(prop)
        if kind is None:
            message = f"{prop!r} is not declared in {PROPERTIES_SCHEMA}"
            return [self._error(note, IssueCode.UNKNOWN_PROPERTY, message, prop)]
        if prop not in rules.allowed:
            message = f"{prop!r} is not a property of type {note_type!r}"
            return [self._error(note, IssueCode.PROPERTY_NOT_ALLOWED, message, prop)]
        if is_empty(value):
            message = "empty properties aren't allowed; remove it if there's no value"
            return [self._error(note, IssueCode.EMPTY_PROPERTY, message, prop)]
        problem = type_problem(kind, value)
        if problem is not None:
            return [self._error(note, problem.code, problem.message, prop)]
        constraint = rules.constraints.get(prop)
        if constraint is None:
            return []
        items = value if isinstance(value, list) else [value]
        return [
            issue
            for item in items
            for issue in self._check_constraint(note, prop, item, constraint)
        ]

    def _check_constraint(
        self, note: Note, prop: str, item: YamlValue, constraint: Constraint
    ) -> list[Issue]:
        """Check one value (or one list item) against a property's constraint.

        Args:
            note: The note.
            prop: The property name.
            item: The value, or one item of a list value.
            constraint: The property's rules for this note type.

        Returns:
            One issue per rule the value breaks.
        """
        issues = []
        if constraint.vocab is not None:
            allowed = self.schema.vocabularies[constraint.vocab]
            if not isinstance(item, str) or item not in allowed:
                message = (
                    f"{item!r} is not in vocabulary {constraint.vocab!r} ({', '.join(allowed)})"
                )
                issues.append(self._error(note, IssueCode.NOT_IN_VOCAB, message, prop))
        if constraint.value_range is not None:
            low, high = constraint.value_range
            if not is_number(item) or not low <= item <= high:
                message = f"{item!r} is outside [{low}, {high}]"
                issues.append(self._error(note, IssueCode.OUT_OF_RANGE, message, prop))
        if constraint.pattern is not None and (
            not isinstance(item, str) or not constraint.pattern.search(item)
        ):
            message = f"{item!r} does not match {constraint.pattern.pattern}"
            issues.append(self._error(note, IssueCode.PATTERN_MISMATCH, message, prop))
        if constraint.link is not None:
            issues += self._check_link(note, prop, item, constraint.link)
        return issues

    def _check_link(self, note: Note, prop: str, item: YamlValue, wanted: list[str]) -> list[Issue]:
        """Check that a value is a wikilink to a note of one of the wanted types.

        An unresolved link is only a warning: it is broken, or its note isn't
        written yet (CONVENTIONS.md section 1).

        Args:
            note: The note.
            prop: The property name.
            item: The value, or one item of a list value.
            wanted: The note types the link may point to.

        Returns:
            At most one issue.
        """
        wanted_text = " or ".join(wanted)
        target = parse_link(item)
        if target is None:
            message = f"{item!r} must be a quoted [[wikilink]] to a {wanted_text} note"
            return [self._error(note, IssueCode.NOT_A_LINK, message, prop)]
        if not target:
            return [self._error(note, IssueCode.NOT_A_LINK, f"{item!r} has no target note", prop)]
        found = self.vault.resolve(target).notes
        if not found and self.vault.private_match(target) != PrivateMatch.NONE:
            return []  # a link into Private/: validate_links reports it
        if not found:
            message = f"[[{target}]] matches no note (broken, or not written yet)"
            return [warning_issue(CHECK, IssueCode.LINK_UNRESOLVED, note.rel, message, prop=prop)]
        if len(found) > 1:
            paths = ", ".join(match.rel for match in found)
            message = f"[[{target}]] matches several notes ({paths}); use a path to pick one"
            return [self._error(note, IssueCode.LINK_AMBIGUOUS, message, prop)]
        target_type = found[0].note_type
        if target_type not in wanted:
            got = f"type {target_type!r}" if target_type else "no type"
            message = f"[[{target}]] ({found[0].rel}) has {got}, expected {wanted_text}"
            return [self._error(note, IssueCode.LINK_WRONG_TYPE, message, prop)]
        return []

    @staticmethod
    def _error(note: Note, code: IssueCode, message: str, prop: str) -> Issue:
        """Build an error against one property of a note.

        Args:
            note: The note.
            code: What kind of problem it is.
            message: What's wrong.
            prop: The property at fault.

        Returns:
            The issue.
        """
        return error_issue(CHECK, code, note.rel, message, prop=prop)


def check(vault: Vault) -> list[Issue]:
    """Check every note's frontmatter against the properties schema.

    Args:
        vault: The vault to check.

    Returns:
        Every issue found.
    """
    checker = PropertyChecker(vault)
    return [issue for note in vault.notes for issue in checker.check(note)]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the properties check from the command line.

    Args:
        argv: The arguments, without the program name; `sys.argv[1:]` when None.

    Returns:
        The exit code.
    """
    return run_cli(DESCRIPTION, check, argv)


if __name__ == "__main__":
    sys.exit(main())

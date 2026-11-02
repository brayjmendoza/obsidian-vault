"""The two schemas as typed models, parsed and cross-checked when they're loaded.

`load_schemas` is the only way in: it reads both YAML files, parses each into a
frozen, strict pydantic model, then checks the references between them (e.g.,
every vocabulary a constraint names exists). Anything wrong becomes an issue
inside a `SchemaError`, so code past the loader only ever sees valid schemas.
"""

import re
from collections.abc import Iterable, Iterator, Mapping
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Final, Literal, Self

import yaml
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    Strict,
    ValidationError,
    model_validator,
)
from pydantic_core import ErrorDetails

from vault_tools.issues import CheckName, Issue, IssueCode, error_issue

PROPERTIES_SCHEMA: Final = "properties-schema.yaml"
STRUCTURE_SCHEMA: Final = "structure-schema.yaml"

# In a structure-schema `types:` or `files:` list, "any" allows anything.
ANY: Final = "any"

# The vocabulary that must list exactly the note types under `types`.
NOTE_TYPE_VOCAB: Final = "note_type"


class SchemaError(Exception):
    """A schema file is valid YAML but breaks the schema's own rules.

    Attributes:
        issues: One `schema-error` issue per problem found.
    """

    def __init__(self, issues: list[Issue]) -> None:
        """Wrap the issues found while loading the schemas.

        Args:
            issues: The problems found, at least one.
        """
        super().__init__(f"{len(issues)} schema problem(s)")
        self.issues = issues


class ObsidianType(StrEnum):
    """The value types Obsidian's properties panel knows."""

    TEXT = "text"
    LIST = "list"
    NUMBER = "number"
    CHECKBOX = "checkbox"
    DATE = "date"
    DATETIME = "datetime"


# -- field types ----------------------------------------------------------------


def _compile_pattern(value: object) -> object:
    """Compile a regex given as text, so a bad pattern fails validation.

    Args:
        value: The raw value from the schema.

    Returns:
        The compiled pattern, or `value` unchanged when it isn't text (pydantic
        then reports the wrong type).

    Raises:
        ValueError: The text is not a valid regular expression.
    """
    if not isinstance(value, str):
        return value
    try:
        return re.compile(value)
    except re.error as exc:  # re.error isn't a ValueError, so pydantic wouldn't catch it
        raise ValueError(f"pattern does not compile: {exc}") from exc


def _check_range(value: list[int | float]) -> list[int | float]:
    """Require a range to be exactly `[min, max]` with `min <= max`.

    Args:
        value: The parsed range.

    Returns:
        The range, unchanged.

    Raises:
        ValueError: The range has the wrong length or its bounds are reversed.
    """
    if len(value) != 2 or value[0] > value[1]:
        raise ValueError("range must be [min, max] with min <= max")
    return value


def _text_as_list(value: object) -> object:
    """Let a single text value stand for a one-item list.

    Args:
        value: The raw value from the schema.

    Returns:
        `[value]` when `value` is text, otherwise `value` unchanged.
    """
    return [value] if isinstance(value, str) else value


type Regex = Annotated[re.Pattern[str], BeforeValidator(_compile_pattern)]
type NumberRange = Annotated[list[int | float], AfterValidator(_check_range)]


class SchemaModel(BaseModel):
    """Base for every model parsed from a schema file.

    Frozen, strict (no quiet conversions such as `"3"` to `3`), and closed to
    unknown keys, so a typo in a schema is an error rather than ignored. Fields
    are lists, not tuples, because strict mode won't read a YAML list as a tuple.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


# -- properties-schema.yaml -----------------------------------------------------


class Constraint(SchemaModel):
    """Value rules for one property of one note type.

    Attributes:
        vocab: Name of the vocabulary the value (or every list item) must be in.
        value_range: Inclusive `[min, max]` for numbers (`range` in the YAML).
        pattern: Regex a text value must match.
        link: Note types a quoted [[wikilink]] value must point to.
    """

    vocab: str | None = None
    value_range: NumberRange | None = Field(default=None, alias="range")
    pattern: Regex | None = None
    link: Annotated[list[str] | None, BeforeValidator(_text_as_list)] = None


class TypeRules(SchemaModel):
    """The properties a note type requires and allows, and their constraints.

    Attributes:
        required: Properties the note must have.
        optional: Properties the note may have.
        constraints: Value rules, keyed by property name.
    """

    required: list[str] = Field(default_factory=list)
    optional: list[str] = Field(default_factory=list)
    constraints: dict[str, Constraint] = Field(default_factory=dict)

    @property
    def declared(self) -> list[str]:
        """Every property this block names, required first."""
        return self.required + self.optional


class PropertiesSchema(SchemaModel):
    """properties-schema.yaml: every property, vocabulary, and note type.

    Attributes:
        version: Shared with CONVENTIONS.md and the structure schema.
        property_types: Every property name in the vault and its one Obsidian type.
        vocabularies: Named lists of allowed values.
        common: Properties every typed note gets.
        types: Per note type, the properties it requires and allows.
    """

    version: str
    property_types: dict[str, Annotated[ObsidianType, Strict(False)]]  # lax: text to enum
    vocabularies: dict[str, list[str]] = Field(default_factory=dict)
    common: TypeRules = Field(default_factory=TypeRules)
    types: dict[str, TypeRules]


# -- structure-schema.yaml ------------------------------------------------------


class DomainSchema(SchemaModel):
    """One domain under `20 Hobbies/` or `30 Life Admin/`.

    Attributes:
        items: Role folders holding one note per tracked or owned thing.
        logs: Role folders holding one note per date or period.
        plans: Role folders holding a series of standing plans.
        domains: Nested domains, with the same shape.
    """

    items: dict[str, list[str]] = Field(default_factory=dict)
    logs: dict[str, list[str]] = Field(default_factory=dict)
    plans: dict[str, list[str]] = Field(default_factory=dict)
    domains: dict[str, DomainSchema] = Field(default_factory=dict)

    @property
    def role_folders(self) -> dict[str, list[str]]:
        """Every role folder in this domain (items, then logs, then plans) and its types."""
        return self.items | self.logs | self.plans


class FolderSchema(SchemaModel):
    """One declared folder.

    Attributes:
        types: Note types allowed directly in it (`any` allows any, or none).
        files: Extensions of non-note files allowed in it (`any` allows anything).
        subfolders: Fixed subfolders, by name.
        domains: Domains it holds, by name.
        flat: Whether subfolders are forbidden.
        open: Whether any subfolders are allowed; they inherit types and files.
        max_depth: With `open`, how many levels of subfolders may sit below it.
        skip: Whether neither validator looks inside it.
    """

    types: list[str] = Field(default_factory=list)
    files: list[str] = Field(default_factory=list)
    subfolders: dict[str, FolderSchema] = Field(default_factory=dict)
    domains: dict[str, DomainSchema] = Field(default_factory=dict)
    flat: bool = False
    open: bool = False
    max_depth: int | None = Field(default=None, ge=1)
    skip: bool = False

    @model_validator(mode="after")
    def _max_depth_needs_open(self) -> Self:
        """Reject `max_depth` on a folder that isn't open.

        Returns:
            The folder, unchanged.

        Raises:
            ValueError: `max_depth` is set without `open: true`.
        """
        if self.max_depth is not None and not self.open:
            raise ValueError("max_depth only applies to open folders")
        return self


class DomainSkeleton(SchemaModel):
    """The shape every domain shares.

    Attributes:
        hub: Whether every domain needs a hub note.
        root_types: Note types allowed loose at a domain root, beside the hub.
        roles: The role keys a domain may use. Documentation only.
        role_folders_flat: Whether role folders forbid subfolders.
    """

    hub: Literal["required", "optional"] = "required"
    root_types: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    role_folders_flat: bool = True


class StructureSchema(SchemaModel):
    """structure-schema.yaml: every allowed folder and filename pattern.

    Attributes:
        version: Shared with CONVENTIONS.md and the properties schema.
        ignore: Names (or glob patterns) skipped everywhere.
        exempt: Files, relative to Public/, that neither validator checks.
        domain: The skeleton every domain follows.
        root: The top-level folders of Public/.
        filenames: Per note type, the regex its filename must match.
    """

    version: str
    ignore: list[str] = Field(default_factory=list)
    exempt: list[str] = Field(default_factory=list)
    domain: DomainSkeleton = Field(default_factory=DomainSkeleton)
    root: dict[str, FolderSchema]
    filenames: dict[str, Regex] = Field(default_factory=dict)


class Schemas(BaseModel):
    """Both schemas, parsed and consistent with each other.

    Attributes:
        properties: The properties schema.
        structure: The structure schema.
    """

    model_config = ConfigDict(frozen=True)

    properties: PropertiesSchema
    structure: StructureSchema


# -- loading --------------------------------------------------------------------


def load_schemas(schema_dir: Path) -> Schemas:
    """Read, parse, and cross-check both schemas.

    Every problem in both files is collected before raising, so one run shows
    them all.

    Args:
        schema_dir: The folder holding both schema files.

    Returns:
        The parsed schemas.

    Raises:
        OSError: A schema file can't be read.
        yaml.YAMLError: A schema file isn't valid YAML.
        SchemaError: A schema breaks its own rules or refers to something that
            doesn't exist.
    """
    issues: list[Issue] = []
    properties = _parse(PropertiesSchema, schema_dir / PROPERTIES_SCHEMA, issues)
    structure = _parse(StructureSchema, schema_dir / STRUCTURE_SCHEMA, issues)
    if properties is not None:
        issues += _schema_issues(PROPERTIES_SCHEMA, properties_problems(properties))
        if structure is not None:
            note_types = set(properties.types)
            issues += _schema_issues(STRUCTURE_SCHEMA, structure_problems(structure, note_types))
    if issues or properties is None or structure is None:
        raise SchemaError(issues)
    return Schemas(properties=properties, structure=structure)


def _parse[M: SchemaModel](model: type[M], path: Path, issues: list[Issue]) -> M | None:
    """Parse one schema file into its model.

    Args:
        model: The model to parse into.
        path: The schema file.
        issues: Where to record problems with the file's shape.

    Returns:
        The parsed schema, or None when it doesn't fit the model.

    Raises:
        OSError: The file can't be read.
        yaml.YAMLError: The file isn't valid YAML.
    """
    with path.open(encoding="utf-8") as handle:
        data: object = yaml.safe_load(handle)
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        issues += _schema_issues(path.name, (_describe(error) for error in exc.errors()))
        return None


def _describe(error: ErrorDetails) -> str:
    """Turn one pydantic error into a message naming the schema key at fault.

    Args:
        error: One entry from `ValidationError.errors()`.

    Returns:
        A message such as `types.piece.constraints.status: unknown key 'vocabb'`.
    """
    where = ".".join(str(part) for part in error["loc"]) or "top level"
    match error["type"]:
        case "extra_forbidden":
            return f"{where}: unknown key"
        case "missing":
            return f"{where}: required key is missing"
        case "value_error":
            return f"{where}: {error.get('ctx', {}).get('error', error['msg'])}"
        case _:
            return f"{where}: {error['msg']}"


def _schema_issues(schema_file: str, problems: Iterable[str]) -> list[Issue]:
    """Wrap problem messages as `schema-error` issues against one schema file.

    Args:
        schema_file: The schema file's name.
        problems: One message per problem.

    Returns:
        One issue per message.
    """
    return [
        error_issue(CheckName.SCHEMA, IssueCode.SCHEMA_ERROR, schema_file, problem)
        for problem in problems
    ]


# -- cross-references -----------------------------------------------------------


def properties_problems(schema: PropertiesSchema) -> list[str]:
    """Find references in the properties schema that point at nothing.

    Args:
        schema: The parsed properties schema.

    Returns:
        One message per problem; empty when the schema is consistent.
    """
    problems = _rule_problems("common", schema.common, set(schema.common.declared), schema)
    for name, rules in schema.types.items():
        allowed = set(rules.declared) | set(schema.common.declared)
        problems += _rule_problems(f"types.{name}", rules, allowed, schema)
    problems += _note_type_vocab_problems(schema)
    return problems


def _rule_problems(
    label: str, rules: TypeRules, allowed: set[str], schema: PropertiesSchema
) -> list[str]:
    """Check one block of type rules against the rest of the properties schema.

    Args:
        label: Where the block sits, for messages (e.g., `types.piece`).
        rules: The block.
        allowed: Every property a note of this type may carry.
        schema: The whole properties schema.

    Returns:
        One message per problem.
    """
    problems = [
        f"{label}: {prop!r} is not declared in property_types"
        for prop in rules.declared
        if prop not in schema.property_types
    ]
    for prop, constraint in rules.constraints.items():
        where = f"{label}.constraints.{prop}"
        if prop not in allowed:
            problems.append(f"{where}: {prop!r} is not a property of this type")
        if constraint.vocab is not None and constraint.vocab not in schema.vocabularies:
            problems.append(f"{where}: no vocabulary named {constraint.vocab!r}")
        problems += [
            f"{where}: link target {target!r} is not a note type"
            for target in constraint.link or []
            if target not in schema.types
        ]
    return problems


def _note_type_vocab_problems(schema: PropertiesSchema) -> list[str]:
    """Check that the note type vocabulary lists exactly the types under `types`.

    Args:
        schema: The parsed properties schema.

    Returns:
        One message per direction that differs.
    """
    listed = set(schema.vocabularies.get(NOTE_TYPE_VOCAB, []))
    defined = set(schema.types)
    problems = []
    if listed - defined:
        problems.append(
            f"vocabularies.{NOTE_TYPE_VOCAB} lists types with no entry under `types`: "
            + ", ".join(sorted(listed - defined))
        )
    if defined - listed:
        problems.append(
            f"types missing from vocabularies.{NOTE_TYPE_VOCAB}: "
            + ", ".join(sorted(defined - listed))
        )
    return problems


def structure_problems(schema: StructureSchema, note_types: set[str]) -> list[str]:
    """Find note type names in the structure schema that the properties schema lacks.

    Args:
        schema: The parsed structure schema.
        note_types: Every note type the properties schema defines.

    Returns:
        One message per unknown type name.
    """
    named = [
        ("domain.root_types", schema.domain.root_types),
        ("filenames", list(schema.filenames)),
        *_folder_type_lists("root", schema.root),
    ]
    return [
        f"{where}: {name!r} is not a note type in {PROPERTIES_SCHEMA}"
        for where, names in named
        for name in names
        if name != ANY and name not in note_types
    ]


def _folder_type_lists(
    prefix: str, folders: Mapping[str, FolderSchema]
) -> Iterator[tuple[str, list[str]]]:
    """Yield every folder's and role folder's `types` list, with where it sits.

    Args:
        prefix: The schema path of the parent, for messages.
        folders: The folders to walk.

    Yields:
        (schema path, note type names) for each folder and role folder.
    """
    for name, folder in folders.items():
        where = f"{prefix}.{name}"
        yield where, folder.types
        yield from _folder_type_lists(f"{where}.subfolders", folder.subfolders)
        yield from _domain_type_lists(f"{where}.domains", folder.domains)


def _domain_type_lists(
    prefix: str, domains: Mapping[str, DomainSchema]
) -> Iterator[tuple[str, list[str]]]:
    """Yield every role folder's `types` list in a set of domains, with where it sits.

    Args:
        prefix: The schema path of the parent, for messages.
        domains: The domains to walk.

    Yields:
        (schema path, note type names) for each role folder.
    """
    for name, domain in domains.items():
        for folder, types in domain.role_folders.items():
            yield f"{prefix}.{name}.{folder}", types
        yield from _domain_type_lists(f"{prefix}.{name}.domains", domain.domains)

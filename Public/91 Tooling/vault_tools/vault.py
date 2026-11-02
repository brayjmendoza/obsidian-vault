"""Load a vault: walk Public/, parse each note's frontmatter, and resolve [[wikilinks]].

Nothing here judges a note. It only loads things and records problems it hits
while loading (unreadable files, broken frontmatter) as issues. The validators
build on it.
"""

import datetime as dt
import fnmatch
import re
import unicodedata
from collections.abc import Iterable, Iterator, Mapping
from enum import StrEnum
from functools import cached_property
from pathlib import Path
from typing import Final, cast

import yaml
from pydantic import BaseModel, ConfigDict, SkipValidation

from vault_tools.issues import CheckName, Issue, IssueCode, error_issue
from vault_tools.markup import NOTE_SUFFIX, clean_target
from vault_tools.schemas import FolderSchema, PropertiesSchema, StructureSchema, load_schemas

PACKAGE_DIR: Final = Path(__file__).resolve().parent  # 91 Tooling/vault_tools/
TOOLING_DIR: Final = PACKAGE_DIR.parent  # 91 Tooling/
DEFAULT_SCHEMA_DIR: Final = TOOLING_DIR / "schemas"
DEFAULT_VAULT_ROOT: Final = TOOLING_DIR.parent  # Public/
PRIVATE_DIR_NAME: Final = "Private"  # beside Public/, at the repository root
CONVENTIONS_PATH: Final = "90 System/Claude/CONVENTIONS.md"

# Folders marked `skip: true` in structure-schema.yaml are never validated, but
# properties-schema.yaml says archived notes still count as link targets.
LINK_TARGET_SKIP_FOLDERS: Final = frozenset({"99 Archive"})

# Folders where a note may have no `type` (CONVENTIONS.md section 4).
UNTYPED_ALLOWED_FOLDERS: Final = frozenset({"00 Inbox", "98 Attachments"})

PROPERTY_LINK_RE: Final = re.compile(r"^\s*\[\[([^\[\]]*)\]\]\s*$")
BYTE_ORDER_MARK: Final = "\ufeff"

type YamlValue = (
    str | int | float | bool | dt.date | dt.datetime | list[YamlValue] | dict[str, YamlValue] | None
)
type Properties = dict[str, YamlValue]


def nfc(text: str) -> str:
    """Normalize text to NFC.

    macOS stores filenames decomposed (NFD), while YAML text is usually NFC, so
    names are compared only after normalizing.

    Args:
        text: Any text.

    Returns:
        The NFC form of `text`.
    """
    return unicodedata.normalize("NFC", text)


def link_key(text: str) -> str:
    """Normalize a link target for lookup: NFC and case-folded, as Obsidian matches.

    Args:
        text: A note name, alias, or path.

    Returns:
        The lookup key.
    """
    return nfc(text).casefold()


def folder_containing(rel: str, folders: Iterable[str]) -> str | None:
    """Find which of `folders` holds a path.

    Args:
        rel: A path relative to Public/.
        folders: Folder paths relative to Public/.

    Returns:
        The first folder that is `rel` or contains it, or None.
    """
    return next((f for f in folders if rel == f or rel.startswith(f + "/")), None)


# -- frontmatter ----------------------------------------------------------------


class Frontmatter(BaseModel):
    """What a note's frontmatter block parsed to.

    Attributes:
        properties: The properties, or None when the note has no frontmatter or
            it is broken.
        error: Why the frontmatter is broken, if it is.
        body: The text after the frontmatter (the whole note when there is none).
        body_line: The 1-based line of the note the body starts on.
    """

    model_config = ConfigDict(frozen=True)

    # Frontmatter values are the validator's to judge, so pydantic leaves them alone.
    properties: SkipValidation[Properties | None] = None
    error: str | None = None
    body: str = ""
    body_line: int = 1


def parse_frontmatter(text: str) -> Frontmatter:
    """Parse the frontmatter at the top of a note.

    Obsidian only treats a block as frontmatter when `---` is the very first
    line and a closing `---` (or `...`) line follows.

    Args:
        text: The whole note.

    Returns:
        The parsed frontmatter.
    """
    text = text.lstrip(BYTE_ORDER_MARK)
    lines = text.splitlines()
    if not lines or lines[0].rstrip() != "---":
        return Frontmatter(body=text)
    for index, line in enumerate(lines[1:], start=1):
        if line.rstrip() in {"---", "..."}:
            body = "\n".join(lines[index + 1 :])
            return _parse_block("\n".join(lines[1:index]), body, body_line=index + 2)
    return Frontmatter(error="frontmatter starts with --- but is never closed", body=text)


def _parse_block(block: str, body: str, *, body_line: int) -> Frontmatter:
    """Parse the YAML between a note's `---` lines.

    Args:
        block: The frontmatter text, without the `---` lines.
        body: The rest of the note.
        body_line: The line of the note the body starts on.

    Returns:
        The parsed frontmatter, empty properties for an empty block.
    """
    try:
        value: object = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        return Frontmatter(error=_yaml_error_message(exc), body=body, body_line=body_line)
    if value is None:
        return Frontmatter(properties={}, body=body, body_line=body_line)
    if not isinstance(value, dict):
        message = "frontmatter must be a set of `name: value` properties"
        return Frontmatter(error=message, body=body, body_line=body_line)
    # safe_load builds only YamlValue types from plain YAML like Obsidian's.
    properties = cast(Properties, {str(k): v for k, v in value.items()})
    return Frontmatter(properties=properties, body=body, body_line=body_line)


def _yaml_error_message(exc: yaml.YAMLError) -> str:
    """Describe a YAML error, with the frontmatter line when PyYAML knows it.

    Args:
        exc: The error PyYAML raised.

    Returns:
        A one-line message.
    """
    if not isinstance(exc, yaml.MarkedYAMLError):
        return f"frontmatter is not valid YAML: {exc}"
    mark = exc.problem_mark
    where = f" (frontmatter line {mark.line + 1})" if mark is not None else ""
    return f"frontmatter is not valid YAML{where}: {exc.problem or exc}"


# -- notes ----------------------------------------------------------------------


class Note(BaseModel):
    """One Markdown note and its parsed frontmatter.

    Attributes:
        path: The absolute path.
        rel: The POSIX path relative to Public/, NFC-normalized.
        properties: The frontmatter, or None when it is missing or broken.
        body: The text after the frontmatter.
        body_line: The 1-based line of the note the body starts on.
        load_issues: Problems hit while loading (unreadable file, broken frontmatter).
    """

    model_config = ConfigDict(frozen=True)

    path: Path
    rel: str
    properties: SkipValidation[Properties | None] = None
    body: str = ""
    body_line: int = 1
    load_issues: tuple[Issue, ...] = ()

    @property
    def stem(self) -> str:
        """The filename without `.md`, NFC-normalized."""
        return nfc(self.path.stem)

    @property
    def top_folder(self) -> str | None:
        """The top-level folder it sits in, or None for a note at the root of Public/."""
        parts = self.rel.split("/")
        return parts[0] if len(parts) > 1 else None

    def file_line(self, body_line: int) -> int:
        """Turn a line number within the body into a line number within the file.

        Args:
            body_line: A 1-based line number counted from the start of the body.

        Returns:
            The 1-based line number in the note's file.
        """
        return self.body_line + body_line - 1

    @property
    def note_type(self) -> YamlValue:
        """The `type` property as written, or None."""
        return (self.properties or {}).get("type")

    @property
    def aliases(self) -> list[str]:
        """The `aliases` property's text values; a single text value counts as one alias."""
        value = (self.properties or {}).get("aliases")
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [alias for alias in value if isinstance(alias, str)]
        return []


def load_note(path: Path, root: Path) -> Note:
    """Read a note and parse its frontmatter.

    Args:
        path: The note's absolute path.
        root: The Public/ folder it sits in.

    Returns:
        The note. Problems reading or parsing it are in `load_issues`.
    """
    rel = nfc(path.relative_to(root).as_posix())
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        issue = error_issue(
            CheckName.PROPERTIES, IssueCode.READ_ERROR, rel, f"could not read note: {exc}"
        )
        return Note(path=path, rel=rel, load_issues=(issue,))
    frontmatter = parse_frontmatter(text)
    if frontmatter.error is not None:
        issue = error_issue(
            CheckName.PROPERTIES, IssueCode.FRONTMATTER_INVALID, rel, frontmatter.error
        )
        return Note(path=path, rel=rel, load_issues=(issue,))
    return Note(
        path=path,
        rel=rel,
        properties=frontmatter.properties,
        body=frontmatter.body,
        body_line=frontmatter.body_line,
    )


# -- links ----------------------------------------------------------------------


def parse_link(value: YamlValue) -> str | None:
    """Extract the target of a property value that is a single wikilink.

    `"[[Target#Heading|Text]]"` gives `"Target"`: headings, block references,
    display text, and a trailing `.md` are dropped.

    Args:
        value: A property value.

    Returns:
        The target, or None when the value isn't exactly one wikilink.
    """
    if not isinstance(value, str):
        return None
    match = PROPERTY_LINK_RE.match(value)
    return clean_target(match.group(1)) if match else None


class Resolution(BaseModel):
    """The notes a link target matched.

    Attributes:
        notes: Every distinct match; empty when nothing matched.
    """

    model_config = ConfigDict(frozen=True)

    notes: list[Note]

    @property
    def unique(self) -> Note | None:
        """The match, when there is exactly one."""
        return self.notes[0] if len(self.notes) == 1 else None


class PrivateMatch(StrEnum):
    """Whether a link target points into Private/."""

    NONE = "none"  # not into Private/, as far as can be told
    PRIVATE = "private"  # a path into Private/, or a name only Private/ has
    AMBIGUOUS = "ambiguous"  # a name both Public/ and Private/ have


class _NoteScan(BaseModel):
    """Every note found under Public/, split by whether it is checked.

    Attributes:
        checked: Notes the properties validator checks.
        archived: Notes in skipped folders that still count as link targets.
        file_keys: Link keys of the other files links may embed (e.g., `scan.png`).
    """

    model_config = ConfigDict(frozen=True)

    checked: list[Note]
    archived: list[Note]
    file_keys: frozenset[str]


class _LinkIndex(BaseModel):
    """Link targets indexed the three ways Obsidian looks them up.

    Attributes:
        by_name: Notes by filename key.
        by_alias: Notes by alias key.
        by_path: Notes by path key, relative to Public/ and without `.md`.
    """

    model_config = ConfigDict(frozen=True)

    by_name: dict[str, list[Note]]
    by_alias: dict[str, list[Note]]
    by_path: dict[str, Note]


# -- the vault ------------------------------------------------------------------


class Vault:
    """A Public/ folder plus the schemas it is judged by.

    Notes are loaded and indexed lazily, the first time they're needed.

    Attributes:
        root: The Public/ folder.
        schema_dir: The folder holding both schemas.
        private_dir: The Private/ folder, when it can be seen. Only its file
            names are ever read, never its files.
        properties_schema: The parsed properties schema.
        structure_schema: The parsed structure schema.
    """

    def __init__(
        self,
        root: Path | str = DEFAULT_VAULT_ROOT,
        schema_dir: Path | str = DEFAULT_SCHEMA_DIR,
        private_dir: Path | str | None = None,
    ) -> None:
        """Load the schemas for a vault.

        Args:
            root: The Public/ folder to check.
            schema_dir: The folder holding both schema files.
            private_dir: The Private/ folder. When None, `Private/` beside
                `root` is used if it exists (on your Mac and in CI, never in
                Claude's runs).

        Raises:
            OSError: A schema file can't be read.
            yaml.YAMLError: A schema file isn't valid YAML.
            vault_tools.schemas.SchemaError: A schema breaks its own rules.
        """
        self.root = Path(root).resolve()
        self.schema_dir = Path(schema_dir).resolve()
        self.private_dir = _find_private_dir(self.root, private_dir)
        schemas = load_schemas(self.schema_dir)
        self.properties_schema: PropertiesSchema = schemas.properties
        self.structure_schema: StructureSchema = schemas.structure
        self._exempt = frozenset(nfc(path) for path in schemas.structure.exempt)
        self._has_files: dict[Path, bool] = {}

    # -- walking --------------------------------------------------------------

    def is_ignored(self, name: str) -> bool:
        """Check a file or folder name against the schema's `ignore` list.

        Args:
            name: A file or folder name.

        Returns:
            Whether an `ignore` entry (an exact name or a glob) matches it.
        """
        return any(fnmatch.fnmatchcase(name, pattern) for pattern in self.structure_schema.ignore)

    def is_exempt(self, rel: str) -> bool:
        """Check whether a file is on the schema's `exempt` list.

        Args:
            rel: A path relative to Public/.

        Returns:
            Whether neither validator checks the file.
        """
        return rel in self._exempt

    def _listing(self, directory: Path) -> list[Path]:
        """List a folder's entries in name order, without ignored names.

        Args:
            directory: The folder.

        Returns:
            Its files and folders, empty folders included.
        """
        entries = sorted(directory.iterdir(), key=lambda path: path.name)
        return [entry for entry in entries if not self.is_ignored(entry.name)]

    def has_files(self, directory: Path) -> bool:
        """Check whether a folder holds any file, at any depth, that isn't ignored.

        Git tracks files, not folders, so a folder without one doesn't exist in
        the repository or in CI's checkout. Treating it as absent keeps a local
        run's results the same as CI's.

        Args:
            directory: The folder.

        Returns:
            Whether git would see the folder.
        """
        if directory not in self._has_files:
            self._has_files[directory] = any(
                not entry.is_dir() or self.has_files(entry) for entry in self._listing(directory)
            )
        return self._has_files[directory]

    def children(self, directory: Path) -> list[Path]:
        """List a folder's entries as git sees them: in name order, without ignored names.

        Folders that hold no files are left out (see `has_files`).

        Args:
            directory: The folder.

        Returns:
            Its files and the subfolders that hold files.
        """
        return [
            entry
            for entry in self._listing(directory)
            if not entry.is_dir() or self.has_files(entry)
        ]

    def iter_paths(self, start: Path | None = None) -> Iterator[Path]:
        """Walk every file and folder below a folder, depth first, skipping ignored names.

        Args:
            start: Where to start; Public/ when None.

        Yields:
            Each file and folder, a folder before its contents.
        """
        for child in self.children(start or self.root):
            yield child
            if child.is_dir():
                yield from self.iter_paths(child)

    def rel(self, path: Path) -> str:
        """Express a path relative to Public/.

        Args:
            path: An absolute path inside Public/.

        Returns:
            The POSIX path relative to Public/, NFC-normalized.
        """
        return nfc(path.relative_to(self.root).as_posix())

    @cached_property
    def skipped_folders(self) -> frozenset[str]:
        """Paths, relative to Public/, of the folders marked `skip: true`."""
        return frozenset(_skipped_folders("", self.structure_schema.root))

    @cached_property
    def _scan(self) -> _NoteScan:
        """Load every note under Public/ once."""
        archived_folders = self.skipped_folders & LINK_TARGET_SKIP_FOLDERS
        checked: list[Note] = []
        archived: list[Note] = []
        file_keys: set[str] = set()
        for path in self.iter_paths():
            if not path.is_file():
                continue
            rel = self.rel(path)
            archived_file = folder_containing(rel, archived_folders) is not None
            if not archived_file and folder_containing(rel, self.skipped_folders):
                continue
            if path.suffix.lower() != NOTE_SUFFIX:
                file_keys.add(link_key(path.name))
            elif self.is_exempt(rel):
                continue
            elif archived_file:
                archived.append(load_note(path, self.root))
            else:
                checked.append(load_note(path, self.root))
        return _NoteScan(checked=checked, archived=archived, file_keys=frozenset(file_keys))

    @property
    def notes(self) -> list[Note]:
        """Every note the properties validator checks.

        Excludes exempt files and every note under a `skip: true` folder.
        """
        return self._scan.checked

    @property
    def link_targets(self) -> list[Note]:
        """Every note a link may resolve to: `notes` plus 99 Archive/."""
        return self._scan.checked + self._scan.archived

    # -- links ----------------------------------------------------------------

    @cached_property
    def _link_index(self) -> _LinkIndex:
        """Index every link target by name, alias, and path."""
        by_name: dict[str, list[Note]] = {}
        by_alias: dict[str, list[Note]] = {}
        by_path: dict[str, Note] = {}
        for note in self.link_targets:
            by_name.setdefault(link_key(note.stem), []).append(note)
            by_path[link_key(note.rel[: -len(NOTE_SUFFIX)])] = note
            for alias in note.aliases:
                by_alias.setdefault(link_key(alias), []).append(note)
        return _LinkIndex(by_name=by_name, by_alias=by_alias, by_path=by_path)

    def resolve(self, target: str) -> Resolution:
        """Resolve a link target the way Obsidian does.

        A target with a `/` is a path from Public/. A bare name matches a
        filename first, then an alias. Matching ignores case.

        Args:
            target: A link target, already stripped of `#`, `^`, and `|` parts.

        Returns:
            Every distinct note it matches.
        """
        index = self._link_index
        key = link_key(target.strip("/"))
        if "/" in key:
            note = index.by_path.get(key)
            return Resolution(notes=[note] if note else [])
        matches = index.by_name.get(key) or index.by_alias.get(key) or []
        distinct = {note.rel: note for note in matches}
        return Resolution(notes=list(distinct.values()))

    # -- Private/ -------------------------------------------------------------

    @cached_property
    def _private_keys(self) -> frozenset[str] | None:
        """Link keys of every file in Private/: full names, plus note names without `.md`.

        Only names are read. CI can see them because git-crypt encrypts file
        contents, not names; aliases live in encrypted frontmatter, so they
        aren't known.
        """
        if self.private_dir is None:
            return None
        keys: set[str] = set()
        for path in self.iter_paths(self.private_dir):
            if path.is_file():
                keys.add(link_key(path.name))
                if path.suffix.lower() == NOTE_SUFFIX:
                    keys.add(link_key(path.stem))
        return frozenset(keys)

    def private_match(self, target: str) -> PrivateMatch:
        """Tell whether a link target points into Private/.

        A path starting `Private/` always does, even when Private/ can't be
        seen. A bare name is judged only when Private/ can be seen: it points
        there when only Private/ has it, and is ambiguous when both folders do.

        Args:
            target: A link target, already stripped of `#`, `^`, and `|` parts.

        Returns:
            The match.
        """
        key = link_key(target.strip("/"))
        private = link_key(PRIVATE_DIR_NAME)
        if key == private or key.startswith(private + "/"):
            return PrivateMatch.PRIVATE
        if "/" in key or self._private_keys is None or key not in self._private_keys:
            return PrivateMatch.NONE
        in_public = bool(self.resolve(target).notes) or key in self._scan.file_keys
        return PrivateMatch.AMBIGUOUS if in_public else PrivateMatch.PRIVATE


def _find_private_dir(root: Path, private_dir: Path | str | None) -> Path | None:
    """Locate the Private/ folder for a vault.

    Args:
        root: The Public/ folder.
        private_dir: An explicit Private/ folder, or None to look beside `root`.

    Returns:
        The folder, or None when there isn't one to see.
    """
    candidate = Path(private_dir) if private_dir is not None else root.parent / PRIVATE_DIR_NAME
    return candidate.resolve() if candidate.is_dir() else None


def _skipped_folders(prefix: str, folders: Mapping[str, FolderSchema]) -> Iterator[str]:
    """Yield the paths of folders marked `skip: true`, at any depth.

    Args:
        prefix: The parent's path relative to Public/ ("" for Public/ itself).
        folders: The folders to walk.

    Yields:
        Each skipped folder's path relative to Public/, NFC-normalized.
    """
    for name, folder in folders.items():
        path = f"{prefix}/{name}" if prefix else name
        if folder.skip:
            yield nfc(path)
        yield from _skipped_folders(path, folder.subfolders)

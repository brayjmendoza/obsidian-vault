"""Enforce structure-schema.yaml on the layout of Public/.

Checks: every folder is declared (or sits under an open folder, within its
max_depth); flat folders have no subfolders; every note's type is allowed in
its folder; filenames match their type's pattern; every domain has a hub,
and its only documentation note is its About page;
non-note files appear only where their extension is allowed. Scratch notes
may sit in any folder under any name; only a domain's hub and About names
are reserved.

    vault-validate-structure [PUBLIC_DIR] [--json]
    python -m vault_tools.validate_structure
"""

import sys
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue
from vault_tools.markup import NOTE_SUFFIX
from vault_tools.schemas import (
    ANY,
    STRUCTURE_SCHEMA,
    DomainSchema,
    DomainSkeleton,
    FolderSchema,
    StructureSchema,
)
from vault_tools.vault import Vault, is_scratch, load_note, nfc

DESCRIPTION: Final = "Enforce structure-schema.yaml on the layout of Public/."
CHECK: Final = CheckName.STRUCTURE
HUB_TYPE: Final = "hub"
ABOUT_NAME: Final = "About"
ABOUT_TYPE: Final = "documentation"


class FolderSpec(BaseModel):
    """The rules for one folder, with domain and open-folder rules worked out.

    Attributes:
        path: The folder relative to Public/ ("" for Public/ itself).
        types: Note types allowed directly in it; None allows any type, or none.
        files: Extensions of non-note files allowed in it; None allows any.
        flat: Whether subfolders are forbidden.
        open: Whether undeclared subfolders are allowed; they inherit these rules.
        max_depth: With `open`, how many levels of subfolders may sit below it.
        skip: Whether to skip it entirely.
        domain: Whether it is a domain, which needs a hub.
        subfolders: Declared subfolders, by NFC name.
        open_depth: For a folder inside an open one, how many levels below it sits.
    """

    model_config = ConfigDict(frozen=True)

    path: str
    types: frozenset[str] | None = frozenset()
    files: frozenset[str] | None = frozenset()
    flat: bool = False
    open: bool = False
    max_depth: int | None = None
    skip: bool = False
    domain: bool = False
    subfolders: dict[str, FolderSpec] = Field(default_factory=dict)
    open_depth: int = 0

    @property
    def name(self) -> str:
        """The folder's own name."""
        return self.path.rsplit("/", 1)[-1]

    @property
    def label(self) -> str:
        """The folder as messages show it, e.g. `10 Projects/`."""
        return f"{self.path}/" if self.path else "Public/"


# -- building the folder tree ---------------------------------------------------


def _any_or(values: list[str]) -> frozenset[str] | None:
    """Read a `types:` or `files:` list, where `any` allows anything.

    Args:
        values: The list from the schema.

    Returns:
        None when the list holds `any`, otherwise the values as a set.
    """
    return None if ANY in values else frozenset(values)


def build_tree(schema: StructureSchema) -> FolderSpec:
    """Turn the structure schema into a tree of folder rules, rooted at Public/.

    Args:
        schema: The parsed structure schema.

    Returns:
        The rules for Public/ itself, with every declared folder below it.
    """
    subfolders = {
        nfc(name): _folder_spec(name, folder, schema.domain) for name, folder in schema.root.items()
    }
    return FolderSpec(path="", subfolders=subfolders)


def _folder_spec(path: str, folder: FolderSchema, skeleton: DomainSkeleton) -> FolderSpec:
    """Build the rules for one declared folder and everything below it.

    Args:
        path: The folder relative to Public/.
        folder: Its schema entry.
        skeleton: The shape every domain shares.

    Returns:
        The folder's rules.
    """
    subfolders = {
        nfc(name): _folder_spec(f"{path}/{name}", sub, skeleton)
        for name, sub in folder.subfolders.items()
    }
    subfolders |= {
        nfc(name): _domain_spec(f"{path}/{name}", domain, skeleton)
        for name, domain in folder.domains.items()
    }
    return FolderSpec(
        path=path,
        types=_any_or(folder.types),
        files=_any_or(folder.files),
        flat=folder.flat,
        open=folder.open,
        max_depth=folder.max_depth,
        skip=folder.skip,
        subfolders=subfolders,
    )


def _domain_spec(path: str, domain: DomainSchema, skeleton: DomainSkeleton) -> FolderSpec:
    """Build the rules for a domain: its root, role folders, and nested domains.

    Args:
        path: The domain folder relative to Public/.
        domain: Its schema entry.
        skeleton: The shape every domain shares.

    Returns:
        The domain's rules.
    """
    subfolders = {
        nfc(name): FolderSpec(
            path=f"{path}/{name}", types=_any_or(types), flat=skeleton.role_folders_flat
        )
        for name, types in domain.role_folders.items()
    }
    subfolders |= {
        nfc(name): _domain_spec(f"{path}/{name}", sub, skeleton)
        for name, sub in domain.domains.items()
    }
    return FolderSpec(
        path=path, types=frozenset(skeleton.root_types), domain=True, subfolders=subfolders
    )


# -- walking --------------------------------------------------------------------


class StructureChecker:
    """Walks Public/ and compares what's there with the folder rules."""

    def __init__(self, vault: Vault) -> None:
        """Build the folder rules from the vault's structure schema.

        Args:
            vault: The vault to check.
        """
        self.vault = vault
        self.root = build_tree(vault.structure_schema)
        self.patterns = vault.structure_schema.filenames
        self.hub_required = vault.structure_schema.domain.hub == "required"
        self.about_allowed = vault.structure_schema.domain.about == "optional"

    def run(self) -> list[Issue]:
        """Check the whole vault.

        Returns:
            Every issue found.
        """
        return list(self._walk(self.vault.root, self.root))

    def _walk(self, directory: Path, spec: FolderSpec) -> Iterator[Issue]:
        """Check a folder and everything below it.

        Args:
            directory: The folder on disk.
            spec: Its rules.

        Yields:
            Each issue found.
        """
        children = self.vault.children(directory)
        if spec.domain and self.hub_required:
            names = {nfc(child.name) for child in children if child.is_file()}
            if f"{spec.name}{NOTE_SUFFIX}" not in names:
                message = f"domain {spec.name!r} has no hub note {spec.name}{NOTE_SUFFIX}"
                yield _error(IssueCode.MISSING_HUB, spec.path + "/", message)
        for child in children:
            rel = self.vault.rel(child)
            if child.is_dir():
                yield from self._check_subfolder(child, rel, spec)
            elif self.vault.is_exempt(rel):
                continue
            elif child.suffix.lower() == NOTE_SUFFIX:
                yield from self._check_note(child, rel, spec)
            else:
                yield from self._check_file(child, rel, spec)

    def _check_subfolder(self, child: Path, rel: str, spec: FolderSpec) -> Iterator[Issue]:
        """Check that a subfolder is allowed, then walk it.

        Args:
            child: The subfolder on disk.
            rel: Its path relative to Public/.
            spec: The rules of the folder it sits in.

        Yields:
            Each issue found in or about the subfolder.
        """
        sub = spec.subfolders.get(nfc(child.name))
        if sub is not None:
            if not sub.skip:
                yield from self._walk(child, sub)
        elif spec.open:
            depth = spec.open_depth + 1
            if spec.max_depth is not None and depth > spec.max_depth:
                top = rel.rsplit("/", depth)[0]
                message = f"folders may sit at most {spec.max_depth} level(s) below {top}/"
                yield _error(IssueCode.TOO_DEEP, rel + "/", message)
            else:
                inherited = spec.model_copy(
                    update={"path": rel, "open_depth": depth, "subfolders": {}}
                )
                yield from self._walk(child, inherited)
        elif spec.flat:
            message = f"{spec.label} is flat: no subfolders allowed"
            yield _error(IssueCode.NOT_FLAT, rel + "/", message)
        else:
            message = f"folder is not declared in {STRUCTURE_SCHEMA}"
            yield _error(IssueCode.UNDECLARED_FOLDER, rel + "/", message)

    def _check_file(self, path: Path, rel: str, spec: FolderSpec) -> Iterator[Issue]:
        """Check that a non-note file's extension is allowed in its folder.

        Args:
            path: The file on disk.
            rel: Its path relative to Public/.
            spec: The rules of its folder.

        Yields:
            An issue when the extension isn't allowed.
        """
        extension = path.suffix.lower().lstrip(".")
        if spec.files is None or (extension and extension in spec.files):
            return
        allowed = ", ".join(sorted(spec.files)) or "none"
        message = f"non-note file not allowed in {spec.label} (allowed extensions: {allowed})"
        yield _error(IssueCode.FILE_NOT_ALLOWED, rel, message)

    def _check_note(self, path: Path, rel: str, spec: FolderSpec) -> Iterator[Issue]:
        """Check that a note's type belongs in its folder and its filename fits its type.

        A note with a missing or malformed type is left to the properties
        validator, except where no notes may sit at all. A scratch note is
        never checked, unless it takes the name of its domain's hub or About page.

        Args:
            path: The note on disk.
            rel: Its path relative to Public/.
            spec: The rules of its folder.

        Yields:
            Each issue found.
        """
        note = load_note(path, self.vault.root)
        note_type = None if note.load_issues else note.note_type
        if spec.domain and note.stem == spec.name:
            if note_type != HUB_TYPE:
                got = f"type {note_type!r}" if note_type else "no type"
                message = f"the domain hub must have type 'hub', not {got}"
                yield _error(IssueCode.HUB_WRONG_TYPE, rel, message)
            return
        if spec.domain and self.about_allowed and note.stem == ABOUT_NAME:
            if note_type != ABOUT_TYPE:
                got = f"type {note_type!r}" if note_type else "no type"
                message = f"a domain's About page must have type {ABOUT_TYPE!r}, not {got}"
                yield _error(IssueCode.ABOUT_WRONG_TYPE, rel, message)
            return
        if is_scratch(note):
            return
        if not isinstance(note_type, str):
            if note_type is None and spec.types is not None and not spec.types:
                message = f"no notes belong directly in {spec.label}"
                yield _error(IssueCode.TYPE_NOT_ALLOWED, rel, message)
            return
        if spec.types is not None:
            if note_type == HUB_TYPE and spec.domain:
                message = f"a hub must be named after its domain: {spec.name}{NOTE_SUFFIX}"
                yield _error(IssueCode.HUB_MISNAMED, rel, message)
                return
            if note_type == ABOUT_TYPE and spec.domain and self.about_allowed:
                message = f"a domain's documentation note must be named {ABOUT_NAME}{NOTE_SUFFIX}"
                yield _error(IssueCode.ABOUT_MISNAMED, rel, message)
                return
            if note_type not in spec.types:
                yield _error(IssueCode.TYPE_NOT_ALLOWED, rel, _not_allowed_message(note_type, spec))
        pattern = self.patterns.get(note_type)
        if pattern is not None and not pattern.search(note.stem):
            message = f"a {note_type} note's filename must match {pattern.pattern}"
            yield _error(IssueCode.FILENAME_MISMATCH, rel, message)


def _not_allowed_message(note_type: str, spec: FolderSpec) -> str:
    """Explain why a note type doesn't belong in a folder.

    Args:
        note_type: The note's type.
        spec: The folder's rules, which list allowed types.

    Returns:
        The message, listing what is allowed.
    """
    if not spec.types:
        return f"no notes belong directly in {spec.label}"
    allowed = ", ".join(sorted(spec.types))
    return f"type {note_type!r} doesn't belong in {spec.label} (allowed: {allowed})"


def _error(code: IssueCode, path: str, message: str) -> Issue:
    """Build a structure error.

    Args:
        code: What kind of problem it is.
        path: Where, relative to Public/ (folders end with `/`).
        message: What's wrong.

    Returns:
        The issue.
    """
    return error_issue(CHECK, code, path, message)


def check(vault: Vault) -> list[Issue]:
    """Check the layout of Public/ against the structure schema.

    Args:
        vault: The vault to check.

    Returns:
        Every issue found.
    """
    return StructureChecker(vault).run()


def main(argv: Sequence[str] | None = None) -> int:
    """Run the structure check from the command line.

    Args:
        argv: The arguments, without the program name; `sys.argv[1:]` when None.

    Returns:
        The exit code.
    """
    return run_cli(DESCRIPTION, check, argv)


if __name__ == "__main__":
    sys.exit(main())

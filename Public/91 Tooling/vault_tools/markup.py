"""Find links and URLs in note text, the way Obsidian reads Markdown.

Code is never a link: fenced code blocks and inline code spans are blanked out
before anything is searched, so examples such as `[[Note]]` in backticks are
ignored. Blanking keeps every newline, so line numbers stay right.
"""

import posixpath
import re
import unicodedata
from typing import Final
from urllib.parse import unquote, urlsplit

from pydantic import BaseModel, ConfigDict, Field

NOTE_SUFFIX: Final = ".md"
WEB_SCHEMES: Final = frozenset({"http", "https"})

FENCE_RE: Final = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE_RE: Final = re.compile(r"(`+)[^\n]+?\1")
WIKILINK_RE: Final = re.compile(r"!?\[\[([^\[\]\n]*)\]\]")
MARKDOWN_LINK_RE: Final = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^)\s]+)(?:\s+\"[^\"\n]*\")?\s*\)"
)
URL_RE: Final = re.compile(r"https?://[^\s<>\"'`()\[\]]+", re.IGNORECASE)
SCHEME_RE: Final = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
# Obsidian: `#` at the start of a line or after whitespace, then letters, digits,
# `_`, `-`, or `/`. So `C#`, `[[Note#Heading]]`, `url/#anchor`, and `# Heading` aren't tags.
TAG_RE: Final = re.compile(r"(?<!\S)#([\w/-]+)")
HEADING_RE: Final = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
BLOCK_ID_RE: Final = re.compile(r"(?:^|\s)\^([A-Za-z0-9-]+)[ \t]*$")
# Characters Obsidian drops from a heading when it links to it.
HEADING_DROPPED_RE: Final = re.compile(r"[#|^:%\[\]\\`*]+")


class Anchor(BaseModel):
    """The part of a link after the note: a chain of headings, or a block.

    Attributes:
        headings: Headings from outer to inner (`#Section#Subsection`).
        block: A block ID (`#^abc123`), without its `^`.
    """

    model_config = ConfigDict(frozen=True)

    headings: list[str] = Field(default_factory=list)
    block: str | None = None

    @property
    def text(self) -> str:
        """The anchor as written after the note name, e.g. `#Section#Sub` or `#^abc`."""
        parts = [f"#{heading}" for heading in self.headings]
        if self.block is not None:
            parts.append(f"#^{self.block}")
        return "".join(parts)


class Link(BaseModel):
    """A link found in note text.

    Attributes:
        target: The note or file it names, without `.md`; empty for the same note.
        anchor: The heading or block it points into, if any.
        shown: The link as messages should show it.
        line: The 1-based line it is on, within the searched text.
    """

    model_config = ConfigDict(frozen=True)

    target: str
    anchor: Anchor = Field(default_factory=Anchor)
    shown: str
    line: int = 1


class Heading(BaseModel):
    """A heading in a note body.

    Attributes:
        level: 1 for `#`, up to 6 for `######`.
        key: The heading text as a link matches it (see `heading_key`).
    """

    model_config = ConfigDict(frozen=True)

    level: int
    key: str


class Found(BaseModel):
    """Something found in a piece of text.

    Attributes:
        text: The link target or URL.
        line: The 1-based line it is on, within the searched text.
    """

    model_config = ConfigDict(frozen=True)

    text: str
    line: int


def blank_fences(text: str) -> str:
    """Empty every line of every fenced code block, keeping the line count.

    Args:
        text: Markdown text.

    Returns:
        The same text with fenced code removed, the same number of lines long.
    """
    lines = text.split("\n")
    fence: str | None = None
    for index, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if fence is None and match:
            fence = match.group(1)
            lines[index] = ""
        elif fence is not None:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            lines[index] = ""
    return "\n".join(lines)


def blank_code(text: str) -> str:
    """Replace fenced code blocks and inline code with spaces, keeping every newline.

    Args:
        text: Markdown text.

    Returns:
        The same text with code blanked out, the same number of lines long.
    """
    return INLINE_CODE_RE.sub(lambda match: " " * len(match.group(0)), blank_fences(text))


def clean_target(raw: str) -> str:
    """Reduce a wikilink's inside to its target note.

    `Target#Heading^block|Text` gives `Target`; a trailing `.md` is dropped.

    Args:
        raw: The text between `[[` and `]]`.

    Returns:
        The target, possibly empty.
    """
    target = raw.split("|", 1)[0]
    target = re.split(r"[#^]", target, maxsplit=1)[0].strip()
    return target[: -len(NOTE_SUFFIX)] if target.lower().endswith(NOTE_SUFFIX) else target


def _line_of(text: str, index: int) -> int:
    """Count which line a character offset falls on.

    Args:
        text: The searched text.
        index: A character offset into it.

    Returns:
        The 1-based line number.
    """
    return text.count("\n", 0, index) + 1


def parse_anchor(text: str) -> Anchor:
    """Read the part of a link after its first `#`.

    Args:
        text: For example `Section#Subsection` or `^abc123`.

    Returns:
        The anchor.
    """
    parts = [part.strip() for part in text.split("#")]
    block = parts.pop()[1:].strip() if parts and parts[-1].startswith("^") else None
    return Anchor(headings=[part for part in parts if part], block=block or None)


def parse_wikilink(inner: str, *, line: int = 1) -> Link:
    """Split the inside of a wikilink into target and anchor.

    Display text is dropped, including after an escaped `\\|` in a table.
    `[[Note^abc]]` is read like `[[Note#^abc]]`.

    Args:
        inner: The text between `[[` and `]]`.
        line: The line it is on.

    Returns:
        The link.
    """
    inner = inner.replace("\\|", "|").split("|", 1)[0]
    target, has_anchor, anchor_text = inner.partition("#")
    target, has_block, block = target.partition("^")
    anchor = parse_anchor(anchor_text) if has_anchor else Anchor()
    if has_block and anchor.block is None:
        anchor = Anchor(headings=anchor.headings, block=block.strip() or None)
    return Link(target=clean_target(target), anchor=anchor, shown=f"[[{inner}]]", line=line)


def wikilinks(text: str) -> list[Link]:
    """Find every wikilink and embed in text.

    Args:
        text: Text with code already blanked out.

    Returns:
        Each link, same-note links (`[[#Heading]]`) included; empty `[[]]` left out.
    """
    links = [
        parse_wikilink(match.group(1), line=_line_of(text, match.start()))
        for match in WIKILINK_RE.finditer(text)
    ]
    return [link for link in links if link.target or link.anchor.headings or link.anchor.block]


def markdown_links(text: str) -> list[Link]:
    """Find every Markdown link or embed to a local file or a heading (not a URL).

    Args:
        text: Text with code already blanked out.

    Returns:
        Each link, its target the decoded path without `<>` or the `#anchor`.
    """
    links = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw = match.group(1).removeprefix("<").removesuffix(">")
        if SCHEME_RE.match(raw):
            continue  # a URL (or mailto:), not a file
        path, has_anchor, anchor_text = unquote(raw).partition("#")
        anchor = parse_anchor(anchor_text) if has_anchor else Anchor()
        if path or anchor.headings or anchor.block:
            line = _line_of(text, match.start())
            links.append(Link(target=path, anchor=anchor, shown=f"({unquote(raw)})", line=line))
    return links


def heading_key(text: str) -> str:
    """Normalize heading text the way a link to it is matched.

    Obsidian drops characters such as `#`, `|`, `^`, `:`, `%`, and `[]` when
    it links to a heading, and matching ignores case and repeated spaces.

    Args:
        text: A heading's text, or a heading named in a link.

    Returns:
        The comparison key.
    """
    return " ".join(HEADING_DROPPED_RE.sub(" ", nfc_casefold(text)).split())


def nfc_casefold(text: str) -> str:
    """NFC-normalize and case-fold text.

    Args:
        text: Any text.

    Returns:
        The folded text.
    """
    return unicodedata.normalize("NFC", text).casefold()


def headings(text: str) -> list[Heading]:
    """Find every ATX heading (`## Heading`) in a note body, outside fenced code.

    Args:
        text: A note body.

    Returns:
        Each heading's level and key, in order.
    """
    found = []
    for line in blank_fences(text).split("\n"):
        match = HEADING_RE.match(line)
        if match:
            found.append(Heading(level=len(match.group(1)), key=heading_key(match.group(2))))
    return found


def block_ids(text: str) -> frozenset[str]:
    """Find every block ID (`^abc123` ending a line) in a note body, outside code.

    Args:
        text: A note body.

    Returns:
        The IDs, case-folded, without their `^`.
    """
    return frozenset(
        match.group(1).casefold()
        for line in blank_code(text).split("\n")
        if (match := BLOCK_ID_RE.search(line))
    )


def has_heading_chain(found: list[Heading], chain: list[str]) -> bool:
    """Check that a chain of headings exists, each one inside the previous one's section.

    Args:
        found: A note's headings, in order.
        chain: Headings named in a link, outer to inner.

    Returns:
        Whether the note has them, nested in that order.
    """
    keys = [heading_key(heading) for heading in chain]

    def search(start: int, end: int, rest: list[str]) -> bool:
        if not rest:
            return True
        for index in range(start, end):
            heading = found[index]
            if heading.key != rest[0]:
                continue
            section_end = next(
                (j for j in range(index + 1, end) if found[j].level <= heading.level), end
            )
            if search(index + 1, section_end, rest[1:]):
                return True
        return False

    return search(0, len(found), keys)


def urls(text: str) -> list[Found]:
    """Find every http or https URL in text.

    Args:
        text: Text with code already blanked out.

    Returns:
        Each URL and its line.
    """
    return [
        Found(text=match.group(0), line=_line_of(text, match.start()))
        for match in URL_RE.finditer(text)
    ]


def tags(text: str) -> list[Found]:
    """Find every inline tag, the way Obsidian recognizes them.

    A tag needs at least one character that isn't a digit, so `#123` isn't one.

    Args:
        text: Text with code already blanked out.

    Returns:
        Each tag without its `#`, and its line.
    """
    return [
        Found(text=match.group(1), line=_line_of(text, match.start()))
        for match in TAG_RE.finditer(text)
        if not match.group(1).isdigit()
    ]


def is_web_url(value: str) -> bool:
    """Check that text is exactly one http or https URL with a host.

    Args:
        value: Text from a property.

    Returns:
        Whether it is a well-formed web URL and nothing else.
    """
    if any(char.isspace() for char in value):
        return False
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    return parts.scheme.lower() in WEB_SCHEMES and bool(parts.hostname)


def markdown_link_targets(note_rel: str, path: str) -> list[str]:
    """Express a Markdown link's path as the link targets Obsidian might mean.

    Obsidian writes Markdown links as a bare name, a path relative to the note,
    or a path from the vault root, depending on a setting Claude can't see. A
    relative path inside Public/ becomes a path from Public/; one that climbs
    out of Public/ becomes a path from the repository root (e.g.,
    `Private/Finance/Salary`).

    Args:
        note_rel: The linking note's path relative to Public/.
        path: The decoded link path.

    Returns:
        Every reading of the path, as wikilink-style targets.
    """
    if "/" not in path:
        return [clean_target(path)]
    targets = [clean_target(path.lstrip("/"))]
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(note_rel), path))
    if not joined.startswith("../"):
        targets.append(clean_target(joined))
    elif not joined.startswith("../../"):
        targets.append(clean_target(joined.removeprefix("../")))
    return list(dict.fromkeys(targets))

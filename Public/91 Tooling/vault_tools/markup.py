"""Find links and URLs in note text, the way Obsidian reads Markdown.

Code is never a link: fenced code blocks and inline code spans are blanked out
before anything is searched, so examples such as `[[Note]]` in backticks are
ignored. Blanking keeps every newline, so line numbers stay right.
"""

import posixpath
import re
from typing import Final
from urllib.parse import unquote, urlsplit

from pydantic import BaseModel, ConfigDict

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


class Found(BaseModel):
    """Something found in a piece of text.

    Attributes:
        text: The link target or URL.
        line: The 1-based line it is on, within the searched text.
    """

    model_config = ConfigDict(frozen=True)

    text: str
    line: int


def blank_code(text: str) -> str:
    """Replace fenced code blocks and inline code with spaces, keeping every newline.

    Args:
        text: Markdown text.

    Returns:
        The same text with code blanked out, the same number of lines long.
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
    return INLINE_CODE_RE.sub(lambda match: " " * len(match.group(0)), "\n".join(lines))


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


def wikilinks(text: str) -> list[Found]:
    """Find every wikilink and embed in text, as cleaned targets.

    Args:
        text: Text with code already blanked out.

    Returns:
        Each link's target and line, empty targets (`[[]]`) left out.
    """
    found = [
        Found(text=clean_target(match.group(1)), line=_line_of(text, match.start()))
        for match in WIKILINK_RE.finditer(text)
    ]
    return [link for link in found if link.text]


def markdown_links(text: str) -> list[Found]:
    """Find every Markdown link or embed to a local file (not a URL).

    Args:
        text: Text with code already blanked out.

    Returns:
        Each link's decoded path, without `<>` or an `#anchor`, and its line.
    """
    found = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw = match.group(1).removeprefix("<").removesuffix(">")
        if SCHEME_RE.match(raw):
            continue  # a URL (or mailto:), not a file
        path = unquote(raw).split("#", 1)[0]
        if path:
            found.append(Found(text=path, line=_line_of(text, match.start())))
    return found


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
    relative path that climbs out of Public/ becomes a path from the
    repository root (e.g., `Private/Finance/Salary`).

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
    if joined.startswith("../") and not joined.startswith("../../"):
        targets.append(clean_target(joined.removeprefix("../")))
    return targets

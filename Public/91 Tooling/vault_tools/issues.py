"""Issues: the problems the validators report, and the order reports list them in."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Severity(StrEnum):
    """How bad an issue is: errors fail a run, warnings don't."""

    ERROR = "error"
    WARNING = "warning"


class CheckName(StrEnum):
    """The check that reported an issue."""

    SCHEMA = "schema"
    PROPERTIES = "properties"
    STRUCTURE = "structure"
    LINKS = "links"
    URLS = "urls"
    TAGS = "tags"


class IssueCode(StrEnum):
    """Stable identifier for each kind of issue, as it appears in JSON reports."""

    # Schemas
    SCHEMA_ERROR = "schema-error"
    VERSION_MISMATCH = "version-mismatch"
    # Loading notes
    READ_ERROR = "read-error"
    FRONTMATTER_INVALID = "frontmatter-invalid"
    # Properties
    MISSING_TYPE = "missing-type"
    UNKNOWN_TYPE = "unknown-type"
    MISSING_PROPERTY = "missing-property"
    EMPTY_PROPERTY = "empty-property"
    UNKNOWN_PROPERTY = "unknown-property"
    PROPERTY_NOT_ALLOWED = "property-not-allowed"
    WRONG_VALUE_TYPE = "wrong-value-type"
    NESTED_OBJECT = "nested-object"
    NOT_IN_VOCAB = "not-in-vocab"
    OUT_OF_RANGE = "out-of-range"
    PATTERN_MISMATCH = "pattern-mismatch"
    NOT_A_LINK = "not-a-link"
    LINK_UNRESOLVED = "link-unresolved"
    LINK_AMBIGUOUS = "link-ambiguous"
    LINK_WRONG_TYPE = "link-wrong-type"
    # Structure
    UNDECLARED_FOLDER = "undeclared-folder"
    NOT_FLAT = "not-flat"
    TOO_DEEP = "too-deep"
    FILE_NOT_ALLOWED = "file-not-allowed"
    TYPE_NOT_ALLOWED = "type-not-allowed"
    MISSING_HUB = "missing-hub"
    HUB_WRONG_TYPE = "hub-wrong-type"
    HUB_MISNAMED = "hub-misnamed"
    FILENAME_MISMATCH = "filename-mismatch"
    # Links and URLs
    PRIVATE_LINK = "private-link"
    ANCHOR_UNRESOLVED = "anchor-unresolved"
    URL_MISPLACED = "url-misplaced"
    URL_INVALID = "url-invalid"
    URL_BROKEN = "url-broken"
    URL_UNVERIFIED = "url-unverified"
    # Tags
    UNKNOWN_TAG = "unknown-tag"


class Issue(BaseModel):
    """One problem found in the vault or its schemas.

    Attributes:
        severity: Whether the issue fails the run.
        check: The check that found it.
        code: What kind of problem it is.
        path: Where it is: a path relative to Public/, or a schema file name.
        message: A sentence saying what's wrong, for people.
        property: The frontmatter property at fault, if there is one.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    severity: Severity
    check: CheckName
    code: IssueCode
    path: str
    message: str
    property: str | None = None


def error_issue(
    check: CheckName, code: IssueCode, path: str, message: str, *, prop: str | None = None
) -> Issue:
    """Build an error-severity issue.

    Args:
        check: The check that found it.
        code: What kind of problem it is.
        path: Where it is, relative to Public/ or a schema file name.
        message: A sentence saying what's wrong.
        prop: The frontmatter property at fault, if any.

    Returns:
        The issue.
    """
    return Issue(
        severity=Severity.ERROR, check=check, code=code, path=path, message=message, property=prop
    )


def warning_issue(
    check: CheckName, code: IssueCode, path: str, message: str, *, prop: str | None = None
) -> Issue:
    """Build a warning-severity issue.

    Args:
        check: The check that found it.
        code: What kind of problem it is.
        path: Where it is, relative to Public/ or a schema file name.
        message: A sentence saying what's wrong.
        prop: The frontmatter property at fault, if any.

    Returns:
        The issue.
    """
    return Issue(
        severity=Severity.WARNING, check=check, code=code, path=path, message=message, property=prop
    )


def sort_key(issue: Issue) -> tuple[str, bool, str, str, str]:
    """Order issues by path, errors before warnings, then check, code, and message.

    Args:
        issue: The issue to place.

    Returns:
        A key for `sorted`.
    """
    return (issue.path, issue.severity != Severity.ERROR, issue.check, issue.code, issue.message)

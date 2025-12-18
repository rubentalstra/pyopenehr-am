"""openehr_am: a pure-Python openEHR AM toolkit.

This package is intentionally standards-driven and keeps a *small* public API.

Stable API (until v1.0):
        - `parse_archetype`, `parse_template`
        - `validate(obj, level=..., rm=...)`
        - `load_bmm_repo(dir)`
        - `compile_opt(template, archetype_dir=..., rm=...)`
"""

from pathlib import Path
from typing import TYPE_CHECKING, Literal

from openehr_am.__about__ import __version__

if TYPE_CHECKING:
    from openehr_am.aom.archetype import Archetype, Template
    from openehr_am.bmm.repository import ModelRepository
    from openehr_am.opt.model import OperationalTemplate
    from openehr_am.validation.issue import Issue


type ValidationLevel = Literal["syntax", "semantic", "rm", "opt", "all"]


def parse_archetype(
    *,
    text: str | None = None,
    path: str | Path | None = None,
    filename: str | None = None,
) -> tuple[Archetype | None, list[Issue]]:
    """Parse ADL and build an AOM `Archetype`.

    Exactly one of `text` or `path` must be provided.

    Returns:
            `(archetype, issues)` where `archetype` is None on failure.
    """

    if (text is None) == (path is None):
        raise TypeError("parse_archetype expects exactly one of 'text' or 'path'")

    from openehr_am.adl.parser import parse_adl
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.builder import build_aom_from_adl
    from openehr_am.validation.issue import Issue, Severity

    if path is not None:
        p = Path(path)
        try:
            source = p.read_text(encoding="utf-8")
        except OSError as e:
            return (
                None,
                [
                    Issue(
                        code="ADL005",
                        severity=Severity.ERROR,
                        message=f"Cannot read input file: {e}",
                        file=str(p),
                        line=1,
                        col=1,
                    )
                ],
            )
        artefact, issues = parse_adl(source, filename=str(p))
    else:
        assert text is not None
        artefact, issues = parse_adl(text, filename=filename)

    if artefact is None:
        return None, issues

    aom_obj, build_issues = build_aom_from_adl(artefact)
    issues.extend(build_issues)

    if not isinstance(aom_obj, Archetype):
        if aom_obj is not None:
            span = getattr(aom_obj, "span", None)
            issues.append(
                Issue(
                    code="AOM205",
                    severity=Severity.ERROR,
                    message="Expected an archetype ADL artefact",
                    file=span.file if span else None,
                    line=span.start_line if span else None,
                    col=span.start_col if span else None,
                    end_line=span.end_line if span else None,
                    end_col=span.end_col if span else None,
                )
            )
        return None, issues

    return aom_obj, issues


def parse_template(
    *,
    text: str | None = None,
    path: str | Path | None = None,
    filename: str | None = None,
) -> tuple[Template | None, list[Issue]]:
    """Parse ADL and build an AOM `Template`.

    Exactly one of `text` or `path` must be provided.

    Returns:
            `(template, issues)` where `template` is None on failure.
    """

    if (text is None) == (path is None):
        raise TypeError("parse_template expects exactly one of 'text' or 'path'")

    from openehr_am.adl.parser import parse_adl
    from openehr_am.aom.archetype import Template
    from openehr_am.aom.builder import build_aom_from_adl
    from openehr_am.validation.issue import Issue, Severity

    if path is not None:
        p = Path(path)
        try:
            source = p.read_text(encoding="utf-8")
        except OSError as e:
            return (
                None,
                [
                    Issue(
                        code="ADL005",
                        severity=Severity.ERROR,
                        message=f"Cannot read input file: {e}",
                        file=str(p),
                        line=1,
                        col=1,
                    )
                ],
            )
        artefact, issues = parse_adl(source, filename=str(p))
    else:
        assert text is not None
        artefact, issues = parse_adl(text, filename=filename)

    if artefact is None:
        return None, issues

    aom_obj, build_issues = build_aom_from_adl(artefact)
    issues.extend(build_issues)

    if not isinstance(aom_obj, Template):
        if aom_obj is not None:
            span = getattr(aom_obj, "span", None)
            issues.append(
                Issue(
                    code="AOM205",
                    severity=Severity.ERROR,
                    message="Expected a template ADL artefact",
                    file=span.file if span else None,
                    line=span.start_line if span else None,
                    col=span.start_col if span else None,
                    end_line=span.end_line if span else None,
                    end_col=span.end_col if span else None,
                )
            )
        return None, issues

    return aom_obj, issues


def load_bmm_repo(
    directory: str | Path,
) -> tuple[ModelRepository | None, list[Issue]]:
    """Load a BMM/RM repository directory.

    Returns:
            `(repo, issues)` where `repo` is None if loading fails.
    """

    from openehr_am.bmm.repository import ModelRepository
    from openehr_am.validation.issue import Issue, Severity

    try:
        repo, issues = ModelRepository.load_from_dir(directory)
        return repo, list(issues)
    except NotADirectoryError as e:
        p = Path(directory)
        return (
            None,
            [
                Issue(
                    code="BMM505",
                    severity=Severity.ERROR,
                    message=str(e),
                    file=str(p),
                    line=1,
                    col=1,
                )
            ],
        )


def compile_opt(
    template: Template,
    *,
    archetype_dir: str | Path,
    rm: ModelRepository | None = None,
) -> tuple[OperationalTemplate | None, list[Issue]]:
    """Compile an AOM `Template` into an OPT.

    Notes:
            `rm` is reserved for future RM-aware compilation; it is currently
            unused by the MVP compiler.
    """

    from openehr_am.opt.compiler import compile_opt as _compile

    return _compile(template, archetype_dir=archetype_dir)


def validate(
    obj: object,
    *,
    level: ValidationLevel = "all",
    rm: ModelRepository | None = None,
) -> tuple[Issue, ...]:
    """Validate an object at a chosen pipeline level.

    Args:
            obj:
                    - For `level="syntax"`: ADL text (`str`) or file path (`Path|str`).
                    - For `level in {"semantic", "rm"}`: AOM `Archetype` or `Template`.
                    - For `level="opt"`: an `OperationalTemplate`.
            level: Validation stage to run.
            rm: Optional RM repo (typically `ModelRepository`) for RM validation.

    Returns:
            Tuple of `Issue` objects, deterministically ordered.
    """

    from openehr_am.validation.issue_collector import IssueCollector

    collector = IssueCollector()

    if level not in {"syntax", "semantic", "rm", "opt", "all"}:
        raise ValueError(f"Unknown validation level: {level!r}")

    if isinstance(obj, (str, Path)):
        if level not in {"syntax", "all"}:
            raise TypeError(
                "validate(text|path) only supports level='syntax' or level='all'"
            )

        from openehr_am.validation.syntax import validate_syntax

        if isinstance(obj, Path):
            collector.extend(validate_syntax(path=obj))
            return collector.issues

        # Heuristic: if this looks like an existing file path, validate as a file.
        maybe_path = Path(obj)
        if maybe_path.exists() and maybe_path.is_file():
            collector.extend(validate_syntax(path=maybe_path))
        else:
            collector.extend(validate_syntax(text=obj))
        return collector.issues

    from openehr_am.aom.archetype import Archetype, Template
    from openehr_am.opt.model import OperationalTemplate

    if isinstance(obj, (Archetype, Template)):
        if level in {"semantic", "all"}:
            from openehr_am.validation.semantic import validate_semantic

            collector.extend(validate_semantic(obj))

        if level in {"rm", "all"}:
            from openehr_am.validation.rm import validate_rm

            collector.extend(validate_rm(obj, rm_repo=rm))

        return collector.issues

    if isinstance(obj, OperationalTemplate):
        if level not in {"opt", "all"}:
            raise TypeError(
                "validate(OperationalTemplate) supports level='opt' or 'all'"
            )

        from openehr_am.validation.opt import validate_opt

        collector.extend(validate_opt(obj))
        return collector.issues

    raise TypeError(
        "validate() expects ADL text/path, an AOM Archetype/Template, or an OperationalTemplate"
    )


__all__ = [
    "__version__",
    "ValidationLevel",
    "parse_archetype",
    "parse_template",
    "validate",
    "load_bmm_repo",
    "compile_opt",
]

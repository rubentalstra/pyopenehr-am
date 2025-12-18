from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import click
import typer
from rich.console import Console

from openehr_am import (
    compile_opt,
    load_bmm_repo,
    parse_archetype,
    parse_template,
    validate,
)
from openehr_am.cli.render import render_issues
from openehr_am.validation.issue import Issue, Severity

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
)


class OutputFormat(StrEnum):
    text = "text"
    json = "json"


@dataclass(slots=True)
class _CliConfig:
    no_color: bool = False


def _console(cfg: _CliConfig) -> Console:
    return Console(no_color=cfg.no_color)


def _coerce_format(*, fmt: OutputFormat, json_flag: bool) -> OutputFormat:
    if json_flag:
        return OutputFormat.json
    return fmt


def _exit_code_for_issues(
    issues: list[Issue] | tuple[Issue, ...],
    *,
    strict: bool,
    io_error: bool,
) -> int:
    if io_error:
        return 2

    if any(i.severity == Severity.ERROR for i in issues):
        return 1

    if strict and any(i.severity == Severity.WARN for i in issues):
        return 1

    return 0


def _guess_adl_kind(path: Path) -> str | None:
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("--"):
                    continue
                lowered = stripped.lower()
                if lowered.startswith("template"):
                    return "template"
                if lowered.startswith("archetype"):
                    return "archetype"
                return None
    except OSError:
        return None


def _is_io_issue(issue: Issue) -> bool:
    # IO codes documented in docs/issue-codes.md.
    return issue.code in {"ADL005", "BMM505", "CLI010", "CLI011"}


def _render_and_exit(
    issues: list[Issue] | tuple[Issue, ...],
    *,
    cfg: _CliConfig,
    fmt: OutputFormat,
    strict: bool,
    io_error: bool,
) -> None:
    console = _console(cfg)
    render_issues(issues, console=console, as_json=(fmt == OutputFormat.json))
    raise typer.Exit(
        code=_exit_code_for_issues(issues, strict=strict, io_error=io_error)
    )


@app.callback()
def _main(
    ctx: typer.Context,
    no_color: bool = typer.Option(
        False,
        "--no-color",
        help="Disable ANSI colors/markup (useful in CI).",
    ),
) -> None:
    """openEHR AM toolkit CLI."""

    ctx.obj = _CliConfig(no_color=no_color)


@app.command("lint")
def cmd_lint(
    file: Path = typer.Argument(..., help="ADL2 file to parse."),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors (exit code 1).",
    ),
    fmt: OutputFormat = typer.Option(
        OutputFormat.text,
        "--format",
        help="Output format for Issues.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Alias for --format json.",
    ),
) -> None:
    """Parse an ADL2 file and report syntax Issues."""

    cfg: _CliConfig = click.get_current_context().obj
    fmt = _coerce_format(fmt=fmt, json_flag=json_output)

    issues = list(validate(file, level="syntax"))
    io_error = any(_is_io_issue(i) for i in issues)
    _render_and_exit(issues, cfg=cfg, fmt=fmt, strict=strict, io_error=io_error)


@app.command("validate")
def cmd_validate(
    file: Path = typer.Argument(..., help="ADL2 archetype or template file."),
    rm: Path | None = typer.Option(
        None,
        "--rm",
        help="BMM/RM repository directory for RM validation.",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors (exit code 1).",
    ),
    fmt: OutputFormat = typer.Option(
        OutputFormat.text,
        "--format",
        help="Output format for Issues.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Alias for --format json.",
    ),
) -> None:
    """Validate semantic (and optionally RM) constraints for an ADL2 file."""

    cfg: _CliConfig = click.get_current_context().obj
    fmt = _coerce_format(fmt=fmt, json_flag=json_output)

    # Parse into AOM.
    kind = _guess_adl_kind(file)
    if kind == "template":
        aom_obj, parse_issues = parse_template(path=file)
    else:
        aom_obj, parse_issues = parse_archetype(path=file)

    issues: list[Issue] = list(parse_issues)
    io_error = any(_is_io_issue(i) for i in issues)

    rm_repo = None
    if rm is not None:
        repo, rm_issues = load_bmm_repo(rm)
        issues.extend(rm_issues)
        if repo is None:
            io_error = True
        rm_repo = repo

    if aom_obj is not None and not io_error:
        if rm_repo is not None:
            issues.extend(validate(aom_obj, level="all", rm=rm_repo))
        else:
            issues.extend(validate(aom_obj, level="semantic"))

    _render_and_exit(issues, cfg=cfg, fmt=fmt, strict=strict, io_error=io_error)


@app.command("compile-opt")
def cmd_compile_opt(
    template: Path = typer.Argument(..., help="Template ADL2 file."),
    repo: Path = typer.Option(
        ...,
        "--repo",
        help="Directory containing archetype ADL files referenced by the template.",
    ),
    out: Path = typer.Option(
        ...,
        "--out",
        help="Path to write the compiled OPT JSON.",
    ),
    rm: Path | None = typer.Option(
        None,
        "--rm",
        help="BMM/RM repository directory (reserved for future RM-aware compilation).",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors (exit code 1).",
    ),
    fmt: OutputFormat = typer.Option(
        OutputFormat.text,
        "--format",
        help="Output format for Issues.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Alias for --format json.",
    ),
) -> None:
    """Compile a template to an OPT2 JSON file."""

    from openehr_am.opt.json import opt_to_json

    cfg: _CliConfig = click.get_current_context().obj
    fmt = _coerce_format(fmt=fmt, json_flag=json_output)

    issues: list[Issue] = []
    io_error = False

    if not repo.exists() or not repo.is_dir():
        issues.append(
            Issue(
                code="CLI011",
                severity=Severity.ERROR,
                message="--repo must be an existing directory",
                file=str(repo),
                line=1,
                col=1,
            )
        )
        io_error = True

    rm_repo = None
    if rm is not None:
        repo_obj, rm_issues = load_bmm_repo(rm)
        issues.extend(rm_issues)
        if repo_obj is None:
            io_error = True
        rm_repo = repo_obj

    tmpl, parse_issues = parse_template(path=template)
    issues.extend(parse_issues)
    if any(i.code == "ADL005" for i in parse_issues):
        io_error = True

    opt = None
    if tmpl is not None and not io_error:
        opt, compile_issues = compile_opt(tmpl, archetype_dir=repo, rm=rm_repo)
        issues.extend(compile_issues)

    if (
        opt is not None
        and not io_error
        and not any(i.severity == Severity.ERROR for i in issues)
    ):
        try:
            out.write_text(opt_to_json(opt, indent=2), encoding="utf-8")
        except OSError as e:
            issues.append(
                Issue(
                    code="CLI010",
                    severity=Severity.ERROR,
                    message=f"Cannot write output file: {e}",
                    file=str(out),
                    line=1,
                    col=1,
                )
            )
            io_error = True

    _render_and_exit(issues, cfg=cfg, fmt=fmt, strict=strict, io_error=io_error)

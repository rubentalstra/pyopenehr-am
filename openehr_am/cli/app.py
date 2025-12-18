import typer

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
)


@app.callback()
def _main() -> None:
    """openEHR AM toolkit CLI."""

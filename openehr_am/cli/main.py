import typer


app = typer.Typer(
    name="openehr-am",
    help="openEHR AM toolkit CLI (placeholder).",
    add_completion=False,
)


@app.callback()
def main() -> None:
    """Entry point for `openehr-am`.

    Placeholder CLI; commands will be added later.
    """

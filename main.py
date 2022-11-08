import settings
from cli import run_cli


if settings.MODE == "CLI":
    run_cli()

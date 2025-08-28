import asyncio
import signal
import sys

import click

import pyinfra

from .main import cli

# Set CLI mode
pyinfra.is_cli = True

# Don't write out deploy.pyc/config.pyc etc
sys.dont_write_bytecode = True

sys.path.append(".")

# Shut it click
click.disable_unicode_literals_warning = True  # type: ignore

# Force line buffering
sys.stdout.reconfigure(line_buffering=True)  # type: ignore
sys.stderr.reconfigure(line_buffering=True)  # type: ignore


def _handle_interrupt(signum, frame):
    click.echo("Exiting upon user request!")
    sys.exit(0)


async def main():
    """
    Main asynchronous function to run the CLI.
    """
    try:
        # Run the CLI command
        await cli()
    except asyncio.CancelledError:
        click.echo("CLI execution was cancelled.")
        sys.exit(0)


if __name__ == "pyinfra_cli.__main__":
    # Register the interrupt handler for SIGINT
    signal.signal(signal.SIGINT, _handle_interrupt)

    # Run the main function using asyncio
    asyncio.run(main())
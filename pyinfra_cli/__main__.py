import signal
import sys

import click
import asyncio

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
    # Your application logic here
    await execute(cli())

if __name__ == "pyinfra_cli.__main__":
    asyncio.run(main())

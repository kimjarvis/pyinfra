import logging  # noqa: I100

import asyncio

import pyinfra_cli  # noqa: F401
from pyinfra import logger

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

# Define an exception handler for asyncio tasks
def asyncio_exception_handler(loop, context):
    """
    Custom exception handler for asyncio to suppress specific exceptions.
    This mimics the behavior of gevent.hub.Hub.NOT_ERROR.
    """
    exception = context.get("exception")
    if isinstance(exception, Exception):  # Suppress all exceptions of type Exception
        logger.debug(f"Suppressed exception in asyncio task: {exception}")
    else:
        # Log unexpected errors
        logger.error(f"Unexpected error in asyncio task: {context}")

# Set the custom exception handler for the asyncio event loop
loop = asyncio.get_event_loop()
loop.set_exception_handler(asyncio_exception_handler)
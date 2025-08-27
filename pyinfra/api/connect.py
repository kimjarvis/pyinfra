from typing import TYPE_CHECKING
import asyncio

from pyinfra.progress import progress_spinner

if TYPE_CHECKING:
    from pyinfra.api.state import State


async def connect_all(state: "State"):
    """
    Connect to all the configured servers in parallel using asyncio. Reads/writes state.inventory.

    Args:
        state (``pyinfra.api.State`` obj): the state containing an inventory to connect to
    """

    # Filter hosts based on limits
    hosts = [
        host
        for host in state.inventory
        if state.is_host_in_limit(host)  # these are the hosts to activate ("initially connect to")
    ]

    # Create tasks for connecting to each host
    task_to_host = {asyncio.create_task(host.connect()): host for host in hosts}

    # Use a progress spinner to track progress
    with progress_spinner(task_to_host.values()) as progress:
        for task in asyncio.as_completed(task_to_host.keys()):
            host = task_to_host[await task]
            progress(host)

    # Get/set the results
    failed_hosts = set()

    for task, host in task_to_host.items():
        try:
            # Wait for the task to complete and handle any exceptions
            await task
        except Exception as e:
            print(f"Error connecting to {host}: {e}")
            failed_hosts.add(host)
            continue

        if host.connected:
            state.activate_host(host)
        else:
            failed_hosts.add(host)

    # Remove those that failed, triggering FAIL_PERCENT check
    state.fail_hosts(failed_hosts, activated_count=len(hosts))


async def disconnect_all(state: "State"):
    """
    Disconnect from all of the configured servers in parallel using asyncio. Reads/writes state.inventory.

    Args:
        state (``pyinfra.api.State`` obj): the state containing an inventory to connect to
    """
    # Create tasks for disconnecting from each host
    task_to_host = {
        asyncio.create_task(host.disconnect()): host
        for host in state.activated_hosts  # only hosts we connected to please!
    }

    # Use a progress spinner to track progress
    with progress_spinner(task_to_host.values()) as progress:
        for task in asyncio.as_completed(task_to_host.keys()):
            host = task_to_host[await task]
            progress(host)

    # Handle task results
    for task, host in task_to_host.items():
        try:
            # Wait for the task to complete and handle any exceptions
            await task
        except Exception as e:
            print(f"Error disconnecting from {host}: {e}")
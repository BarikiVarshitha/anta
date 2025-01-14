# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
# pylint: disable = redefined-outer-name
"""
Click commands to get information from or generate inventories
"""
from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

import click
from cvprac.cvp_client import CvpClient
from cvprac.cvp_client_errors import CvpApiError
from rich.pretty import pretty_repr

from anta.cli.console import console
from anta.cli.get.utils import inventory_output_options
from anta.cli.utils import ExitCode, inventory_options
from anta.inventory import AntaInventory

from .utils import create_inventory_from_ansible, create_inventory_from_cvp, get_cv_token

logger = logging.getLogger(__name__)


@click.command
@click.pass_context
@inventory_output_options
@click.option("--host", "-host", help="CloudVision instance FQDN or IP", type=str, required=True)
@click.option("--username", "-u", help="CloudVision username", type=str, required=True)
@click.option("--password", "-p", help="CloudVision password", type=str, required=True)
@click.option("--container", "-c", help="CloudVision container where devices are configured", type=str)
def from_cvp(ctx: click.Context, output: Path, host: str, username: str, password: str, container: str | None) -> None:
    """
    Build ANTA inventory from Cloudvision

    TODO - handle get_inventory and get_devices_in_container failure
    """
    logger.info(f"Getting authentication token for user '{username}' from CloudVision instance '{host}'")
    token = get_cv_token(cvp_ip=host, cvp_username=username, cvp_password=password)

    clnt = CvpClient()
    try:
        clnt.connect(nodes=[host], username="", password="", api_token=token)
    except CvpApiError as error:
        logger.error(f"Error connecting to CloudVision: {error}")
        ctx.exit(ExitCode.USAGE_ERROR)
    logger.info(f"Connected to CloudVision instance '{host}'")

    cvp_inventory = None
    if container is None:
        # Get a list of all devices
        logger.info(f"Getting full inventory from CloudVision instance '{host}'")
        cvp_inventory = clnt.api.get_inventory()
    else:
        # Get devices under a container
        logger.info(f"Getting inventory for container {container} from CloudVision instance '{host}'")
        cvp_inventory = clnt.api.get_devices_in_container(container)
    create_inventory_from_cvp(cvp_inventory, output)


@click.command
@click.pass_context
@inventory_output_options
@click.option("--ansible-group", "-g", help="Ansible group to filter", type=str, default="all")
@click.option(
    "--ansible-inventory",
    help="Path to your ansible inventory file to read",
    type=click.Path(file_okay=True, dir_okay=False, exists=True, readable=True, path_type=Path),
    required=True,
)
def from_ansible(ctx: click.Context, output: Path, ansible_group: str, ansible_inventory: Path) -> None:
    """Build ANTA inventory from an ansible inventory YAML file"""
    logger.info(f"Building inventory from ansible file '{ansible_inventory}'")
    try:
        create_inventory_from_ansible(
            inventory=ansible_inventory,
            output=output,
            ansible_group=ansible_group,
        )
    except ValueError as e:
        logger.error(str(e))
        ctx.exit(ExitCode.USAGE_ERROR)


@click.command
@inventory_options
@click.option("--connected/--not-connected", help="Display inventory after connection has been created", default=False, required=False)
def inventory(inventory: AntaInventory, tags: list[str] | None, connected: bool) -> None:
    """Show inventory loaded in ANTA."""

    logger.debug(f"Requesting devices for tags: {tags}")
    console.print("Current inventory content is:", style="white on blue")

    if connected:
        asyncio.run(inventory.connect_inventory())

    inventory_result = inventory.get_inventory(tags=tags)
    console.print(pretty_repr(inventory_result))


@click.command
@inventory_options
def tags(inventory: AntaInventory, tags: list[str] | None) -> None:  # pylint: disable=unused-argument
    """Get list of configured tags in user inventory."""
    tags_found = []
    for device in inventory.values():
        tags_found += device.tags
    tags_found = sorted(set(tags_found))
    console.print("Tags found:")
    console.print_json(json.dumps(tags_found, indent=2))

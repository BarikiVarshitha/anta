# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""
Click commands to execute various scripts on EOS devices
"""
from __future__ import annotations

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

import click
from yaml import safe_load

from anta.cli.exec.utils import clear_counters_utils, collect_commands, collect_scheduled_show_tech
from anta.cli.utils import inventory_options
from anta.inventory import AntaInventory

logger = logging.getLogger(__name__)


@click.command
@inventory_options
def clear_counters(inventory: AntaInventory, tags: list[str] | None) -> None:
    """Clear counter statistics on EOS devices"""
    asyncio.run(clear_counters_utils(inventory, tags=tags))


@click.command()
@inventory_options
@click.option(
    "--commands-list",
    "-c",
    help="File with list of commands to collect",
    required=True,
    show_envvar=True,
    type=click.Path(file_okay=True, dir_okay=False, exists=True, readable=True, path_type=Path),
)
@click.option(
    "--output",
    "-o",
    show_envvar=True,
    type=click.Path(file_okay=False, dir_okay=True, exists=False, writable=True, path_type=Path),
    help="Directory to save commands output.",
    default=f"anta_snapshot_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}",
    show_default=True,
)
def snapshot(inventory: AntaInventory, tags: list[str] | None, commands_list: Path, output: Path) -> None:
    """Collect commands output from devices in inventory"""
    print(f"Collecting data for {commands_list}")
    print(f"Output directory is {output}")
    try:
        with open(commands_list, "r", encoding="UTF-8") as file:
            file_content = file.read()
            eos_commands = safe_load(file_content)
    except FileNotFoundError:
        logger.error(f"Error reading {commands_list}")
        sys.exit(1)
    asyncio.run(collect_commands(inventory, eos_commands, output, tags=tags))


@click.command()
@inventory_options
@click.option("--output", "-o", default="./tech-support", show_default=True, help="Path for test catalog", type=click.Path(path_type=Path), required=False)
@click.option("--latest", help="Number of scheduled show-tech to retrieve", type=int, required=False)
@click.option(
    "--configure",
    help="Ensure devices have 'aaa authorization exec default local' configured (required for SCP on EOS). THIS WILL CHANGE THE CONFIGURATION OF YOUR NETWORK.",
    default=False,
    is_flag=True,
    show_default=True,
)
def collect_tech_support(inventory: AntaInventory, tags: list[str] | None, output: Path, latest: int | None, configure: bool) -> None:
    """Collect scheduled tech-support from EOS devices"""
    asyncio.run(collect_scheduled_show_tech(inventory, output, configure, tags=tags, latest=latest))

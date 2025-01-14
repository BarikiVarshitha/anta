# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""
Click commands to execute various scripts on EOS devices
"""
import click

from anta.cli.exec import commands


@click.group
def exec() -> None:  # pylint: disable=redefined-builtin
    """Commands to execute various scripts on EOS devices"""


exec.add_command(commands.clear_counters)
exec.add_command(commands.snapshot)
exec.add_command(commands.collect_tech_support)

#  Copyright (c) 2015-2017 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import click

import molecule.command
from molecule import config
from molecule import logger
from molecule.command import base

LOG = logger.get_logger(__name__)


class Test(base.Base):
    """
    Target the default scenario:

    >>> molecule test

    Target all scenarios:

    >>> molecule test --all

    Targeting a specific scenario:

    >>> molecule test --scenario-name foo

    Targeting a specific driver:

    >>> molecule converge --driver-name foo

    Executing with `debug`:

    >>> molecule --debug test
    """

    def execute(self):
        """
        Execute the actions necessary to perform a `molecule test` and
        returns None.

        :return: None
        """


@click.command()
@click.pass_context
@click.option(
    '--scenario-name',
    default='default',
    help='Name of the scenario to target. (default)')
@click.option(
    '--driver-name',
    type=click.Choice(config.molecule_drivers()),
    help='Name of driver to use. (docker)')
@click.option(
    '--all/--no-all',
    '__all',
    default=False,
    help='Test all scenarios. Default is False.')
def test(ctx, scenario_name, driver_name, __all):  # pragma: no cover
    """ Test (destroy, create, converge, lint, verify, destroy). """
    args = ctx.obj.get('args')
    command_args = {
        'subcommand': __name__,
        'scenario_name': scenario_name,
        'driver_name': driver_name,
    }

    if __all:
        command_args['scenario_name'] = None

    for c in base.get_configs(args, command_args):
        for task in c.scenario.test_sequence:
            command_module = getattr(molecule.command, task)
            command = getattr(command_module, task.capitalize())
            command(c).execute()

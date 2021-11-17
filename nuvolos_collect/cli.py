#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: nuvolos_collect.cli
.. moduleauthor:: Mate Kovacs <mate.kovacs@alphacruncher.com>
"""
import click_log
from nuvolos_collect.logging import clog
import click
from .__init__ import __version__
from .collect import collect
from .distribute import distribute


@click.group()
@click_log.simple_verbosity_option(clog)
@click.pass_context
def cli(ctx):
    """
    NUVOLOS COLLECT TOOL

    The Nuvolos collect tool provides a convenient way to collect and hand out assignments submitted by your students.

    The following commands can be provided:

    collect: collects a specified assignment
    handout: hands out a specified assignment
    """
    # Use the verbosity count to determine the logging level...
    if ctx.obj is None:
        ctx.obj = dict()
    pass


@cli.command("collect")
@click.option(
    "--assignment_name",
    type=str,
    required=True,
    help="Sets the assignment name, which is provided by you on the Nuvolos UI when creating the assignment distribution.",
)
@click.option(
    "--assignment_folder",
    type=str,
    required=True,
    help="Sets the assignment folder, which is provided by you on the Nuvolos UI when creating the assignment distribution.",
)
@click.option(
    "--target_folder",
    type=str,
    required=True,
    help="Sets the target folder to which collected assignments are copied for evaluation.",
)
@click.pass_context
def collect_assignment(ctx, **kwargs):
    """
    collect command

    Collect a specified assignment. This triggers a script that iterates over the assignment folders under assignment_review/handing/...
    and for each user recovers the latest assignment that was handed in.

    Collected assignments are placed at a target location in assignment_name/userid/.. layout.
    """

    ret = collect(**kwargs)
    return ret


@cli.command("distribute")
@click.option(
    "--source_folder",
    type=str,
    required=True,
    help="Sets the assignment folder, which is provided by you on the Nuvolos UI when creating the assignment distribution.",
)
@click.pass_context
def distribute_assignment(ctx, **kwargs):
    """
    distribute command

    Distribute a specified assignment. This triggers a script that takes a collected and graded set of assignments and
    places them iteratively into their respective assignment_review/handback/... folders.

    The source directory should be the value that nvcollect collect was called with as a target.
    """
    ret = distribute(**kwargs)
    return ret


@cli.command("version")
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))

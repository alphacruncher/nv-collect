#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: nuvolos_collect.cli
.. moduleauthor:: Mate Kovacs <mate.kovacs@alphacruncher.com>
"""
import click_log
from nuvolos_collect.logging import clog
import click
from .__init__ import __version__
from nuvolos_collect.collect import collect
from nuvolos_collect.handback import handback
from nuvolos_collect.grade import otter_grade


@click.group()
@click_log.simple_verbosity_option(clog)
@click.pass_context
def cli(ctx):
    """
    NUVOLOS COLLECT TOOL

    The Nuvolos collect tool provides a convenient way to collect and hand out assignments submitted by your students.

    The following commands can be provided:

    collect: collects a specified assignment
    handback: hands out a specified assignment
    otter-grade: grades collected assignments with the otter-grader library (optional, needs to be installed)
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


@cli.command("handback")
@click.option(
    "--source_folder",
    type=str,
    required=True,
    help="Sets the assignment folder, which is provided by you on the Nuvolos UI when creating the assignment distribution.",
)
@click.pass_context
def handback_assignment(ctx, **kwargs):
    """
    handback command

    handback a specified assignment. This triggers a script that takes a collected and graded set of assignments and
    places them iteratively into their respective assignment_review/handback/... folders.

    The source directory should be the value that nvcollect collect was called with as a target.
    """
    ret = handback(**kwargs)
    return ret


@cli.command("otter-grade")
@click.option(
    "--source_folder",
    type=str,
    required=True,
    help="The folder where collected assignments reside.",
)
@click.option(
    "--autograder_location",
    type=str,
    required=True,
    help="The folder where collected assignments reside.",
)
@click.option(
    "--relative_path",
    type=str,
    required=True,
    help="The relative path compared to the assignment folder root where the notebook to be graded is located.",
)
@click.pass_context
def grade_assignment(ctx, **kwargs):
    """
    otter-grade command

    Execute the otter-grader on a collected set of assignments.
    """

    ret = otter_grade(**kwargs)
    return ret


@cli.command("version")
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))

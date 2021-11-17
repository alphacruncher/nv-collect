# nuvolos_collect

The Nuvolos Assignment Collector is a Command Line (CLI) tool that lets you collect hand-ins from your students with a single command, and once you've completed the grading, handing back is also a single command.

What you require:

- Access to [Nuvolos](https://nuvolos.cloud)
- Create an [assignment](https://docs.nuvolos.cloud/education/student-topics/assignments-1)
- Once the deadline has passed and students handed in their assignments, collect them with `nvcollect collect`
- Grade the assignments
- Once you are done with grading, hand back the documents with `nvcollect distribute`.

## Getting Started

This package comes installed with Python-based Nuvolos applications. In case you are missing the package for some reason, reach out to our support via Intercom. 

If you want to update the current version, hit `pip install --upgrade git+https://github.com/alphacruncher/nv-collect` in your terminal.

## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)

## Resources

Below are some handy resource links.

* [Project Documentation](http://nuvolos_collect.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## Authors

* **Mate Kovacs** - *Initial work* - [github](https://github.com/matek-alphacruncher)

See also the list of [contributors](https://github.com/matek-alphacruncher/nuvolos_collect/contributors) who participated in this project.

## LicenseCopyright (c) Mate Kovacs

All rights reserved.
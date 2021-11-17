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


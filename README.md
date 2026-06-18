# nuvolos_collect

The Nuvolos Assignment Collector is a Command Line (CLI) tool that lets you collect hand-ins from your students with a single command, and once you've completed the grading, handing back is also a single command.

What you require:

- Access to [Nuvolos](https://nuvolos.cloud)
- Create an [assignment](https://docs.nuvolos.cloud/education/student-topics/assignments-1)
- Once the deadline has passed and students handed in their assignments, collect them with `nvcollect collect`
- Grade the assignments
- Once you are done with grading, hand back the documents with `nvcollect distribute`.

## Commands

### collect

Collect a specific assignment's latest submissions, grouped by student.

```
nvcollect collect --assignment_name hw1 --assignment_folder homework --target_folder ./collected
```

Output: `target_folder/{instance_id}/...`

### archive

Collect submissions grouped by assignment and create a zip file per assignment. This inverts the default structure from `student/assignment/` to `assignment/student/...`.

```
# Archive all assignments
nvcollect archive --target_folder ./archives

# Archive a specific assignment
nvcollect archive --target_folder ./archives --assignment_name hw1

# Archive a specific assignment and folder
nvcollect archive --target_folder ./archives --assignment_name hw1 --assignment_folder homework
```

Output: `target_folder/{assignment_name}/{instance_id}/...` plus `target_folder/{assignment_name}.zip`

### handback

Hand back graded assignments to students. Reads the manifest written by `collect` and copies graded work to the handback directory.

```
nvcollect handback --source_folder ./collected
```

### otter-grade

Auto-grade collected assignments using the [otter-grader](https://otter-grader.readthedocs.io/) library (must be installed separately).

```
nvcollect otter-grade --source_folder ./collected --autograder_location ./autograder.zip --relative_path notebook.ipynb
```

## Getting Started

This package comes installed with Python-based Nuvolos applications. In case you are missing the package for some reason, reach out to our support via Intercom. 

If you want to update the current version, hit `pip install --upgrade git+https://github.com/alphacruncher/nv-collect` in your terminal.

## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)


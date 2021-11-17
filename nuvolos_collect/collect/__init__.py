from nuvolos_collect.logging import clog
from nuvolos_collect.collect.utils import (
    identify_collectables,
    distinct_submissions,
    gather_latest_submissions,
    path_identify,
    path_prefix,
    extract_instance_id,
    instance_grouped,
    get_latest_assignment,
    create_folder_structure,
    copy_submissions,
)
from nuvolos_collect.exception import *


def collect(assignment_name, assignment_folder, target_folder):

    """
    Look for the directory tree under assignments-review for subtrees that have matching
    assignment_name and assignment_folder path items. In case there is none, the user mis-specified either of the two folders.
    """

    try:
        colls = identify_collectables(assignment_name, assignment_folder)
    except NoCollectiblesException:
        clog.error(
            f'Found no collectable submissions with assignment name "{assignment_name}" and assignment folder "{assignment_folder}".'
        )
        return 1

    """
    From all the subtrees select ones that belong to distinct submissions
    """

    iinfo = distinct_submissions(colls)

    """
    Group submissions by user. 
    """

    ugs = instance_grouped(iinfo)

    """
    Select one submission to collect per user. Currently we only support the latest (one with highest parsed timestamp).
    """
    filtered = gather_latest_submissions(ugs)

    """
    Create folder structure for each user in the target_folder.
    """
    create_folder_structure(target_folder, filtered)

    """
    Copy all substructures of the selected sources into the appropriate user folder in the target.
    """
    copy_submissions(target_folder, filtered, assignment_name, assignment_folder)

    clog.info(f"Collection completed. We have collected {len(filtered)} submissions.")
    return 0

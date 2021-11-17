from datetime import datetime as dt
from pathlib import Path
import re
from nuvolos_collect.logging import clog
from nuvolos_collect.exception import (
    SourceDoesNotExistException,
    ManifestMissingException,
)
import json
import os
from distutils.dir_util import copy_tree
from datetime import datetime as dt


def do_nothing():
    pass


def read_manifest(source_folder):
    """read_manifest

    Reads the manifest log after the grading has happened and creates the data structure based on which
    graded homeworks are copied back to the handin folder.

    Args:
        source_folder (str): The folder which contains the list of submissions grouped by users.
    """

    if not os.path.exists(source_folder):
        raise SourceDoesNotExistException(f"Source {source_folder} does not exist.")

    path = f"{source_folder}/nvcollect_manifest.json"
    with open(path, "r") as j:
        info = json.loads(j.read())
    clog.debug(info)
    return info


def generate_target_info(source_info):

    cpinfo = source_info["items"]

    target_list = []
    for d in cpinfo:
        d["handback_target"] = d["src"].replace(
            "/assignments-review/handin", "/assignments-review/handback"
        )
        target_list += [d]

    clog.debug(target_list)
    return target_list


def execute_handback_copy(target_info):

    for d in target_info:
        copy_tree(d["target"], d["handback_target"])


def write_manifest_file(source_folder, target_info):
    now = dt.now()

    manifest_data = {"meta": {}, "items": target_info}
    printable_now = now.strftime("%Y-%m-%d %H:%M:%S")
    filename_now = now.strftime("%Y%m%d_%H%M%S")
    manifest_data["meta"]["handback_time"] = printable_now
    loc = f"{source_folder}/nvcollect_manifest_handback_{filename_now}.json"

    with open(loc, "w") as fp:
        json.dump(manifest_data, fp)
    return

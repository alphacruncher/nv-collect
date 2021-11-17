from datetime import datetime as dt
from pathlib import Path
import re
import os
from nuvolos_collect.logging import clog
from nuvolos_collect.exception import (
    NoCollectiblesException,
    AmbiguousCopySourceException,
)
import shutil
from datetime import datetime as dt
import json


def identify_collectables(assignment_name, assignment_folder):
    collectables = sorted(
        Path("/files/assignments-review/handin/").glob(
            f"**/{assignment_name}/**/{assignment_folder}"
        )
    )
    clog.debug(collectables)
    if len(collectables) == 0:
        raise NoCollectiblesException(
            f"Found no collectable submissions with assignment_name {assignment_name} and assignment folder {assignment_folder}."
        )
    return collectables


def path_identify(path):
    path_split = path.parts
    return {"prefix": f"{path_split[0]}{path_split[1]/path_split[2]/path_split[3]}"}


def path_prefix(path_split):
    return f"{path_split[4]}/{path_split[6]}"


def distinct_submissions(collectables):
    path_splits = [x.parts for x in collectables]
    relevant_info = list(set([path_prefix(x) for x in path_splits]))
    instance_id_map = extract_instance_id(relevant_info)
    clog.debug(instance_id_map)
    return instance_id_map


def extract_instance_id(its):
    pattern_instance = re.compile("(single_user_inst.*)/(.*)")
    return [{pattern_instance.search(x).group(1): [x]} for x in its]


def instance_grouped(assignment_list):
    res = {}

    for d in assignment_list:
        for k in d.keys():
            if res.get(k) is None:
                res[k] = d[k]
            else:
                res[k] = res[k] + d[k]
    return res


def get_latest_assignment(items):
    pattern_date_time = re.compile(
        r"(.*)/([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2})_(.*)"
    )

    datestrings = [pattern_date_time.search(x).group(2) for x in items]

    dates = {dt.strptime(y, "%Y-%m-%d_%H:%M:%S"): y for y in datestrings}
    latest = max(list(dates.keys()))
    return dates[latest]


def gather_latest_submissions(user_grouped_submission_info):
    filtered_submissions = {
        k: get_latest_assignment(v) for k, v in user_grouped_submission_info.items()
    }
    clog.debug(filtered_submissions)
    return filtered_submissions


def create_folder_structure(target_folder, filtered_info):

    # Check first if the target_folder exists

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    """ 
    Not needed: shutil.copytree does this.
    
    for k,v in filtered_info.items():
        new_path = target_folder + '/' + k
        clog.debug(new_path)
        if os.path.exists(new_path):
            clog.warning(f"Folder {new_path} already exists.")
        else:
            clog.debug(f"Creating {new_path}.")
            os.makedirs(new_path)
    """
    pass


def copy_submissions(target_folder, filtered_info, assignment_name, assignment_folder):
    clog.debug(filtered_info)
    copy_metadata = {"meta": {}, "items": []}
    copy_info = []
    for k, v in filtered_info.items():
        src_path = sorted(
            Path("/files/assignments-review/handin/").glob(
                f"{k}/{assignment_name}/{v}*/{assignment_folder}"
            )
        )
        if len(src_path) > 1:
            clog.error(f"Ambiguous source for {k}. Please collect manually.")
            raise AmbiguousCopySourceException(
                f"Ambiguous source for {k}. Please collect manually."
            )
        clog.debug(src_path)

        target_path = f"{target_folder}/{k}/"

        copy_info += [{"src": str(src_path[0]), "target": target_path}]
        shutil.copytree(src_path[0], target_path)

    copy_metadata["items"] = copy_info
    write_manifest_file(target_folder, copy_metadata)
    return 0


def write_manifest_file(target_folder, data):

    now = dt.now()
    printable_now = now.strftime("%Y-%m-%d %H:%M:%S")
    data["meta"]["write_time"] = printable_now
    loc = f"{target_folder}/nvcollect_manifest.json"

    with open(loc, "w") as fp:
        json.dump(data, fp)
    return

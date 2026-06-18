from pathlib import Path
import os
import shutil
from nuvolos_collect.logging import clog
from nuvolos_collect.collect.utils import (
    identify_collectables,
    distinct_submissions,
    instance_grouped,
    gather_latest_submissions,
    write_manifest_file,
)
from nuvolos_collect.exception import NoCollectiblesException


HANDIN_BASE = Path("/files/assignments-review/handin/")


def discover_assignment_pairs(assignment_name=None, assignment_folder=None):
    pairs = set()
    for instance_dir in HANDIN_BASE.iterdir():
        if not instance_dir.is_dir():
            continue
        for aname_dir in instance_dir.iterdir():
            if not aname_dir.is_dir():
                continue
            if assignment_name and aname_dir.name != assignment_name:
                continue
            for ts_dir in aname_dir.iterdir():
                if not ts_dir.is_dir():
                    continue
                for afolder_dir in ts_dir.iterdir():
                    if afolder_dir.is_dir():
                        if assignment_folder and afolder_dir.name != assignment_folder:
                            continue
                        pairs.add((aname_dir.name, afolder_dir.name))
    return sorted(pairs)


def archive_copy_submissions(target_folder, filtered_info, assignment_name, assignment_folder):
    copy_info = []
    for k, v in filtered_info.items():
        src_path = sorted(
            HANDIN_BASE.glob(f"{k}/{assignment_name}/{v}*/{assignment_folder}")
        )
        if len(src_path) == 0:
            clog.warning(f"No source found for instance {k}, skipping.")
            continue
        if len(src_path) > 1:
            clog.warning(f"Ambiguous source for {k}, using first match.")

        target_path = os.path.join(target_folder, k)
        shutil.copytree(src_path[0], target_path, dirs_exist_ok=True)
        copy_info.append({"src": str(src_path[0]), "target": target_path})

    return copy_info


def archive(target_folder, assignment_name=None, assignment_folder=None):
    pairs = discover_assignment_pairs(assignment_name, assignment_folder)

    if not pairs:
        clog.error("No assignments found to archive.")
        return 1

    by_name = {}
    for aname, afolder in pairs:
        by_name.setdefault(aname, []).append(afolder)

    clog.info(f"Found {len(by_name)} assignment(s) to archive.")

    archived = 0
    for aname, afolders in sorted(by_name.items()):
        assignment_target = os.path.join(target_folder, aname)
        all_copy_info = []

        for afolder in afolders:
            try:
                colls = identify_collectables(aname, afolder)
            except NoCollectiblesException:
                clog.warning(f'No submissions for "{aname}/{afolder}", skipping.')
                continue

            iinfo = distinct_submissions(colls)
            ugs = instance_grouped(iinfo)
            filtered = gather_latest_submissions(ugs)

            os.makedirs(assignment_target, exist_ok=True)
            copy_info = archive_copy_submissions(
                assignment_target, filtered, aname, afolder
            )
            all_copy_info.extend(copy_info)

        if not all_copy_info:
            continue

        write_manifest_file(assignment_target, {"meta": {}, "items": all_copy_info})

        shutil.make_archive(
            base_name=assignment_target,
            format="zip",
            root_dir=target_folder,
            base_dir=aname,
        )

        clog.info(
            f'Archived "{aname}" ({len(all_copy_info)} submissions) -> {assignment_target}.zip'
        )
        archived += 1

    clog.info(f"Archive completed. {archived} assignment(s) archived.")
    return 0

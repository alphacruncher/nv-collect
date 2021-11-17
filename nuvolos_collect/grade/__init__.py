import json
import os

from nuvolos_collect.logging import clog
from nuvolos_collect.exception import ManifestMissingException, MissingAutograderFile
from nuvolos_collect.handback.utils import read_manifest


def otter_grade(source_folder, autograder_location, relative_path, grade_identifier=""):
    # from otter.api import grade_submission

    if not os.path.exists(autograder_location):
        clog.error(
            f"The autograder.zip file at location {autograder_location} does not exist."
        )
        return 1

    manifest_data = read_manifest(source_folder)

    homework_folders = manifest_data["items"]

    results = []

    if grade_identifier != "":
        grade_identifier = "_" + grade_identifier

    for d in homework_folders:
        location_folder = d["target"]
        full_hw_location = os.path.join(location_folder, relative_path)

        # hw_result = grade_submission(full_hw_location, autograder_location)

        # hw_result_dict = hw_result.to_dict()
        hw_result_dict = {"a": 1}

        results += [{"location": full_hw_location, "result": hw_result_dict}]

        student_result_location = os.path.join(
            location_folder, f"grade{grade_identifier}.json"
        )

        with open(student_result_location, "w") as fp:
            json.dump(hw_result_dict, fp)

    full_result_file_loc = student_result_location = os.path.join(
        source_folder, f"grade{grade_identifier}.json"
    )

    with open(student_result_location, "w") as fp:
        json.dump(results, fp)

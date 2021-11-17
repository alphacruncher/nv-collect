import json
import os
import re

from nuvolos_collect.logging import clog
from nuvolos_collect.exception import ManifestMissingException, MissingAutograderFile
from nuvolos_collect.handback.utils import read_manifest
from nuvolos_collect.grade.utils import generate_df, merge_csv


def otter_grade(source_folder, autograder_location, relative_path, grade_identifier=""):
    from otter.api import grade_submission
    import pandas as pd

    if not os.path.exists(autograder_location):
        clog.error(
            f"The autograder.zip file at location {autograder_location} does not exist."
        )
        return 1

    manifest_data = read_manifest(source_folder)

    homework_folders = manifest_data["items"]

    results = []
    csv_results = []
    if grade_identifier != "":
        grade_identifier = "_" + grade_identifier

    for d in homework_folders:
        location_folder = d["target"]
        full_hw_location = os.path.join(location_folder, relative_path)
        clog.debug(f"Grading {full_hw_location}.")

        if not os.path.exists(full_hw_location):
            clog.warning(
                f"No homework found at location {full_hw_location}. Continuing."
            )
            hw_result_dict = {full_hw_location: "Missing"}

        else:
            hw_result = grade_submission(full_hw_location, autograder_location)
            hw_result_dict = hw_result.to_dict()
            csv_score_result = generate_df(hw_result_dict, d["src"])
            clog.debug(csv_score_result)

        results += [{"location": full_hw_location, "result": hw_result_dict}]
        csv_results += [csv_score_result]

        student_result_location = os.path.join(
            location_folder, f"grade{grade_identifier}.csv"
        )

        """
        with open(student_result_location, "w") as fp:
            json.dump(hw_result_dict, fp)
        """
        csv_score_result.to_csv(student_result_location)

    full_result_file_loc = os.path.join(source_folder, f"grade{grade_identifier}.csv")

    """
    with open(student_result_location, "w") as fp:
        json.dump(results, fp)
    """
    csv_score = merge_csv(csv_results)
    csv_score.to_csv(full_result_file_loc)

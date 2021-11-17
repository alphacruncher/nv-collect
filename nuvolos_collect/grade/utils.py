from nuvolos_collect.logging import clog


def generate_df(data_dict, tag_info):
    import pandas as pd
    import re

    student_id_re = re.compile("(.*handin)/([a-zA-Z0-9_]*)/(.*)")
    clog.debug(tag_info)
    matching = student_id_re.search(tag_info)
    student_id = matching.group(2)

    student_result = pd.DataFrame(data_dict)[0:1]
    student_result["student_id"] = student_id
    return student_id


def merge_csv(df_list):
    import pandas as pd

    result = pd.concat(df_list, axis=0, join="inner").sort_index()
    return result

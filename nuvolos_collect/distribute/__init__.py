from nuvolos_collect.distribute.utils import (
    read_manifest,
    generate_target_info,
    execute_handback_copy,
    write_manifest_file,
)


def distribute(source_folder):

    """
    Read the collection manifest log.
    """
    source_info = read_manifest(source_folder)
    """
    Create an in-memory re-distribution manifest log.
    """
    target_info = generate_target_info(source_info)
    """
    Execute the re-distribution.
    """
    execute_handback_copy(target_info)
    """
    Write handback manifest.
    """
    write_manifest_file(source_folder, target_info)

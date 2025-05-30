def get_highest_version_file(directory: str, base_filename: str) -> str:
    """
    Determines the highest version file and returns its full path.
    """
    highest_version = set_file_version(directory, base_filename)
    openshift_file_path = os.path.join(directory, f"{base_filename}.v{highest_version}.yaml")
    return openshift_file_path
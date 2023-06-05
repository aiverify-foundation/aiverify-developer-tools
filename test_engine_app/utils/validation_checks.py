from pathlib import Path


def is_folder(argument: Path) -> bool:
    """
    A helper function to check if argument is a folder

    Args:
        argument (Path): path to folder

    Returns:
        bool: True if argument is a folder
    """
    return argument.is_dir()


def is_file(argument: str) -> bool:
    """
    A helper function to check if argument is a file

    Args:
        argument (str): path to file

    Returns:
        bool: True if argument is a file
    """
    return Path(argument).is_file()


def is_empty_string(argument: str) -> bool:
    """
    A helper function to check if argument is an empty string

    Args:
        argument (str): string to be checked

    Returns:
        bool: True if argument is an empty string
    """
    if argument is None or argument == "None" or argument == "none" or argument == "":
        return True
    else:
        return len(argument.strip()) <= 0

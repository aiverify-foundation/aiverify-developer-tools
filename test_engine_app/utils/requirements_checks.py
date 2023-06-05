import json
import subprocess
import sys
from typing import List, Tuple

import semantic_version
from iscompatible import iscompatible


def get_installed_packages() -> Tuple[bool, str]:
    """
    A helper function to get installed packages on host environment

    Args:

    Raises:
        json.JSONDecodeError: Raise exception when the returned string of pip list isn't in json format

    Returns:
        tuple(bool, str): tuple containing bool indicating whether call is successful and
                    list of installed packages on host in json array format with each installed package info
                    is represented as a json, if successful. Otherwise, exception message.
    """

    try:
        result = subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--format", "json"]
        )
        return True, json.loads(result)
    except json.JSONDecodeError as error:
        error_msg = str(error)
        return False, error_msg


def get_package_version(package_name: str, packages_json: List) -> Tuple[bool, str]:
    """
    A helper function to find the package in the packages (package_json) and retrieve the version
    of that package in the packages(package_json)

    Args:
        package_name (str): name of subject
        packages_json (list): list of packages which the subject check against

    Returns:
        tuple(bool, str): tuple containing bool indicating whether call is successful and
                          version string of package defined in package_json
                          if found, otherwise empty string
    """

    for package_info in packages_json:
        if package_name == package_info["name"]:
            return True, package_info["version"]
    return False, "Unable to get package version"


def extract_package_name(package_version_requirement: str) -> Tuple[bool, str]:
    """
    A helper function to extract the name of package from the package version requirement

    Args:
        package_version_requirement (str): package version requirement

    Returns:
        tuple(bool, str): tuple containing bool indicating whether call is successful and name of package if found,
                    otherwise error message
    """

    list_of_token_symbol = ["=", ">", "<"]

    token_found = False
    list_of_position = []

    # find the position where the name of package ends
    for token in list_of_token_symbol:
        position_of_token = package_version_requirement.find(token)
        if position_of_token > 0:
            token_found = True
            list_of_position.append(position_of_token)

    if token_found:
        min_position = min(list_of_position)
        # extract the name of package
        package_name = package_version_requirement[0:min_position]
    else:
        return False, "Unable to determine the package name"

    return True, package_name


def remove_empty(tuples: Tuple) -> Tuple:
    """
    A helper function to remove away empty field(s)

    Args:
        tuples (str): tuple that may contain empty fields. E.g.: ()

    Returns:
        tuple: tuple with all empty fields removed
    """
    tuples = [t for t in tuples if t]
    return tuple(tuples)


def is_package_supported(package_version_requirement: str) -> Tuple[bool, str]:
    """
    A helper function to check if the package version requirement can be supported in
    current host environment

    Args:
        package_version_requirement: specifying package and the version requirement e.g.:'numpy>=1.2.3, <2.0.0'

    Returns:
        (bool, str): tuple containing bool indicating whether package is supported and error message
                if the call is unsuccessful
    """
    get_installed_packages_result = get_installed_packages()
    if not get_installed_packages_result[0]:
        # if failed to get installed packages, return False and error message
        return get_installed_packages_result

    return is_package_in_json(
        package_version_requirement, get_installed_packages_result[1]
    )


def is_package_in_json(
    package_version_requirement: str, packages_json: List
) -> Tuple[bool, str]:
    """
    A helper function to check if the package version requirement can be supported based on the
    packages specified in packages_json

    Args:
        package_version_requirement (str): requirement specification of a package
        packages_json (list): list of packages which the package requirement check against

    Returns:
        (bool, str): True if requirements of the package can be supported. Otherwise, False
    """

    extract_package_name_result = extract_package_name(package_version_requirement)
    if not extract_package_name_result[0]:
        return extract_package_name_result

    subject_package_name = extract_package_name_result[1].strip()
    # get the package version in the host
    package_version_result = get_package_version(subject_package_name, packages_json)
    if package_version_result[0]:
        # managed to get package version in packages_json
        package_version = package_version_result[1]
        package_semantic_version = semantic_version.Version(package_version)

        # package_semantic_version may contain empty fields, remove them
        package_semantic_version_tuple = remove_empty(tuple(package_semantic_version))

        try:
            # check compatibility
            result = iscompatible(
                package_version_requirement, package_semantic_version_tuple
            )
        except ValueError:
            return False, "Error handling package version value"

        if result:
            return result, ""
        else:
            return result, "Not compatible"
    else:
        return False, "Unable to find the package version on host environment"

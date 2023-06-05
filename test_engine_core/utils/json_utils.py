import json
from typing import Any, Dict

import jsonschema
import numpy
from jsonschema.validators import validate


def scan_for_single_quotes(input_data: str) -> str:
    """
    A function to replace all single quotes to double quotes in error messages

    Args:
        input_data (str): input data

    Returns:
        str: modified input data without single quotes
    """
    return input_data.replace("'", '"')


def remove_numpy_formats(data: Any) -> Any:
    """
    A recursive function to check through the given dictionary to
    ensure the keys are strings and recast numpy formats values from the dictionary

    Args:
        data (Any): Input data

    Returns:
         Any: Formatted result
    """
    if data is None:
        return None

    elif isinstance(data, numpy.integer):
        return int(data)

    elif isinstance(data, numpy.floating):
        return float(data)

    elif isinstance(data, numpy.ndarray):
        return data.tolist()

    elif type(data) is list:
        for count, _ in enumerate(data):
            data[count] = remove_numpy_formats(data[count])
        return data

    elif type(data) is dict:
        new_results = dict()
        for key, value in data.items():
            new_results.update({str(key): remove_numpy_formats(value)})
        return new_results

    else:
        return data


def validate_json(data: dict, schema: dict) -> bool:
    """
    A function to validate data with the provided json schema

    Args:
        data (dict): input data dictionary
        schema (dict): input json schema to be validated with

    Returns:
        bool: True if validation is successful
    """
    try:
        validate(instance=data, schema=schema)
        return True

    except jsonschema.exceptions.ValidationError:
        return False


def load_schema_file(schema_path: str) -> Dict:
    """
    A function to load the JSON schema at the given path as a Python object

    Args:
        schema_path (str): A filename for a JSON schema.

    Raises:
        RuntimeError: Invalid JSON when loading the schema file

    Returns:
        Dict: A Python object representation of the schema.
    """
    try:
        with open(schema_path) as schema_path:
            schema = json.load(schema_path)
            return schema

    except ValueError as error:
        raise RuntimeError(f"Invalid JSON in schema: {str(error)}")

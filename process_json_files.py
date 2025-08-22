"""
This module provides utility functions for reading, writing,
and processing ship data in JSON format.

Functions:
    - read_json_data(path): Reads JSON data from a specified file.
    - write_json_data(path, data): Writes dictionary data to a JSON file.
"""


import json


def read_json_data(path):
    """
    Reads JSON data from the specified file path.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict or None: Parsed JSON data as a dictionary, or None if the file is not found.
    """
    try:
        with open(path, "r") as file:
            json_str = file.read()
            data = json.loads(json_str)
        return data
    except FileNotFoundError as error:
        print("There has been an error ...", error)
        return None


def write_json_data(path, data):
    """
    Writes dictionary data to a JSON file at the specified path.

    Args:
        path (str): Path to the output JSON file.
        data (dict): Dictionary data to write.
    """
    try:
        with open(path, "w") as file:
            json_str = json.dumps(data)
            file.write(json_str)
    except FileExistsError as error:
        print("There has been an error ...", error)

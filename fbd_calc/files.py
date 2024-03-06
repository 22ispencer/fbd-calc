from fbd_calc.data import AppData
import json
from pydantic import ValidationError


def write(app_data: AppData,
          filename: str = "fbd-data.json"):
    """
    For writing to a file

    Args:
        app_data (AppData): The data to write
        filename (str): The name/path of the file to write to
    """

    data = app_data.model_dump_json(indent=2)

    with open(filename, "w") as outfile:
        outfile.write(data)


def read(filename: str) -> AppData | bool:
    """
    For reading from a given file

    Args:
        filename (str): The name of the input file

    Returns:
         AppData | bool: AppData with all the app data, or False if the given
         file is in an invalid format
    """
    with open(filename, "r") as file:
        file_data = file.readall()

        try:
            app_data = AppData.model_validate_json(file_data)
        except ValidationError:
            return False
        else:
            return app_data
